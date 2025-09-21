# 🚀 කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය
# 🐄 Farm Security System with AI Animal Detection

**Advanced AI-powered animal detection system with automatic SMS alerts, sound alarms, and beautiful web interface for comprehensive farm security monitoring.**

## ✨ ප්‍රධාන විශේෂාංග / Key Features

- 🤖 **AI Animal Detection**: Advanced computer vision to detect animals vs humans
- 📱 **SMS Alerts**: Automatic SMS notifications via Twilio when animals are detected  
- 🔊 **Sound Alarms**: Customizable alarm sounds with automatic playback
- 📹 **Live Camera Feed**: HD camera monitoring with real-time animal labeling
- 🌐 **Beautiful Web Interface**: Modern, responsive web dashboard
- 📊 **Statistics Dashboard**: Real-time statistics and event tracking
- 📱 **Mobile Friendly**: Works on phones, tablets, and computers
- 🎯 **Animal Names**: Animals are automatically labeled with Sinhala names
- 📈 **Event History**: Complete log of all detection events
- ⚙️ **Easy Configuration**: Simple web-based configuration panel

## 🌟 ප්‍රධාන විශේෂාංග

### 1. සතුන් අනාවරණය
- OpenCV BackgroundSubtractorMOG2 භාවිතය
- AI-පුහුණු අධිපතනය (මිනිසුන්/ගස් නොසලකා හරිනු, සතුන් පමණක් අනාවරණය)
- ENTER/EXIT සිදුවීම් සඳහා state machine
- වින්‍යාස කළ හැකි thresholds

### 2. සිංහල SMS ඇලර්ට් (Twilio)
- සිංහල භාෂාවෙන් පමණක් පණිවිඩ
- ඇතුළු වීම: "ඔබේ වත්තට සතුන් ඇතුළු වී ඇත. කරුණාකර පරීක්ෂා කරන්න."
- පිටවීම: "සතුන් වත්තෙන් පිටවී ගොස් ඇත."
- Twilio නොමැති විට graceful degradation

### 3. ඇලම් පද්ධතිය
- alert.mp3 ලූප් කරන ඇලම්
- සතුන් පිටවන තෙක් වාදනය
- පසුබිම් thread හි ධාවනය
- පරීක්ෂා බොත්තම්

### 4. වෙබ් ඩෑෂ්බෝඩ් (සිංහල UI)
- Flask app සහිත mobile-friendly UI
- සජීවී කැමරා stream + පද්ධති status
- Status Badge:
  - 🟢 "සුරක්ෂිතයි" (Safe)
  - 🔴 "ඇතුළු වී ඇත" (Intrusion)
  - ⚪ "අක්‍රීයයි" (Offline)
- කර්මිකාර බොත්තම්: Test SMS, Test Alarm
- අවසන් සිදුවීම + කාලය පෙන්වයි

### 5. පහසු Admin Panel
- SMS දුරකථන අංකය වෙනස් කිරීම
- Thresholds සකස් කිරීම (MIN_AREA, detection frames)
- ඇලම් ශබ්ද උඩුගත කිරීම/වෙනස් කිරීම
- ලෝගෝ උඩුගත කිරීම/වෙනස් කිරීම
- සියලුම labels සිංහලෙන්

### 6. සිදුවීම් ලොගිං
- සියලුම ENTER/EXIT සිදුවීම් events.csv හි ලොග්
- සිදුවීම් පිටුව සිංහලෙන් ඉතිහාසය පෙන්වයි

### 7. එක්-ක්ලික් ස්ථාපනය
- setup_env.bat → Python deps ස්වයංක්‍රීයව ස්ථාපනය
- start.bat → Flask + ස්වයංක්‍රීය browser විවෘත කිරීම
- කර්මිකාරයන්ට ද්විත්ව ක්ලික් පමණක්, terminal typing නැත

### 8. පරිශීලක-හිතකාමී UI
- සිංහල සෑම තැනකම
- විශාල බොත්තම් + ඉහළ contrast (කොළ = සුරක්ෂිත, රතු = ඇලර්ට්)
- Mobile-friendly (කර්මිකාර දුරකථන browser වැඩ කරයි)

### 9. දෝෂ-නිදොස් ගැරන්ටි
- කැමරා නැත → ඩෑෂ්බෝඩ් "කැමරාව සම්බන්ධ කර නොමැත" පෙන්වයි
- Twilio නැත → "SMS අක්‍රීයයි" පෙන්වයි
- පැහැදිලිව logs මුද්‍රණය

## 🛠️ ස්ථාපනය

### අවශ්‍යතා
- Python 3.8 හෝ ඉහළ
- Windows 10/11
- Webcam/Camera
- අන්තර්ජාල සම්බන්ධතාවය (SMS සඳහා)

