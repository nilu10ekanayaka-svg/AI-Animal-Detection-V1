import cv2
import numpy as np
import json
import time
from datetime import datetime
import os
import random

class AnimalDetector:
    def __init__(self, config_file="config.json"):
        """Initialize the animal detection system"""
        self.load_config(config_file)
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        self.camera = None
        self.detection_count = 0
        self.last_detection_time = 0
        self.is_detecting = False
        self.detected_animals = {}  # Store detected animals with their positions
        self.animal_names = ["ගවයා", "බැටළුවා", "කුකුලා", "හරකා", "අශ්වයා", "පූසා", "බල්ලා", "වල් සතා"]
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration
            self.config = {
                "min_area": 1000,
                "detection_frames": 5,
                "camera_index": 0,
                "detection_enabled": True
            }
    
    def initialize_camera(self):
        """Initialize camera connection"""
        try:
            # Try different camera backends
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]
            for backend in backends:
                try:
                    self.camera = cv2.VideoCapture(self.config.get("camera_index", 0), backend)
                    if self.camera.isOpened():
                        break
                except:
                    continue
            
            if not self.camera or not self.camera.isOpened():
                print("No camera found, using default")
                self.camera = cv2.VideoCapture(self.config.get("camera_index", 0))
            
            if not self.camera.isOpened():
                return False
                
            # Set camera properties for better performance and quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            self.camera.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
            self.camera.set(cv2.CAP_PROP_CONTRAST, 0.5)
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size
            return True
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def is_animal_motion(self, frame):
        """Enhanced detection to filter out humans and focus on animals"""
        # Convert to grayscale for better processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(blurred)
        
        # Enhanced morphological operations
        kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
        # Remove noise
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel_small)
        # Fill gaps
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel_large)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Enhanced filtering for animal detection
        animal_contours = []
        min_area = self.config.get("min_area", 1000)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # Animals typically have different aspect ratios than humans
                if 0.2 < aspect_ratio < 4.0:  # Wider range for different animal shapes
                    # Calculate contour properties
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    
                    if hull_area > 0:
                        solidity = area / hull_area
                        extent = area / (w * h) if w * h > 0 else 0
                        
                        # Animals tend to have more irregular shapes and different movement patterns
                        if (0.2 < solidity < 0.9 and  # Not too irregular, not too regular
                            0.1 < extent < 0.8 and    # Reasonable extent
                            w > 20 and h > 20):       # Minimum size
                            
                            # Additional check: contour perimeter vs area ratio
                            perimeter = cv2.arcLength(contour, True)
                            if perimeter > 0:
                                perimeter_area_ratio = (perimeter * perimeter) / area
                                if 10 < perimeter_area_ratio < 50:  # Reasonable ratio for animals
                                    animal_contours.append(contour)
        
        return len(animal_contours) > 0, animal_contours
    
    def detect_animals(self):
        """Main detection loop"""
        if not self.camera or not self.camera.isOpened():
            return False, None, "කැමරාව සම්බන්ධ කර නොමැත"
        
        ret, frame = self.camera.read()
        if not ret:
            return False, None, "කැමරාවෙන් රූපය ලබා ගැනීමට නොහැකි විය"
        
        if not self.config.get("detection_enabled", True):
            return True, frame, "අක්‍රීයයි"
        
        # Detect animal motion
        has_animals, contours = self.is_animal_motion(frame)
        
        if has_animals:
            self.detection_count += 1
            self.last_detection_time = time.time()
            
            # Draw bounding boxes around detected animals with names
            current_time = time.time()
            for i, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)
                
                # Generate or assign animal name
                animal_id = f"{x}_{y}_{w}_{h}"
                if animal_id not in self.detected_animals:
                    self.detected_animals[animal_id] = {
                        'name': random.choice(self.animal_names),
                        'first_seen': current_time,
                        'position': (x, y, w, h)
                    }
                
                animal_info = self.detected_animals[animal_id]
                animal_name = animal_info['name']
                
                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                
                # Draw animal name above the head (top of bounding box)
                text_size = cv2.getTextSize(animal_name, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y - 15
                
                # Draw background rectangle for text
                cv2.rectangle(frame, (text_x - 5, text_y - text_size[1] - 5), 
                             (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)
                
                # Draw animal name
                cv2.putText(frame, animal_name, (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                
                # Update position
                self.detected_animals[animal_id]['position'] = (x, y, w, h)
            
            # Clean up old animal detections (remove animals not seen for 5 seconds)
            current_time = time.time()
            animals_to_remove = []
            for animal_id, animal_info in self.detected_animals.items():
                if current_time - animal_info['first_seen'] > 5.0:
                    animals_to_remove.append(animal_id)
            
            for animal_id in animals_to_remove:
                del self.detected_animals[animal_id]
            
            # Check if we have enough consecutive detections
            if self.detection_count >= self.config.get("detection_frames", 5):
                if not self.is_detecting:
                    self.is_detecting = True
                    return True, frame, "ඇතුළු වී ඇත"
                else:
                    return True, frame, "ඇතුළු වී ඇත"
        else:
            # Reset detection count if no animals detected
            if self.detection_count > 0:
                # Check if enough time has passed without detection
                if time.time() - self.last_detection_time > 2.0:  # 2 seconds
                    if self.is_detecting:
                        self.is_detecting = False
                        self.detection_count = 0
                        return True, frame, "පිටවී ගොස් ඇත"
                    else:
                        self.detection_count = 0
                        return True, frame, "සුරක්ෂිතයි"
                else:
                    return True, frame, "ඇතුළු වී ඇත"
            else:
                return True, frame, "සුරක්ෂිතයි"
    
    def get_status(self):
        """Get current system status"""
        if not self.camera or not self.camera.isOpened():
            return "අක්‍රීයයි", "කැමරාව සම්බන්ධ කර නොමැත"
        
        if self.is_detecting:
            return "ඇතුළු වී ඇත", "සතුන් අනාවරණය වී ඇත"
        else:
            return "සුරක්ෂිතයි", "සියල්ල සාමාන්‍යයි"
    
    def release_camera(self):
        """Release camera resources"""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
    
    def __del__(self):
        """Cleanup on destruction"""
        self.release_camera()
