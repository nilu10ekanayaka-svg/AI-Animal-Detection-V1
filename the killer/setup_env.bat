@echo off
echo ========================================
echo කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය
echo පරිසරය සකසමින්...
echo ========================================

echo.
echo Python ස්ථාපනය පරීක්ෂා කරමින්...
python --version >nul 2>&1
if errorlevel 1 (
    echo දෝෂය: Python ස්ථාපනය කර නැත!
    echo කරුණාකර Python 3.8 හෝ ඉහළ ස්ථාපනය කරන්න
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python සාර්ථකව ස්ථාපනය කර ඇත!

echo.
echo අවශ්‍ය පැකේජ ස්ථාපනය කරමින්...
pip install -r requirements.txt

if errorlevel 1 (
    echo දෝෂය: පැකේජ ස්ථාපනයේදී දෝෂයක් සිදුවිය!
    pause
    exit /b 1
)

echo.
echo ගොනු ව්‍යුහය සකසමින්...
if not exist "static" mkdir static
if not exist "templates" mkdir templates
if not exist "events" mkdir events
if not exist "tests" mkdir tests
if not exist "docs" mkdir docs

echo.
echo .env ගොනුව සකසමින්...
if not exist ".env" (
    echo TWILIO_SID=AK4vaWhaF9b57JG4Ndv9v19D5y7EkcQRwT > .env
    echo TWILIO_AUTH=df22a9bca76020d1701af377e37972e5 >> .env
    echo TWILIO_FROM=+18646629787 >> .env
    echo FARMER_PHONE= >> .env
    echo .env ගොනුව සාදන ලදී
) else (
    echo .env ගොනුව දැනටමත් පවතී
)

echo.
echo පරිසර විචල්‍ය පූරණය කරමින්...
set TWILIO_SID=AK4vaWhaF9b57JG4Ndv9v19D5y7EkcQRwT
set TWILIO_AUTH=df22a9bca76020d1701af377e37972e5
set TWILIO_FROM=+18646629787
set FARMER_PHONE=

echo.
echo නියැදි ගොනු සාදමින්...
if not exist "static\alert.mp3" (
    echo නියැදි ඇලම් ශබ්ද ගොනුව අවශ්‍යයි
    echo කරුණාකර static\alert.mp3 ගොනුව එක් කරන්න
)

if not exist "static\logo.png" (
    echo නියැදි ලෝගෝ ගොනුව අවශ්‍යයි
    echo කරුණාකර static\logo.png ගොනුව එක් කරන්න
)

echo.
echo ========================================
echo ස්ථාපනය සාර්ථකව සම්පූර්ණ විය!
echo ========================================
echo.
echo ඊළඟ පියවර:
echo 1. static\alert.mp3 ඇලම් ශබ්ද ගොනුව එක් කරන්න
echo 2. static\logo.png ලෝගෝ ගොනුව එක් කරන්න
echo 3. .env ගොනුවේ FARMER_PHONE අංකය සකසන්න
echo 4. start.bat ද්විත්ව ක්ලික් කරන්න
echo.
pause
