@echo off
title BLACKOUT launcher
cd /d "%~dp0"

REM 1) Ollama: start the background service if it is not already running
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I "ollama.exe" >NUL
if errorlevel 1 (
    start "" /min ollama serve
    timeout /t 3 /nobreak >NUL
)

REM 2) Page server: start it minimized if port 8080 is not already in use
netstat -ano | find ":8080 " | find "LISTENING" >NUL
if errorlevel 1 (
    start "BLACKOUT server" /min "%USERPROFILE%\miniconda3\python.exe" -m http.server 8080
    timeout /t 2 /nobreak >NUL
)

REM 3) Open BLACKOUT in its own app window (no tabs, no address bar)
start "" msedge --app=http://localhost:8080 --window-size=1400,900
exit
