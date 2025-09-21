#!/usr/bin/env python3
"""
Farm Gate Monitor System - Test Script
කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය - පරීක්ෂා ස්ක්‍රිප්ට්
"""

import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from twilio.rest import Client
        print("✅ Twilio imported successfully")
    except ImportError as e:
        print(f"❌ Twilio import failed: {e}")
        return False
    
    try:
        import pygame
        print("✅ Pygame imported successfully")
    except ImportError as e:
        print(f"❌ Pygame import failed: {e}")
        return False
    
    return True

def test_config_files():
    """Test if configuration files exist and are valid"""
    print("\n🔍 Testing configuration files...")
    
    # Test config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✅ config.json is valid JSON")
            
            required_keys = ['min_area', 'detection_frames', 'farmer_phone', 'detection_enabled']
            for key in required_keys:
                if key in config:
                    print(f"✅ {key} found in config")
                else:
                    print(f"❌ {key} missing from config")
        except Exception as e:
            print(f"❌ config.json error: {e}")
            return False
    else:
        print("❌ config.json not found")
        return False
    
    return True

def test_detector():
    """Test animal detector initialization"""
    print("\n🔍 Testing animal detector...")
    
    try:
        from detector import AnimalDetector
        detector = AnimalDetector()
        print("✅ AnimalDetector initialized successfully")
        
        # Test camera initialization (may fail if no camera)
        if detector.initialize_camera():
            print("✅ Camera initialized successfully")
        else:
            print("⚠️ Camera initialization failed (no camera connected)")
        
        return True
    except Exception as e:
        print(f"❌ AnimalDetector error: {e}")
        return False

def test_state_machine():
    """Test state machine functionality"""
    print("\n🔍 Testing state machine...")
    
    try:
        from state_machine import FarmGateStateMachine
        sm = FarmGateStateMachine()
        print("✅ StateMachine initialized successfully")
        
        # Test state updates
        result = sm.update_state("සුරක්ෂිතයි")
        print(f"✅ State update test: {result}")
        
        result = sm.update_state("ඇතුළු වී ඇත")
        print(f"✅ Intrusion state test: {result}")
        
        return True
    except Exception as e:
        print(f"❌ StateMachine error: {e}")
        return False

def test_sms_system():
    """Test SMS system initialization"""
    print("\n🔍 Testing SMS system...")
    
    try:
        from sms_system import SMSSystem
        sms = SMSSystem()
        print("✅ SMSSystem initialized successfully")
        
        status, message = sms.get_status()
        print(f"✅ SMS status: {status} - {message}")
        
        return True
    except Exception as e:
        print(f"❌ SMSSystem error: {e}")
        return False

def test_alarm_system():
    """Test alarm system initialization"""
    print("\n🔍 Testing alarm system...")
    
    try:
        from alarm_system import AlarmSystem
        alarm = AlarmSystem()
        print("✅ AlarmSystem initialized successfully")
        
        status, message = alarm.get_status()
        print(f"✅ Alarm status: {status} - {message}")
        
        return True
    except Exception as e:
        print(f"❌ AlarmSystem error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = ['static', 'templates', 'events', 'tests', 'docs']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False
    
    return True

def test_templates():
    """Test if HTML templates exist"""
    print("\n🔍 Testing HTML templates...")
    
    required_templates = [
        'templates/dashboard.html',
        'templates/admin.html',
        'templates/events.html'
    ]
    
    for template in required_templates:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            return False
    
    return True

def test_batch_files():
    """Test if batch files exist"""
    print("\n🔍 Testing batch files...")
    
    batch_files = ['setup_env.bat', 'start.bat']
    
    for batch_file in batch_files:
        if os.path.exists(batch_file):
            print(f"✅ {batch_file} exists")
        else:
            print(f"❌ {batch_file} missing")
            return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය - පරීක්ෂා")
    print("Farm Gate Monitor System - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config_files,
        test_directories,
        test_templates,
        test_batch_files,
        test_detector,
        test_state_machine,
        test_sms_system,
        test_alarm_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"පරීක්ෂා ප්‍රතිඵල: {passed}/{total} සාර්ථක")
    print(f"Test Results: {passed}/{total} passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 සියලුම පරීක්ෂා සාර්ථක! පද්ධතිය සූදානම්!")
        print("🎉 All tests passed! System is ready!")
        return True
    else:
        print("⚠️ සමහර පරීක්ෂා අසාර්ථක විය. කරුණාකර පරීක්ෂා කරන්න.")
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
