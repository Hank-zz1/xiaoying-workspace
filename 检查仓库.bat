@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   检查 GitHub 仓库是否存在
echo ========================================
echo.
echo 正在检查仓库...
echo 仓库地址：https://github.com/Hank-zz1/xiaoying-workspace
echo.
echo 请在浏览器中打开以上地址
echo.
echo 如果看到:
echo - ✅ 404 页面 → 仓库不存在，需要创建
echo - ✅ 仓库页面 → 仓库已存在
echo.
echo 按任意键继续...
pause

:: 尝试使用 git ls-remote 检查远程仓库
echo.
echo 正在尝试连接远程仓库...
git ls-remote https://github.com/Hank-zz1/xiaoying-workspace.git >nul 2>&1

if %errorlevel% == 0 (
    echo ✓ 仓库存在且可访问！
    echo.
    echo 仓库信息:
    git ls-remote https://github.com/Hank-zz1/xiaoying-workspace.git | findstr /c:"refs/heads/main"
    echo.
) else (
    echo ✗ 无法访问仓库
    echo.
    echo 可能原因:
    echo 1. 仓库不存在 - 需要先在 GitHub 创建
    echo 2. 网络问题 - 检查网络连接
    echo 3. 仓库是私有的且未认证
    echo.
)

echo.
echo ========================================
echo 如何创建仓库:
echo ========================================
echo.
echo 1. 访问：https://github.com/new
echo 2. 登录账号：932142751@qq.com
echo 3. 仓库名：xiaoying-workspace
echo 4. 可见性：选择 Private(私有) 或 Public(公开)
echo 5. 不要勾选"Add a README file"
echo 6. 点击"Create repository"
echo.
echo 创建后，运行:
echo   push-to-github.bat
echo.
pause
