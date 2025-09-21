# SMS Setup Guide - කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය

## SMS සැකසුම් මාර්ගෝපදේශය

### Twilio ගිණුමක් සාදා ගැනීම

1. **Twilio වෙබ් අඩවියට යන්න**: https://www.twilio.com
2. **නොමිලේ ගිණුමක් සාදා ගන්න**
3. **දුරකථන අංකයක් මිල දී ගන්න** (මාසික $1 පමණ)

### Twilio අක්ෂර සංකේත ලබා ගැනීම

1. Twilio Dashboard හි **Account SID** සහ **Auth Token** සොයා ගන්න
2. **Phone Numbers** කොටසෙන් ඔබේ Twilio දුරකථන අංකය සොයා ගන්න

### config.json ගොනුව යාවත්කාලීන කිරීම

`config.json` ගොනුවේ පහත අගයන් යාවත්කාලීන කරන්න:

```json
{
    "farmer_phone": "+94771234567",
    "twilio_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "twilio_auth": "your_auth_token_here",
    "twilio_from": "+1234567890"
}
```

### පරීක්ෂා කිරීම

1. යෙදුම ආරම්භ කරන්න: `python app.py`
2. වෙබ් අතුරුමුහුණත වෙත යන්න: http://localhost:5000
3. **SMS පරීක්ෂා** බොත්තම ක්ලික් කරන්න

### වැදගත් සටහන්

- **farmer_phone**: ඔබේ සැබෑ දුරකථන අංකය (ජාත්‍යන්තර ආකාරයෙන්)
- **twilio_sid**: Twilio Account SID
- **twilio_auth**: Twilio Auth Token
- **twilio_from**: Twilio වෙතින් ලබා ගත් දුරකථන අංකය

### දෝෂ නිරාකරණය

**"SMS අක්‍රීයයි"** පණිවිඩය දක්නට ලැබුණහොත්:
1. Twilio අක්ෂර සංකේත නිවැරදිදැයි පරීක්ෂා කරන්න
2. දුරකථන අංකයන් නිවැරදි ආකාරයෙන් ඇතුළත් කර ඇත්දැයි පරීක්ෂා කරන්න
3. Twilio ගිණුමේ මුදල් ඇතිදැයි පරීක්ෂා කරන්න

### ආරක්ෂාව

- Twilio Auth Token කිසිවිටක වෙබ් අඩවියක හෝ පොදු ස්ථානයක තබන්න එපා
- config.json ගොනුව ආරක්ෂිතව තබන්න