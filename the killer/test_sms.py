#!/usr/bin/env python3
"""
Test SMS System - Works without Twilio
This creates a mock SMS system for testing
"""

import json
from datetime import datetime

class TestSMSSystem:
    def __init__(self):
        self.sms_log = []
    
    def send_sms(self, to_number, message):
        """Mock SMS sending - logs to file instead"""
        sms_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "to": to_number,
            "message": message,
            "status": "SENT (MOCK)"
        }
        self.sms_log.append(sms_record)
        
        # Save to file
        with open("sms_log.json", "w", encoding="utf-8") as f:
            json.dump(self.sms_log, f, indent=2, ensure_ascii=False)
        
        print(f"📱 MOCK SMS SENT:")
        print(f"   To: {to_number}")
        print(f"   Message: {message}")
        print(f"   Time: {sms_record['timestamp']}")
        
        return True, f"SMS logged successfully (Mock mode)"
    
    def send_animal_alert(self, phone_number):
        """Send animal detection alert"""
        message = "🚨 ඔබේ වත්තට සතුන් ඇතුළු වී ඇත! කරුණාකර පරීක්ෂා කරන්න."
        return self.send_sms(phone_number, message)
    
    def send_animal_exit_alert(self, phone_number):
        """Send animal exit alert"""
        message = "✅ සතුන් වත්තෙන් පිටවී ගොස් ඇත."
        return self.send_sms(phone_number, message)

if __name__ == "__main__":
    # Test the mock SMS system
    sms = TestSMSSystem()
    
    print("🧪 Testing Mock SMS System")
    print("=" * 40)
    
    # Test animal detection alert
    success, msg = sms.send_animal_alert("+94719563015")
    print(f"Animal Alert: {'✅' if success else '❌'} {msg}")
    
    # Test animal exit alert
    success, msg = sms.send_animal_exit_alert("+94719563015")
    print(f"Animal Exit: {'✅' if success else '❌'} {msg}")
    
    print("\n📋 SMS Log saved to: sms_log.json")
    print("🔧 To use real SMS, update config.json with valid Twilio credentials")

