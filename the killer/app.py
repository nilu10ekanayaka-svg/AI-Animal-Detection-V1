from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import cv2
import json
import threading
import time
from datetime import datetime
import os
import base64
import io
from PIL import Image
from werkzeug.utils import secure_filename

from detector import AnimalDetector
from state_machine import FarmGateStateMachine
from sms_system import SMSSystem
from alarm_system import AlarmSystem

app = Flask(__name__)

# File upload configuration
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global instances
detector = None
state_machine = None
sms_system = None
alarm_system = None
camera_thread = None
is_running = False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def initialize_systems():
    """Initialize all monitoring systems"""
    global detector, state_machine, sms_system, alarm_system
    
    detector = AnimalDetector()
    state_machine = FarmGateStateMachine()
    sms_system = SMSSystem()
    alarm_system = AlarmSystem()
    
    # Initialize camera
    if detector.initialize_camera():
        print("Camera initialized successfully")
    else:
        print("Camera initialization failed")

def camera_monitoring_loop():
    """Main monitoring loop running in background thread"""
    global is_running, detector, state_machine, sms_system, alarm_system
    
    while is_running:
        try:
            # Get detection result
            result = detector.detect_animals()
            if result is None:
                print("Detector returned None, skipping this iteration")
                time.sleep(0.1)
                continue
                
            success, frame, status = result
            
            if success:
                # Update state machine
                event = state_machine.update_state(status)
                
                # Handle state changes
                if event == "ENTER":
                    print("Animals detected - starting alarm and SMS")
                    alarm_system.start_alarm()
                    sms_system.send_animal_enter_alert()
                
                elif event == "EXIT":
                    print("Animals left - stopping alarm and sending SMS")
                    alarm_system.stop_alarm()
                    sms_system.send_animal_exit_alert()
                
                # Store current frame for web display
                if frame is not None:
                    # Encode frame for web display
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame_bytes = buffer.tobytes()
                    # Store in global variable for web access
                    app.current_frame = frame_bytes
            
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(1)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    """Admin panel page"""
    return render_template('admin.html')

@app.route('/events')
def events():
    """Events history page"""
    return render_template('events.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/help')
def help():
    """Help page"""
    return render_template('help.html')

@app.route('/api/status')
def api_status():
    """Get current system status"""
    if not detector:
        return jsonify({
            'status': 'අක්‍රීයයි',
            'status_icon': '⚪',
            'message': 'පද්ධතිය අක්‍රීයයි',
            'camera_status': 'කැමරාව සම්බන්ධ කර නොමැත',
            'sms_status': 'SMS අක්‍රීයයි',
            'alarm_status': 'ඇලම් අක්‍රීයයි'
        })
    
    # Get detector status
    detector_status, detector_message = detector.get_status()
    
    # Get state machine status
    state_info = state_machine.get_current_state()
    status_text, status_icon = state_machine.get_state_display()
    
    # Get SMS status
    sms_status, sms_message = sms_system.get_status()
    
    # Get alarm status
    alarm_status, alarm_message = alarm_system.get_status()
    
    return jsonify({
        'status': status_text,
        'status_icon': status_icon,
        'message': detector_message,
        'camera_status': detector_message,
        'sms_status': sms_status,
        'alarm_status': alarm_status,
        'is_intrusion': state_info['is_intrusion'],
        'intrusion_duration': int(state_info['intrusion_duration'])
    })

@app.route('/api/video_feed')
def video_feed():
    """Video feed endpoint"""
    def generate_frames():
        while True:
            if hasattr(app, 'current_frame') and app.current_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + app.current_frame + b'\r\n')
            else:
                # Send placeholder image
                img = Image.new('RGB', (640, 480), color='black')
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG')
                img_bytes = img_bytes.getvalue()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
            time.sleep(0.1)
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/test_sms', methods=['POST'])
def test_sms():
    """Test SMS functionality"""
    success, message = sms_system.send_test_sms()
    return jsonify({'success': success, 'message': message})

@app.route('/api/test_alarm', methods=['POST'])
def test_alarm():
    """Test alarm functionality"""
    success, message = alarm_system.test_alarm()
    return jsonify({'success': success, 'message': message})

