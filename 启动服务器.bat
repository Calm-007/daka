@echo off
cd /d "%~dp0"
echo 本地模式 (仅本机可访问)
echo 地址: http://localhost:8765
echo.
python -m http.server 8765 --bind 127.0.0.1
pause
