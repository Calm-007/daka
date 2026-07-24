@echo off
cd /d "%~dp0"
echo 局域网模式 (手机可访问)
echo 电脑: http://localhost:8765
echo 手机: http://192.168.1.8:8765
echo.
python -m http.server 8765 --bind 0.0.0.0
pause
