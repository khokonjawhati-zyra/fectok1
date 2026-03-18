@echo off
set "ROOT=C:\Users\Admin\backup 3"
cd /d "%ROOT%\sovereign_media_hub\uplink"
start /min cmd /c "python uplink_server.py > uplink.log 2>&1"
cd /d "%ROOT%\backend"
start /min cmd /c "python -m uvicorn main:app --host 0.0.0.0 --port 5000 > backend.log 2>&1"
cd /d "%ROOT%\admin_panel\build\web"
start /min python -m http.server 9090
cd /d "%ROOT%\user_panel\build\web"
start /min python -m http.server 8181
exit
