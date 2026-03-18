@echo off
REM Default backup destination requested by user: "D:\lovetok backup"
set "DEST=D:\lovetok backup"

echo Backing up project to: "%DEST%"
powershell -ExecutionPolicy Bypass -File "c:\Users\Admin\shorts\smart_backup.ps1" -SourcePath "c:\Users\Admin\shorts" -DestinationPath "%DEST%"
pause
