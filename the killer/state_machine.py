import time
from datetime import datetime
import csv
import os

class FarmGateStateMachine:
    def __init__(self):
        self.state = "SAFE"  # SAFE, INTRUSION, EXIT
        self.last_state_change = time.time()
        self.intrusion_start_time = None
        self.events_file = "events/events.csv"
        self.ensure_events_file()
    
    def ensure_events_file(self):
        """Create events CSV file if it doesn't exist"""
        if not os.path.exists("events"):
            os.makedirs("events")
        
        if not os.path.exists(self.events_file):
            with open(self.events_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "event", "description_sinhala", "description_english"])
    
    def update_state(self, detection_status):
        """Update state based on detection status"""
        current_time = time.time()
        
        if detection_status == "ඇතුළු වී ඇත":
            if self.state == "SAFE":
                self.state = "INTRUSION"
                self.intrusion_start_time = current_time
                self.log_event("ENTER", "සතුන් වත්තට ඇතුළු වී ඇත", "Animals entered the farm")
                return "ENTER"
            elif self.state == "INTRUSION":
                return "CONTINUE_INTRUSION"
        
        elif detection_status == "පිටවී ගොස් ඇත":
            if self.state == "INTRUSION":
                self.state = "SAFE"
                intrusion_duration = current_time - self.intrusion_start_time if self.intrusion_start_time else 0
                self.log_event("EXIT", f"සතුන් වත්තෙන් පිටවී ගොස් ඇත (කාලය: {int(intrusion_duration)}s)", 
                             f"Animals left the farm (Duration: {int(intrusion_duration)}s)")
                self.intrusion_start_time = None
                return "EXIT"
            elif self.state == "SAFE":
                return "CONTINUE_SAFE"
        
        elif detection_status == "සුරක්ෂිතයි":
            if self.state == "INTRUSION":
                # Check if enough time has passed to consider it an exit
                if current_time - self.last_state_change > 3.0:  # 3 seconds threshold
                    self.state = "SAFE"
                    intrusion_duration = current_time - self.intrusion_start_time if self.intrusion_start_time else 0
                    self.log_event("EXIT", f"සතුන් වත්තෙන් පිටවී ගොස් ඇත (කාලය: {int(intrusion_duration)}s)", 
                                 f"Animals left the farm (Duration: {int(intrusion_duration)}s)")
                    self.intrusion_start_time = None
                    return "EXIT"
                else:
                    return "CONTINUE_INTRUSION"
            elif self.state == "SAFE":
                return "CONTINUE_SAFE"
        
        self.last_state_change = current_time
        return "NO_CHANGE"
    
    def log_event(self, event_type, sinhala_desc, english_desc):
        """Log event to CSV file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.events_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, event_type, sinhala_desc, english_desc])
        except Exception as e:
            print(f"Error logging event: {e}")
    
    def get_current_state(self):
        """Get current state information"""
        return {
            "state": self.state,
            "is_intrusion": self.state == "INTRUSION",
            "is_safe": self.state == "SAFE",
            "intrusion_duration": time.time() - self.intrusion_start_time if self.intrusion_start_time else 0
        }
    
    def get_state_display(self):
        """Get Sinhala display text for current state"""
        if self.state == "SAFE":
            return "සුරක්ෂිතයි", "🟢"
        elif self.state == "INTRUSION":
            return "ඇතුළු වී ඇත", "🔴"
        else:
            return "අක්‍රීයයි", "⚪"
    
    def reset_state(self):
        """Reset state machine to safe state"""
        self.state = "SAFE"
        self.intrusion_start_time = None
        self.last_state_change = time.time()
