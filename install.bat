@echo off
title Video Downloader Installer
color 0A
echo.
echo  ================================
echo    Video Downloader Installer
echo  ================================
echo.
pause

echo [1/3] Checking Python...
python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo [OK] Python already installed!
) ELSE (
    echo Installing Python...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python.exe'"
    "%TEMP%\python.exe" /quiet InstallAllUsers=1 PrependPath=1
    echo [OK] Python installed!
)

echo.
echo [2/3] Installing yt-dlp...
pip install yt-dlp --quiet
echo [OK] yt-dlp ready!

echo.
echo [3/3] Installing ffmpeg...
winget install --id Gyan.FFmpeg -e --silent
echo [OK] ffmpeg ready!

echo.
echo  ================================
echo  Everything is installed!
echo  ================================
echo.
set /p LAUNCH="Launch the downloader now? (y/n): "
IF /I "%LAUNCH%"=="y" (
    video_downloader.exe
)
pause