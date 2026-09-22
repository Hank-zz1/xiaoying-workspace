@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   一键推送数据到 GitHub
echo ========================================
echo.
echo 本脚本会自动:
echo 1. 打开 GitHub 创建仓库页面
echo 2. 等待你登录并创建仓库
echo 3. 自动推送所有数据
echo.
echo 远程仓库名：xiaoying-workspace
echo 账号：932142751@qq.com
echo.
pause

:: 步骤 1: 打开 GitHub
echo [步骤 1/3] 打开 GitHub 创建页面...
start https://github.com/new
echo.
echo 请在浏览器中:
echo 1. 登录账号：932142751@qq.com
echo 2. 仓库名：xiaoying-workspace
echo 3. 可见性：选择 Private (私有)
echo 4. 不要勾选 "Add a README file"
echo 5. 点击 "Create repository"
echo.
set /p DONE="完成后按回车继续... "

:: 步骤 2: 验证仓库
echo.
echo [步骤 2/3] 验证仓库是否创建成功...
cd /d "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"

git ls-remote https://github.com/Hank-zz1/xiaoying-workspace.git >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo [警告] 无法连接到仓库
    echo 可能原因:
    echo 1. 仓库还未创建成功
    echo 2. 网络问题
    echo.
    echo 请确认:
    echo - 已在 GitHub 创建仓库
    echo - 仓库名：xiaoying-workspace
    echo - 用户名：Hank-zz1
    echo.
    set /p RETRY="是否重试？(Y/N): "
    if /i "%RETRY%"=="Y" goto :0
    pause
    exit /b 1
)

echo ✓ 仓库已存在且可访问
echo.

:: 步骤 3: 推送
echo [步骤 3/3] 推送数据到 GitHub...
echo.
echo 数据量：2,490 个文件，约 300-500MB
echo 预计时间：5-15 分钟（取决于网络）
echo.
echo 推送过程中 Windows 会弹出登录窗口
echo 输入 GitHub 账号密码即可
echo.
pause

git push -u origin main

echo.
if %errorlevel% == 0 (
    echo ========================================
    echo   ✅ 推送成功！
    echo ========================================
    echo.
    echo 你的工作区已同步到:
    echo https://github.com/Hank-zz1/xiaoying-workspace
    echo.
    echo 下一步:
    echo 1. 访问以上网址验证
    echo 2. 在新电脑运行 新电脑恢复.bat
    echo.
) else (
    echo ========================================
    echo   ❌ 推送失败
    echo ========================================
    echo.
    echo 可能原因:
    echo 1. 账号密码错误
    echo 2. 网络问题
    echo 3. 仓库不存在
    echo.
    echo 建议:
    echo 1. 使用 GitHub Desktop: https://desktop.github.com/
    echo 2. 检查网络连接
    echo 3. 查看 推送 GitHub 指南.md
    echo.
)

pause
