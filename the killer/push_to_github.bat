@echo off
echo Pushing AI Animal Detection project to GitHub...
echo.
echo This will push your project to: https://github.com/nilu10ekanayaka-svg/AI-animal-detection.git
echo.
echo If prompted for authentication:
echo - Username: nilu10ekanayaka-svg
echo - Password: Use your GitHub Personal Access Token (not your GitHub password)
echo.
echo To get a Personal Access Token:
echo 1. Go to GitHub.com
echo 2. Settings > Developer settings > Personal access tokens > Tokens (classic)
echo 3. Generate new token with 'repo' permissions
echo.
pause
git push -u origin master
pause
