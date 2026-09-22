@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   推送到 GitHub
echo ========================================
echo.
echo 请输入你的 GitHub 用户名 (不是邮箱):
echo 例如：zhangsan
echo.
set /p USERNAME=GitHub 用户名：

if "%USERNAME%"=="" (
    echo ❌ 用户名不能为空
    pause
    exit /b
)

set REPO_URL=https://github.com/%USERNAME%/xiaoying-workspace.git

echo.
echo 正在设置远程仓库...
echo 仓库地址：%REPO_URL%
echo.

cd /d "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"

git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo ✓ 远程仓库已设置
echo.

echo 正在设置主分支...
git branch -M main

echo ✓ 主分支已设置
echo.

echo ========================================
echo 准备推送数据到 GitHub
echo ========================================
echo.
echo 仓库：%REPO_URL%
echo.
echo 注意:
echo 1. 如果是第一次推送，会弹出 GitHub 登录窗口
echo 2. 使用你的 GitHub 账号 (932142751@qq.com) 登录
echo 3. 如果开启了两因素认证，可能需要使用 Personal Access Token
echo.
echo 按任意键开始推送...
pause

git push -u origin main

echo.
if %errorlevel% == 0 (
    echo ========================================
    echo   ✅ 推送成功！
    echo ========================================
    echo.
    echo 你的工作区已同步到:
    echo %REPO_URL%
    echo.
) else (
    echo ========================================
    echo   ❌ 推送失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 仓库不存在 - 请先在 GitHub 创建仓库
    echo 2. 认证失败 - 检查账号密码或使用 Token
    echo 3. 网络问题 - 检查网络连接
    echo.
)

pause
