# කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය - ස්ථාපන මාර්ගෝපදේශය
# Farm Gate Monitor System - Setup Guide

## 🚀 ඉක්මන් ආරම්භය (Quick Start)

### පියවර 1: පරිසරය සකසන්න
```bash
setup_env.bat ද්විත්ව ක්ලික් කරන්න
```

### පියවර 2: සැකසුම් සකසන්න
1. `.env` ගොනුවේ `FARMER_PHONE` අංකය සකසන්න
2. `static/alert.mp3` ඇලම් ශබ්ද ගොනුව එක් කරන්න
3. `static/logo.png` ලෝගෝ ගොනුව එක් කරන්න

### පියවර 3: පද්ධතිය ආරම්භ කරන්න
```bash
start.bat ද්විත්ව ක්ලික් කරන්න
```

### පියවර 4: බ්‍රවුසරය විවෘත කරන්න
- Dashboard: http://localhost:5000
- Admin Panel: http://localhost:5000/admin
- Events: http://localhost:5000/events

## 📋 විස්තරාත්මක ස්ථාපනය

### අවශ්‍යතා
- Windows 10/11
- Python 3.8+ 
- Webcam/Camera
- අන්තර්ජාල සම්බන්ධතාවය

### Python ස්ථාපනය
1. https://www.python.org/downloads/ වෙත යන්න
2. Python 3.8+ බාගත කර ස්ථාපනය කරන්න
3. "Add Python to PATH" තේරීමට වග බලා ගන්න

### පැකේජ ස්ථාපනය
```bash
pip install -r requirements.txt
```

### වින්‍යාසය

#### .env ගොනුව
```env
TWILIO_SID=AK4vaWhaF9b57JG4Ndv9v19D5y7EkcQRwT
TWILIO_AUTH=df22a9bca76020d1701af377e37972e5
TWILIO_FROM=+18646629787
FARMER_PHONE=+94771234567
```

#### config.json
```json
{
    "min_area": 1000,
    "detection_frames": 5,
    "farmer_phone": "+94771234567",
    "alarm_file": "static/alert.mp3",
    "logo_file": "static/logo.png",
    "camera_index": 0,
    "detection_enabled": true,
    "sms_enabled": true
}
```

## 🔧 පරීක්ෂා කිරීම

### පද්ධති පරීක්ෂා
```bash
python tests/test_system.py
```

### නිදර්ශන ධාවනය
```bash
python demo.py
```

## 🐛 ගැටලු විසඳීම

### කැමරා සම්බන්ධ නොවේ
- USB කැමරා සම්බන්ධතාවය පරීක්ෂා කරන්න
- `config.json` හි `camera_index` වෙනස් කරන්න (0, 1, 2...)
- වෙනත් කැමරා යෙදුම් වසා තබන්න

### SMS නොවැඩේ
- `.env` ගොනුවේ Twilio credentials පරීක්ෂා කරන්න
- දුරකථන අංකය ජාත්‍යන්තර ආකාරයෙන් ඇතුළත් කර ඇත්ද පරීක්ෂා කරන්න
- Twilio ගිණුමේ ධාරාව පරීක්ෂා කරන්න

### ඇලම් නොවැඩේ
- `static/alert.mp3` ගොනුව පවතීද පරීක්ෂා කරන්න
- ශබ්ද පරිමාව පරීක්ෂා කරන්න
- pygame ස්ථාපනය කර ඇත්ද පරීක්ෂා කරන්න

### Python දෝෂ
- Python 3.8+ ස්ථාපනය කර ඇත්ද පරීක්ෂා කරන්න
- pip යාවත්කාලීන කරන්න: `python -m pip install --upgrade pip`
- සියලුම පැකේජ නැවත ස්ථාපනය කරන්න: `pip install -r requirements.txt --force-reinstall`

## 📱 Mobile භාවිතය

පද්ධතිය mobile-friendly වන අතර කර්මිකාරයාගේ දුරකථන browser හි වැඩ කරයි:

1. දුරකථනයේ බ්‍රවුසරය විවෘත කරන්න
2. http://[computer-ip]:5000 වෙත යන්න
3. Dashboard භාවිතා කරන්න

## 🔒 ආරක්ෂාව

- Twilio credentials ආරක්ෂිතව තබා ගන්න
- .env ගොනුව version control හි ඇතුළත් නොකරන්න
- නිතර password වෙනස් කරන්න

## 📞 සහාය

ගැටලු සඳහා:
1. `events/events.csv` ගොනුව පරීක්ෂා කරන්න
2. Console logs පරීක්ෂා කරන්න
3. Admin Panel හි සැකසුම් පරීක්ෂා කරන්න
4. Test scripts ධාවනය කරන්න

---

**සාර්ථක ස්ථාපනය!** 🎉
