@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   小盈工作区 Git 同步设置向导
echo ========================================
echo.

cd /d "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"

echo 步骤 1/5: 初始化 Git 仓库...
if not exist .git (
    git init
    echo ✓ Git 仓库初始化完成
) else (
    echo ✓ Git 仓库已存在
)
echo.

echo 步骤 2/5: 创建 .gitignore 文件...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo env/
echo venv/
echo ENV/
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Node
echo node_modules/
echo npm-debug.log
echo yarn-error.log
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo Desktop.ini
echo.
echo # Logs
echo *.log
echo logs/
echo.
echo # Temporary files
echo *.tmp
echo *.temp
echo.
echo # Backup files
echo *.bak
echo *.backup
echo.
echo # 大型数据文件 (可选)
echo # sessions/*/data/*
echo # sessions/*/attachments/*
echo # data/
) > .gitignore
echo ✓ .gitignore 创建完成
echo.

echo 步骤 3/5: 检查 Git 状态...
git status --short
echo.

echo 步骤 4/5: 添加所有文件...
git add -A
echo ✓ 文件已添加到暂存区
echo.

echo 步骤 5/5: 首次提交...
git commit -m "Initial commit: 小盈工作区数据"
echo ✓ 首次提交完成
echo.

echo ========================================
echo   Git 初始化完成！
echo ========================================
echo.
echo 下一步操作:
echo.
echo 1️⃣  在 GitHub/Gitee 创建新仓库 (不要勾选"初始化 README")
echo.
echo 2️⃣  创建后复制仓库地址，例如:
echo    https://github.com/yourname/xiaoying-workspace.git
echo    或 git@github.com:yourname/xiaoying-workspace.git
echo.
echo 3️⃣  运行设置远程仓库脚本:
echo    setup-git-remote.bat
echo.
echo 4️⃣  推送数据到远程仓库:
echo    git push -u origin main
echo.
echo ========================================
pause
