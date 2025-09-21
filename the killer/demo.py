#!/usr/bin/env python3
"""
Demo script for Farm Security System
This script demonstrates the key features of the system
"""

import cv2
import time
import json
from detector import AnimalDetector
from sms_system import SMSSystem
from alarm_system import AlarmSystem

def demo_detection():
    """Demo the animal detection system"""
    print("🔍 Animal Detection Demo")
    print("=" * 50)
    
    detector = AnimalDetector()
    
    if detector.initialize_camera():
        print("✅ Camera initialized successfully")
        
        print("📹 Starting detection demo (10 seconds)...")
        print("Move in front of the camera to test detection")
        
        start_time = time.time()
        while time.time() - start_time < 10:
            success, frame, status = detector.detect_animals()
            
            if success and frame is not None:
                # Display the frame
                cv2.imshow('Animal Detection Demo', frame)
                
                if status == "ඇතුළු වී ඇත":
                    print(f"🚨 Animals detected! Status: {status}")
                elif status == "පිටවී ගොස් ඇත":
                    print(f"✅ Animals left! Status: {status}")
                elif status == "සුරක්ෂිතයි":
                    print(f"🟢 Secure! Status: {status}")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
        detector.release_camera()
        print("✅ Detection demo completed")
    else:
        print("❌ Camera initialization failed")

def demo_sms():
    """Demo the SMS system"""
    print("\n📱 SMS System Demo")
    print("=" * 50)
    
    sms = SMSSystem()
    
    print(f"SMS Status: {sms.get_status()}")
    
    if sms.is_enabled():
        print("📤 Sending test SMS...")
        success, message = sms.send_test_sms()
        print(f"Result: {'✅' if success else '❌'} {message}")
    else:
        print("⚠️ SMS is disabled - check your Twilio credentials in config.json")

def demo_alarm():
    """Demo the alarm system"""
    print("\n🔊 Alarm System Demo")
    print("=" * 50)
    
    alarm = AlarmSystem()
    
    print("🔊 Testing alarm system...")
    success, message = alarm.start_alarm()
    print(f"Start Alarm: {'✅' if success else '❌'} {message}")
    
    if success:
        print("⏰ Playing alarm for 3 seconds...")
        time.sleep(3)
        
        success, message = alarm.stop_alarm()
        print(f"Stop Alarm: {'✅' if success else '❌'} {message}")

def demo_config():
    """Demo the configuration system"""
    print("\n⚙️ Configuration Demo")
    print("=" * 50)
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("📋 Current Configuration:")
        print(f"  📱 Farmer Phone: {config.get('farmer_phone', 'Not set')}")
        print(f"  📏 Min Area: {config.get('min_area', 'Not set')}")
        print(f"  🎬 Detection Frames: {config.get('detection_frames', 'Not set')}")
        print(f"  📹 Camera Index: {config.get('camera_index', 'Not set')}")
        print(f"  🔔 Alarm File: {config.get('alarm_file', 'Not set')}")
        print(f"  📧 SMS Enabled: {config.get('sms_enabled', 'Not set')}")
        
    except FileNotFoundError:
        print("❌ config.json file not found")
    except json.JSONDecodeError:
        print("❌ Invalid JSON in config.json")

def main():
    """Main demo function"""
    print("🚀 Farm Security System Demo")
    print("=" * 60)
    print("This demo will test all major components of the system")
    print("=" * 60)
    
    # Demo configuration
    demo_config()
    
    # Demo SMS system
    demo_sms()
    
    # Demo alarm system
    demo_alarm()
    
    # Demo detection system
    demo_detection()
    
    print("\n🎉 Demo completed!")
    print("=" * 60)
    print("To start the full system, run: python app.py")
    print("Then open: http://localhost:5000")

if __name__ == "__main__":
    main()