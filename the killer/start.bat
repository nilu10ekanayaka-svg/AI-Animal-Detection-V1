@echo off
echo ========================================
echo කර්මිකාරයාගේ වත්තේ ආරක්ෂක පද්ධතිය
echo පද්ධතිය ආරම්භ කරමින්...
echo ========================================

echo.
echo පරිසරය පරීක්ෂා කරමින්...
if not exist "requirements.txt" (
    echo දෝෂය: requirements.txt ගොනුව හමු නොවීය!
    echo කරුණාකර setup_env.bat පළමුව ධාවනය කරන්න
    pause
    exit /b 1
)

echo.
echo Python පැකේජ පරීක්ෂා කරමින්...
python -c "import cv2, flask, twilio" >nul 2>&1
if errorlevel 1 (
    echo දෝෂය: අවශ්‍ය පැකේජ ස්ථාපනය කර නැත!
    echo කරුණාකර setup_env.bat ධාවනය කරන්න
    pause
    exit /b 1
)

echo.
echo පද්ධතිය ආරම්භ කරමින්...
echo අන්තර්ජාල බ්‍රවුසරය ස්වයංක්‍රීයව විවෘත වේ...
echo.

REM Start the Flask application
python app.py

echo.
echo පද්ධතිය නවතා ඇත
pause
