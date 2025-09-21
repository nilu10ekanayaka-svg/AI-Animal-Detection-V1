
import pygame
import threading
import time
import os
from datetime import datetime

class AlarmSystem:
    def __init__(self, alarm_file="static/alert.wav"):
        """Initialize alarm system"""
        self.alarm_file = alarm_file
        self.is_playing = False
        self.should_stop = False
        self.alarm_thread = None
        self.pygame_initialized = False
        self.initialize_pygame()
    
    def initialize_pygame(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.pygame_initialized = True
            print("Audio system initialized successfully")
        except Exception as e:
            print(f"Audio initialization error: {e}")
            self.pygame_initialized = False
    
    def start_alarm(self):
        """Start playing alarm in background thread"""
        if not self.pygame_initialized:
            print("Audio system not initialized - alarm disabled")
            return False, "ශබ්ද පද්ධතිය අක්‍රීයයි"
        
        if self.is_playing:
            return True, "ඇලම් දැනටමත් වාදනය වේ"
        
        if not os.path.exists(self.alarm_file):
            return False, f"ඇලම් ගොනුව හමු නොවීය: {self.alarm_file}"
        
        self.should_stop = False
        self.alarm_thread = threading.Thread(target=self._play_alarm_loop, daemon=True)
        self.alarm_thread.start()
        
        return True, "ඇලම් ආරම්භ කරන ලදී"
    
    def stop_alarm(self):
        """Stop playing alarm"""
        if not self.is_playing:
            return True, "ඇලම් දැනටමත් නවතා ඇත"
        
        self.should_stop = True
        self.is_playing = False
        
        # Wait for thread to finish (with timeout)
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join(timeout=2.0)
        
        return True, "ඇලම් නවතා ඇත"
    
    def _play_alarm_loop(self):
        """Internal method to play alarm in loop"""
        try:
            self.is_playing = True
            print(f"Starting alarm loop: {self.alarm_file}")
            
            while not self.should_stop:
                try:
                    # Load and play the alarm sound
                    pygame.mixer.music.load(self.alarm_file)
                    pygame.mixer.music.play()
                    
                    # Wait for the sound to finish or stop signal
                    while pygame.mixer.music.get_busy() and not self.should_stop:
                        time.sleep(0.1)
                    
                    if self.should_stop:
                        break
                        
                except pygame.error as e:
                    print(f"Error playing alarm: {e}")
                    break
                except Exception as e:
                    print(f"Unexpected error in alarm loop: {e}")
                    break
            
            # Stop any playing music
            pygame.mixer.music.stop()
            self.is_playing = False
            print("Alarm loop ended")
            
        except Exception as e:
            print(f"Error in alarm thread: {e}")
            self.is_playing = False
    
    def test_alarm(self):
        """Test alarm for a short duration"""
        if not self.pygame_initialized:
            return False, "ශබ්ද පද්ධතිය අක්‍රීයයි"
        
        if not os.path.exists(self.alarm_file):
            return False, f"ඇලම් ගොනුව හමු නොවීය: {self.alarm_file}"
        
        try:
            # Play alarm for 3 seconds
            pygame.mixer.music.load(self.alarm_file)
            pygame.mixer.music.play()
            
            # Start a timer to stop after 3 seconds
            def stop_after_delay():
                time.sleep(3)
                pygame.mixer.music.stop()
            
            timer_thread = threading.Thread(target=stop_after_delay, daemon=True)
            timer_thread.start()
            
            return True, "ඇලම් පරීක්ෂා කරන ලදී"
        
        except Exception as e:
            return False, f"ඇලම් පරීක්ෂා දෝෂය: {str(e)}"
    
    def is_playing_alarm(self):
        """Check if alarm is currently playing"""
        return self.is_playing
    
    def get_status(self):
        """Get alarm system status"""
        if not self.pygame_initialized:
            return "අක්‍රීයයි", "ශබ්ද පද්ධතිය අක්‍රීයයි"
        elif self.is_playing:
            return "වාදනය වේ", "ඇලම් වාදනය වේ"
        else:
            return "සුරක්ෂිතයි", "ඇලම් නවතා ඇත"
    
    def set_alarm_file(self, file_path):
        """Set new alarm file"""
        if os.path.exists(file_path):
            self.alarm_file = file_path
            return True, f"ඇලම් ගොනුව යාවත්කාලීන කරන ලදී: {file_path}"
        else:
            return False, f"ගොනුව හමු නොවීය: {file_path}"
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_alarm()
        if self.pygame_initialized:
            pygame.mixer.quit()
