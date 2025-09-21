@echo off
echo ========================================
echo AI Animal Detection - GitHub Push Tool
echo ========================================
echo.
echo This will push your project to GitHub
echo Repository: https://github.com/nilu10ekanayaka-svg/AI-animal-detection.git
echo.
echo Make sure you are signed into GitHub in your browser!
echo.
pause
echo.
echo Adding all files...
git add .
echo.
echo Committing changes...
git commit -m "Complete AI Animal Detection System - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
echo.
echo Pushing to GitHub...
git push --force origin main
echo.
echo ========================================
echo Push completed! Check your repository:
echo https://github.com/nilu10ekanayaka-svg/AI-animal-detection
echo ========================================
pause
