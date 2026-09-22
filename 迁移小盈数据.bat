@echo off
chcp 65001 >nul
echo ========================================
echo   小盈历史对话数据迁移工具
echo ========================================
echo.

set WORKSPACE=C:\Users\26011970\.incaier-agent\workspaces\my-workspace
set BACKUP_DIR=C:\Users\26011970\Desktop\小盈数据备份
set TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_NAME=小盈数据备份_%TIMESTAMP%

echo 正在准备备份...
echo 工作区路径：%WORKSPACE%
echo 备份目标：%BACKUP_DIR%\%BACKUP_NAME%
echo.

:: 创建备份目录
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: 复制核心数据
echo [1/5] 复制历史对话数据 (sessions)...
xcopy /E /I /Q /Y "%WORKSPACE%\sessions" "%BACKUP_DIR%\%BACKUP_NAME%\sessions" >nul

echo [2/5] 复制工作区配置...
xcopy /Q /Y "%WORKSPACE%\config.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul
xcopy /Q /Y "%WORKSPACE%\automations.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul
xcopy /Q /Y "%WORKSPACE%\skill-registry.json" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul

echo [3/5] 复制长期记忆...
xcopy /E /I /Q /Y "%WORKSPACE%\memory" "%BACKUP_DIR%\%BACKUP_NAME%\memory" >nul

echo [4/5] 复制自定义技能...
xcopy /E /I /Q /Y "%WORKSPACE%\skills" "%BACKUP_DIR%\%BACKUP_NAME%\skills" >nul
xcopy /E /I /Q /Y "%WORKSPACE%\skills-dev" "%BACKUP_DIR%\%BACKUP_NAME%\skills-dev" >nul

echo [5/5] 复制数据源配置...
xcopy /E /I /Q /Y "%WORKSPACE%\sources" "%BACKUP_DIR%\%BACKUP_NAME%\sources" >nul

:: 复制迁移指南
xcopy /Q /Y "%WORKSPACE%\小盈数据迁移指南.md" "%BACKUP_DIR%\%BACKUP_NAME%\" >nul

echo.
echo ========================================
echo   备份完成!
echo ========================================
echo.
echo 备份位置: %BACKUP_DIR%\%BACKUP_NAME%
echo.
echo 下一步:
echo 1. 将备份文件夹复制到新机器
echo 2. 在新机器上安装小盈 Agent
echo 3. 按照《小盈数据迁移指南.md》还原数据
echo.
pause