@app.route('/api/stop_alarm', methods=['POST'])
def stop_alarm():
    """Stop alarm manually"""
    success, message = alarm_system.stop_alarm()
    return jsonify({'success': success, 'message': message})

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """Get or update configuration"""
    if request.method == 'GET':
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return jsonify(config_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            new_config = request.json
            
            # Update configuration
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            
            # Update detector config
            if detector:
                detector.load_config('config.json')
            
            # Update SMS system
            if sms_system:
                sms_system.load_config('config.json')
            
            return jsonify({'success': True, 'message': 'වින්‍යාසය යාවත්කාලීන කරන ලදී'})
        
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events')
def api_events():
    """Get events history"""
    try:
        events = []
        if os.path.exists('events/events.csv'):
            import csv
            with open('events/events.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                events = list(reader)
        
        return jsonify(events)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics')
def api_statistics():
    """Get system statistics"""
    try:
        stats = {
            'total_events': 0,
            'today_events': 0,
            'animals_detected': 0,
            'system_uptime': 0,
            'last_detection': 'කිසිවිටක නැත'
        }
        
        # Count events
        if os.path.exists('events/events.csv'):
            import csv
            from datetime import datetime, timedelta
            
            with open('events/events.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                events = list(reader)
                
            stats['total_events'] = len(events)
            
            # Count today's events
            today = datetime.now().strftime('%Y-%m-%d')
            today_events = [e for e in events if e.get('date', '').startswith(today)]
            stats['today_events'] = len(today_events)
            
            # Count animal detections
            animal_events = [e for e in events if 'ඇතුළු වී ඇත' in e.get('status', '')]
            stats['animals_detected'] = len(animal_events)
            
            # Last detection
            if animal_events:
                last_event = animal_events[-1]
                stats['last_detection'] = f"{last_event.get('date', '')} {last_event.get('time', '')}"
        
        # System uptime (simplified)
        if detector and detector.camera and detector.camera.isOpened():
            stats['system_uptime'] = "ක්‍රියාත්මකයි"
        else:
            stats['system_uptime'] = "අක්‍රීයයි"
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload_alarm', methods=['POST'])
def upload_alarm():
    """Upload alarm sound file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'ගොනුව තෝරාගෙන නැත'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'ගොනුව තෝරාගෙන නැත'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename('alert.mp3')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update config
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['alarm_file'] = f'static/{filename}'
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            # Update alarm system
            if alarm_system:
                alarm_system.set_alarm_file(filepath)
            
            return jsonify({'success': True, 'message': f'ඇලම් ගොනුව උඩුගත කරන ලදී: {filename}'})
        else:
            return jsonify({'success': False, 'error': 'අවසර නැති ගොනු වර්ගය'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload_logo', methods=['POST'])
def upload_logo():
    """Upload logo image file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'ගොනුව තෝරාගෙන නැත'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'ගොනුව තෝරාගෙන නැත'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename('logo.png')
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Update config
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['logo_file'] = f'static/{filename}'
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            return jsonify({'success': True, 'message': f'ලෝගෝ ගොනුව උඩුගත කරන ලදී: {filename}'})
        else:
            return jsonify({'success': False, 'error': 'අවසර නැති ගොනු වර්ගය'}), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/start_system', methods=['POST'])
def start_system():
    """Start the monitoring system"""
    global is_running, camera_thread
    
    if is_running:
        return jsonify({'success': False, 'message': 'පද්ධතිය දැනටමත් ක්‍රියාත්මක වේ'})
    
    try:
        initialize_systems()
        is_running = True
        camera_thread = threading.Thread(target=camera_monitoring_loop, daemon=True)
        camera_thread.start()
        
        return jsonify({'success': True, 'message': 'පද්ධතිය ආරම්භ කරන ලදී'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stop_system', methods=['POST'])
def stop_system():
    """Stop the monitoring system"""
    global is_running, detector, alarm_system
    
    try:
        is_running = False
        
        if alarm_system:
            alarm_system.stop_alarm()
        
        if detector:
            detector.release_camera()
        
        return jsonify({'success': True, 'message': 'පද්ධතිය නවතා ඇත'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize systems on startup
    initialize_systems()
    
    # Start monitoring in background
    is_running = True
    camera_thread = threading.Thread(target=camera_monitoring_loop, daemon=True)
    camera_thread.start()
    
    print("Farm Gate Monitor starting...")
    print("Dashboard: http://localhost:5000")
    print("Admin Panel: http://localhost:5000/admin")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