### ස්ථාපන පියවර

1. **පරිසරය සකසන්න**
   ```bash
   setup_env.bat ද්විත්ව ක්ලික් කරන්න
   ```

2. **සැකසුම් සකසන්න**
   - `.env` ගොනුවේ `FARMER_PHONE` අංකය සකසන්න
   - `static/alert.mp3` ඇලම් ශබ්ද ගොනුව එක් කරන්න
   - `static/logo.png` ලෝගෝ ගොනුව එක් කරන්න

3. **පද්ධතිය ආරම්භ කරන්න**
   ```bash
   start.bat ද්විත්ව ක්ලික් කරන්න
   ```

4. **බ්‍රවුසරය විවෘත කරන්න**
   - Dashboard: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin
   - Events: http://localhost:5000/events

## 📁 පද්ධති ව්‍යුහය

```
farm-gate-monitor/
├── app.py                 # Main Flask application
├── detector.py            # Animal detection system
├── state_machine.py       # ENTER/EXIT state management
├── sms_system.py          # Twilio SMS alerts
├── alarm_system.py        # Audio alarm system
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── setup_env.bat          # One-click setup
├── start.bat              # One-click startup
├── static/                # Static files
│   ├── alert.mp3         # Alarm sound file
│   └── logo.png          # Logo image
├── templates/             # HTML templates
│   ├── dashboard.html     # Main dashboard
│   ├── admin.html         # Admin panel
│   └── events.html        # Events history
├── events/                # Event logs
│   └── events.csv         # CSV event log
└── docs/                  # Documentation
```

## 🔧 වින්‍යාසය

### config.json
```json
{
    "min_area": 1000,           // Minimum area for detection
    "detection_frames": 5,       // Frames needed for detection
    "farmer_phone": "",          // Farmer's phone number
    "alarm_file": "static/alert.mp3",
    "logo_file": "static/logo.png",
    "camera_index": 0,           // Camera device index
    "detection_enabled": true,   // Enable/disable detection
    "sms_enabled": true          // Enable/disable SMS
}
```

### .env
```env
TWILIO_SID=your_twilio_sid
TWILIO_AUTH=your_twilio_auth
TWILIO_FROM=your_twilio_number
FARMER_PHONE=your_farmer_phone
```

## 🚀 භාවිතය

1. **පද්ධතිය ආරම්භ කරන්න**: `start.bat` ද්විත්ව ක්ලික්
2. **ඩෑෂ්බෝඩ් විවෘත කරන්න**: http://localhost:5000
3. **Admin Panel විවෘත කරන්න**: http://localhost:5000/admin
4. **SMS දුරකථන අංකය සකසන්න**: Admin Panel හි
5. **අනාවරණ සැකසුම් සකසන්න**: MIN_AREA, detection frames
6. **පරීක්ෂා කරන්න**: SMS සහ ඇලම් පරීක්ෂා බොත්තම්

## 📱 Mobile Support

පද්ධතිය mobile-friendly වන අතර කර්මිකාරයාගේ දුරකථන browser හි වැඩ කරයි.

## 🔍 Troubleshooting

### කැමරා සම්බන්ධ නොවේ
- කැමරා USB සම්බන්ධතාවය පරීක්ෂා කරන්න
- `config.json` හි `camera_index` වෙනස් කරන්න (0, 1, 2...)

### SMS නොවැඩේ
- `.env` ගොනුවේ Twilio credentials පරීක්ෂා කරන්න
- දුරකථන අංකය ජාත්‍යන්තර ආකාරයෙන් ඇතුළත් කර ඇත්ද පරීක්ෂා කරන්න

### ඇලම් නොවැඩේ
- `static/alert.mp3` ගොනුව පවතීද පරීක්ෂා කරන්න
- ශබ්ද පරිමාව පරීක්ෂා කරන්න

## 📞 සහාය

පද්ධතියේ ගැටලු සඳහා:
1. `events/events.csv` ගොනුව පරීක්ෂා කරන්න
2. Console logs පරීක්ෂා කරන්න
3. Admin Panel හි සැකසුම් පරීක්ෂා කරන්න

## 🎉 Hackathon Quality Features

- ✅ සිංහල + ඉංග්‍රීසි README
- ✅ Dashboard screenshots
- ✅ Clean, bold UI
- ✅ One-click setup
- ✅ Error-free operation
- ✅ Mobile-friendly design
- ✅ Real-time monitoring
- ✅ Professional logging

---

**කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය** - AI බලයෙන් යුත් ස්වයංක්‍රීය ආරක්ෂාව!
#   A I - a n i m a l - d e t e c t i o n  
 #   A I - a n i m a l - d e t e c t i o n  
 