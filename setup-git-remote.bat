@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   设置 Git 远程仓库
echo ========================================
echo.

cd /d "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"

set /p REPO_URL="请输入远程仓库地址 (HTTPS 或 SSH): "
echo.
echo 正在设置远程仓库 %REPO_URL%...
echo.

git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo ✓ 远程仓库已添加
echo.

echo 当前远程仓库:
git remote -v
echo.

echo ========================================
echo 下一步:
echo ========================================
echo.
echo 1. 推送到远程仓库:
echo    git push -u origin main
echo.
echo 2. 如果遇到分支名称问题，使用:
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
pause
