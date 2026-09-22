@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo   小盈工作区 - 新电脑恢复工具
echo ========================================
echo.
echo 本脚本会在新电脑上:
echo 1. 检查 Git 是否安装
echo 2. 从 GitHub 克隆工作区
echo 3. 配置 Agent 工作区
echo.
echo 远程仓库：https://github.com/Hank-zz1/xiaoying-workspace.git
echo.
pause

:: 检查 Git 是否安装
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [错误] Git 未安装！
    echo.
    echo 请先安装 Git:
    echo 1. 访问：https://git-scm.com/download/win
    echo 2. 下载并安装
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo [1/4] Git 已安装，版本信息:
git --version
echo.

:: 获取当前用户名
set USERNAME=%USERNAME%
set WORKSPACE_PATH=C:\Users\%USERNAME%\.incaier-agent\workspaces

echo [2/4] 创建工作区目录...
if not exist "%WORKSPACE_PATH%" (
    mkdir "%WORKSPACE_PATH%"
    echo ✓ 目录已创建：%WORKSPACE_PATH%
) else (
    echo ✓ 目录已存在：%WORKSPACE_PATH%
)
echo.

:: 检查是否已存在工作区
if exist "%WORKSPACE_PATH%\my-workspace\.git" (
    echo [警告] 工作区已存在！
    echo.
    echo 检测到已存在的工作区:
    echo %WORKSPACE_PATH%\my-workspace
    echo.
    echo 选择操作:
    echo 1. 拉取最新数据 (git pull)
    echo 2. 删除并重新克隆
    echo 3. 退出
    echo.
    set /p CHOICE="请输入选择 (1/2/3): "
    
    if "%CHOICE%"=="1" (
        echo.
        echo 正在拉取最新数据...
        cd /d "%WORKSPACE_PATH%\my-workspace"
        git pull
        echo.
        echo ✓ 拉取完成！
        echo.
        goto :success
    )
    
    if "%CHOICE%"=="2" (
        echo.
        echo 正在删除旧工作区...
        rd /s /q "%WORKSPACE_PATH%\my-workspace"
        echo ✓ 已删除
        echo.
        goto :clone
    )
    
    if "%CHOICE%"=="3" (
        echo.
        echo 已退出
        pause
        exit /b
    )
    
    echo.
    echo 无效选择
    pause
    exit /b 1
)

:clone
echo [3/4] 从 GitHub 克隆工作区...
echo.
echo 远程仓库：https://github.com/Hank-zz1/xiaoying-workspace.git
echo 目标位置：%WORKSPACE_PATH%\my-workspace
echo.
echo 注意:
echo - 首次克隆可能需要较长时间 (约 300MB 数据)
echo - 请确保网络连接稳定
echo - 可能需要 GitHub 账号认证
echo.
set /p CONFIRM="确认克隆？(Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo.
    echo 已取消
    pause
    exit /b
)

cd /d "%WORKSPACE_PATH%"
git clone https://github.com/Hank-zz1/xiaoying-workspace.git my-workspace

if %errorlevel% neq 0 (
    echo.
    echo [错误] 克隆失败！
    echo.
    echo 可能原因:
    echo 1. 网络问题 - 检查网络连接或使用代理/VPN
    echo 2. 仓库不存在 - 请先在当前电脑推送数据
    echo 3. 认证失败 - 检查 GitHub 账号密码
    echo.
    echo 解决方案:
    echo - 使用 GitHub Desktop: https://desktop.github.com/
    echo - 手动克隆: git clone https://github.com/Hank-zz1/xiaoying-workspace.git
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ 克隆成功！
echo.

:success
echo [4/4] 配置完成检查...
echo.
cd /d "%WORKSPACE_PATH%\my-workspace"

echo 工作区信息:
echo - 路径：%WORKSPACE_PATH%\my-workspace
echo - Git 分支: 
git branch
echo - 最后提交:
git log --oneline -1
echo.

:: 统计文件
for /f "tokens=*" %%i in ('dir /b /s ^| find /c /v ""') do set FILE_COUNT=%%i
echo - 文件总数：%FILE_COUNT% 个

echo.
echo ========================================
echo   恢复完成！
echo ========================================
echo.
echo 下一步:
echo 1. 打开小盈 Agent
echo 2. 设置 → 工作区 → 打开现有工作区
echo 3. 选择：%WORKSPACE_PATH%\my-workspace
echo 4. 重启 Agent
echo.
echo 验证数据:
echo - 历史会话：应该显示 285 个
echo - 技能列表：应该显示 197 个
echo - 定时任务：应该显示 6 个
echo - 长期记忆：应该显示 370+ 条
echo.
echo 如需日常同步，运行:
echo   git pull    (拉取更新)
echo   git push    (推送更改)
echo.
echo 详细指南请查看:
echo   跨机器同步指南.md
echo.
pause
