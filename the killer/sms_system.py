import os
import json

# Import Twilio with proper error handling
try:
    from twilio.rest import Client
    from twilio.base.exceptions import TwilioException
    TWILIO_AVAILABLE = True
except ImportError:
    print("Warning: Twilio library not installed. SMS functionality will be disabled.")
    print("To enable SMS, install Twilio with: pip install twilio")
    Client = None
    TwilioException = Exception
    TWILIO_AVAILABLE = False

class SMSSystem:
    def __init__(self, config_file="config.json"):
        """Initialize SMS system with Twilio"""
        self.load_config(config_file)
        self.client = None
        self.sms_enabled = False
        self.initialize_twilio()
    
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
    
    def initialize_twilio(self):
        """Initialize Twilio client"""
        if not TWILIO_AVAILABLE:
            print("Twilio library not available - Using mock SMS system")
            self.sms_enabled = True
            self.mock_mode = True
            return
            
        try:
            # Try to get credentials from environment variables first
            account_sid = os.getenv('TWILIO_SID', self.config.get('twilio_sid'))
            auth_token = os.getenv('TWILIO_AUTH', self.config.get('twilio_auth'))
            from_number = os.getenv('TWILIO_FROM', self.config.get('twilio_from'))
            
            if account_sid and auth_token and from_number:
                # Check if credentials are placeholder values
                if (account_sid.startswith("YOUR_") or 
                    auth_token.startswith("YOUR_") or 
                    from_number.startswith("YOUR_")):
                    print("SMS credentials not configured - Using mock SMS system")
                    print("SMS will be logged to sms_log.json file")
                    self.sms_enabled = True
                    self.mock_mode = True
                else:
                    self.client = Client(account_sid, auth_token)
                    self.from_number = from_number
                    self.sms_enabled = True
                    self.mock_mode = False
                    print("SMS system initialized successfully with Twilio")
            else:
                print("SMS credentials not found - Using mock SMS system")
                self.sms_enabled = True
                self.mock_mode = True
        except Exception as e:
            print(f"SMS initialization error: {e} - Using mock SMS system")
            self.sms_enabled = True
            self.mock_mode = True
    
    def send_animal_enter_alert(self, farmer_phone=None):
        """Send SMS alert when animals enter"""
        if not self.sms_enabled:
            return False, "SMS අක්‍රීයයි"
        
        phone = farmer_phone or self.config.get('farmer_phone') or os.getenv('FARMER_PHONE')
        if not phone:
            return False, "කර්මිකාරයාගේ දුරකථන අංකය සකසා නැත"
        
        message = "ඔබේ වත්තට සතුන් ඇතුළු වී ඇත. කරුණාකර පරීක්ෂා කරන්න."
        return self.send_sms(phone, message)
    
    def send_animal_exit_alert(self, farmer_phone=None):
        """Send SMS alert when animals exit"""
        if not self.sms_enabled:
            return False, "SMS අක්‍රීයයි"
        
        phone = farmer_phone or self.config.get('farmer_phone') or os.getenv('FARMER_PHONE')
        if not phone:
            return False, "කර්මිකාරයාගේ දුරකථන අංකය සකසා නැත"
        
        message = "සතුන් වත්තෙන් පිටවී ගොස් ඇත."
        return self.send_sms(phone, message)
    
    def send_test_sms(self, farmer_phone=None):
        """Send test SMS"""
        if not self.sms_enabled:
            return False, "SMS අක්‍රීයයි"
        
        phone = farmer_phone or self.config.get('farmer_phone') or os.getenv('FARMER_PHONE')
        if not phone:
            return False, "කර්මිකාරයාගේ දුරකථන අංකය සකසා නැත"
        
        message = "කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය සාර්ථකව ක්‍රියාත්මක වේ."
        return self.send_sms(phone, message)
    
    def send_sms(self, to_number, message):
        """Send SMS using Twilio or mock system"""
        try:
            # Clean phone number (remove spaces, add + if needed)
            to_number = to_number.strip()
            if not to_number.startswith('+'):
                to_number = '+' + to_number
            
            # Use mock SMS if Twilio is not available or configured
            if hasattr(self, 'mock_mode') and self.mock_mode:
                return self._send_mock_sms(to_number, message)
            
            if not self.client:
                return False, "SMS සේවාව අක්‍රීයයි"
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            return True, f"SMS යවන ලදී (ID: {message_obj.sid})"
        
        except TwilioException as e:
            error_msg = f"Twilio දෝෂය: {str(e)}"
            print(error_msg)
            return False, error_msg
        
        except Exception as e:
            error_msg = f"SMS යැවීමේ දෝෂය: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def _send_mock_sms(self, to_number, message):
        """Send mock SMS (logs to file)"""
        try:
            from datetime import datetime
            
            # Load existing log
            sms_log = []
            try:
                with open("sms_log.json", "r", encoding="utf-8") as f:
                    sms_log = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                sms_log = []
            
            # Add new SMS record
            sms_record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "to": to_number,
                "message": message,
                "status": "SENT (MOCK)"
            }
            sms_log.append(sms_record)
            
            # Save to file
            with open("sms_log.json", "w", encoding="utf-8") as f:
                json.dump(sms_log, f, indent=2, ensure_ascii=False)
            
            print(f"📱 MOCK SMS SENT:")
            print(f"   To: {to_number}")
            print(f"   Message: {message}")
            print(f"   Time: {sms_record['timestamp']}")
            
            return True, f"SMS ලොග් කරන ලදී (Mock mode) - {sms_record['timestamp']}"
            
        except Exception as e:
            return False, f"Mock SMS දෝෂය: {str(e)}"
    
    def update_farmer_phone(self, phone_number):
        """Update farmer phone number in config"""
        try:
            self.config['farmer_phone'] = phone_number
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True, "දුරකථන අංකය යාවත්කාලීන කරන ලදී"
        except Exception as e:
            return False, f"යාවත්කාලීන දෝෂය: {str(e)}"
    
    def is_enabled(self):
        """Check if SMS is enabled"""
        return self.sms_enabled
    
    def get_status(self):
        """Get SMS system status"""
        if self.sms_enabled:
            phone = self.config.get('farmer_phone') or os.getenv('FARMER_PHONE')
            if phone:
                return "SMS සක්‍රීයයි", f"දුරකථන: {phone}"
            else:
                return "SMS සක්‍රීයයි", "දුරකථන අංකය සකසා නැත"
        else:
            return "SMS අක්‍රීයයි", "Twilio සක්‍රීය නොවේ"
