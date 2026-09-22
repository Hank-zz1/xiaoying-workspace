@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   Xiaoying Data Migration Tool
echo ========================================
echo.

set WORKSPACE=C:\Users\26011970\.incaier-agent\workspaces\my-workspace
set BACKUP_DIR=C:\Users\26011970\Desktop\xiaoying_backup
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_NAME=xiaoying_data_%TIMESTAMP%

echo Preparing backup...
echo Workspace: %WORKSPACE%
echo Backup to: %BACKUP_DIR%\%BACKUP_NAME%
echo.

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo [1/6] Copying sessions...
xcopy /E /I /Q /Y "%WORKSPACE%\sessions" "%BACKUP_DIR%\%BACKUP_NAME%\sessions"

echo [2/6] Copying config files...
copy /Y "%WORKSPACE%\config.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul
copy /Y "%WORKSPACE%\automations.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul
copy /Y "%WORKSPACE%\skill-registry.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul

echo [3/6] Copying memory...
xcopy /E /I /Q /Y "%WORKSPACE%\memory" "%BACKUP_DIR%\%BACKUP_NAME%\memory"

echo [4/6] Copying skills...
xcopy /E /I /Q /Y "%WORKSPACE%\skills" "%BACKUP_DIR%\%BACKUP_NAME%\skills"
xcopy /E /I /Q /Y "%WORKSPACE%\skills-dev" "%BACKUP_DIR%\%BACKUP_NAME%\skills-dev"

echo [5/6] Copying sources...
xcopy /E /I /Q /Y "%WORKSPACE%\sources" "%BACKUP_DIR%\%BACKUP_NAME%\sources"

echo [6/6] Copying migration guide...
copy /Y "%WORKSPACE%\小盈数据迁移指南.md" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul

echo.
echo ========================================
echo   Backup completed!
echo ========================================
echo.
echo Backup location: %BACKUP_DIR%\%BACKUP_NAME%
echo.
echo Next steps:
echo 1. Copy the backup folder to new machine
echo 2. Install Xiaoying Agent on new machine
echo 3. Follow the migration guide to restore
echo.
pause
