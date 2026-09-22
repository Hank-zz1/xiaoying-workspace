# 小盈历史对话数据迁移脚本 (PowerShell 版本)
# 解决 CMD 中文编码问题

$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "  小盈历史对话数据迁移工具" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host ""

$WORKSPACE = "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"
$BACKUP_DIR = "C:\Users\26011970\Desktop\小盈数据备份"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_NAME = "小盈数据备份_$TIMESTAMP"
$BACKUP_PATH = Join-Path $BACKUP_DIR $BACKUP_NAME

Write-Host "工作区路径：$WORKSPACE"
Write-Host "备份目标：$BACKUP_PATH"
Write-Host ""

# 创建备份目录
if (!(Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR | Out-Null
}
New-Item -ItemType Directory -Path $BACKUP_PATH -Force | Out-Null

Write-Host "[1/6] 复制历史对话数据 (sessions)..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\sessions" -Destination "$BACKUP_PATH\sessions" -Recurse -Force

Write-Host "[2/6] 复制工作区配置..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\config.json" -Destination $BACKUP_PATH -Force
Copy-Item -Path "$WORKSPACE\automations.json" -Destination $BACKUP_PATH -Force
Copy-Item -Path "$WORKSPACE\skill-registry.json" -Destination $BACKUP_PATH -Force

Write-Host "[3/6] 复制长期记忆..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\memory" -Destination "$BACKUP_PATH\memory" -Recurse -Force

Write-Host "[4/6] 复制自定义技能..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\skills" -Destination "$BACKUP_PATH\skills" -Recurse -Force
Copy-Item -Path "$WORKSPACE\skills-dev" -Destination "$BACKUP_PATH\skills-dev" -Recurse -Force

Write-Host "[5/6] 复制数据源配置..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\sources" -Destination "$BACKUP_PATH\sources" -Recurse -Force

Write-Host "[6/6] 复制迁移指南..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\小盈数据迁移指南.md" -Destination $BACKUP_PATH -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  备份完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "备份位置：$BACKUP_PATH" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步操作:" -ForegroundColor Yellow
Write-Host "1. 将备份文件夹复制到新机器"
Write-Host "2. 在新机器上安装小盈 Agent"
Write-Host "3. 按照《小盈数据迁移指南.md》还原数据"
Write-Host ""
Write-Host "按任意键继续..."
# $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
