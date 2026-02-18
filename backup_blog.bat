@echo off
setlocal
set "SOURCE_DIR=%~dp0"
set "BACKUP_DIR=D:\Blog_Backups" :: 외장하드 경로로 수정 필요
set "TIMESTAMP=%date:~0,4%-%date:~5,2%-%date:~8,2%_%time:~0,2%-%time:~3,2%"

echo [INFO] Pulling latest changes from GitHub...
git pull origin main

echo [INFO] Starting backup for %SOURCE_DIR%...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

powershell -Command "Compress-Archive -Path '%SOURCE_DIR%' -DestinationPath '%BACKUP_DIR%\Blog_Backup_%TIMESTAMP%.zip' -Force"

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Backup completed: %BACKUP_DIR%\Blog_Backup_%TIMESTAMP%.zip
) else (
    echo [ERROR] Backup failed.
)
pause
