@echo off
chcp 65001 >nul 2>&1
color 0A
echo ========================================
echo   小盈工作区 - GitHub 同步向导
echo ========================================
echo.
echo 欢迎使用 Git 同步！
echo.
echo 本工具会帮你:
echo ✓ 打开 GitHub 创建仓库
echo ✓ 自动推送所有数据到云端
echo ✓ 为多设备同步做好准备
echo.
echo 数据量：2,490 个文件 (约 300-500MB)
echo 包含：285 个会话、197 个技能、6 个定时任务
echo.
echo ========================================
echo.
pause

:MENU
cls
echo ========================================
echo   请选择操作
echo ========================================
echo.
echo 1. 开始推送数据到 GitHub
echo 2. 查看推送指南
echo 3. 退出
echo.
set /p CHOICE="请输入选择 (1/2/3): "

if "%CHOICE%"=="1" goto :PUSH
if "%CHOICE%"=="2" goto :GUIDE
if "%CHOICE%"=="3" goto :END

echo 无效选择
timeout /t 2 >nul
goto :MENU

:PUSH
cls
echo ========================================
echo   步骤 1: 创建 GitHub 仓库
echo ========================================
echo.
echo 正在打开 GitHub...
echo.
start https://github.com/new
echo.
echo ========================================
echo 请在浏览器中完成以下操作:
echo ========================================
echo.
echo 1. 登录账号：932142751@qq.com
echo 2. 填写仓库信息:
echo    - Repository name: xiaoying-workspace
echo    - Description: 小盈 Agent 工作区
echo 3. 选择可见性: Private (私有) 
echo 4. 不要勾选 "Add a README file"
echo 5. 点击 "Create repository"
echo.
echo ========================================
echo.
set /p DONE1="完成后按回车继续..."

cls
echo ========================================
echo   步骤 2: 推送数据
echo ========================================
echo.
echo 正在切换到工作区目录...
cd /d "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"

echo.
echo 正在添加所有文件...
git add -A
echo ✓ 文件已添加

echo.
echo 正在提交更改...
git commit -m "同步工作区数据"
echo ✓ 已提交

echo.
echo 准备推送到 GitHub...
echo 数据量：2,490 个文件
echo 预计时间：5-15 分钟
echo.
echo 注意:
echo - Windows 会弹出 GitHub 登录窗口
echo - 输入账号：932142751@qq.com
echo - 输入密码或使用 Token
echo.
set /p CONFIRM="按回车开始推送..."

echo.
echo 正在推送...
echo.
git push -u origin main

echo.
if %errorlevel% == 0 (
    color 0A
    echo ========================================
    echo   ✅ 推送成功！
    echo ========================================
    echo.
    echo 你的数据已同步到:
    echo https://github.com/Hank-zz1/xiaoying-workspace
    echo.
    echo 下一步:
    echo 1. 访问以上网址验证
    echo 2. 在新电脑运行 新电脑恢复.bat
    echo.
    echo 庆祝！你的工作区已具备云同步能力！
    echo.
) else (
    color 0C
    echo ========================================
    echo   ❌ 推送失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 仓库还未创建 - 请返回步骤 1
    echo 2. 账号密码错误 - 检查登录信息
    echo 3. 网络问题 - 检查网络连接
    echo 4. 需要使用代理/VPN
    echo.
    echo 解决方案:
    echo 方案 A: 使用 GitHub Desktop
    echo   下载：https://desktop.github.com/
    echo.
    echo 方案 B: 查看详细指南
    echo   打开：推送 GitHub 指南.md
    echo.
    echo 方案 C: 检查网络连接后重试
    echo.
)

echo ========================================
echo.
set /p AGAIN="是否返回主菜单？(Y/N): "
if /i "%AGAIN%"=="Y" goto :MENU
goto :END

:GUIDE
cls
echo ========================================
echo   推送指南
echo ========================================
echo.
echo 详细步骤请查看:
echo.
echo 1. 00-开始这里.md - 快速开始
echo 2. 推送 GitHub 指南.md - 详细方案
echo 3. 跨机器同步指南.md - 完整流程
echo.
echo 按回车返回主菜单...
pause >nul
goto :MENU

:END
cls
echo ========================================
echo   感谢使用
echo ========================================
echo.
echo 如有问题，请查看:
echo - 00-开始这里.md
echo - Git 同步总览.md
echo.
echo 祝你使用愉快！
echo.
pause
