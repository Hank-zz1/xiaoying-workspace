# 小盈历史对话数据迁移脚本
$ErrorActionPreference = "SilentlyContinue"

Write-Host "========================================"
Write-Host "  小盈数据迁移工具" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host ""

$WORKSPACE = "C:\Users\26011970\.incaier-agent\workspaces\my-workspace"
$BACKUP_DIR = "C:\Users\26011970\Desktop\小盈数据备份"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$BACKUP_NAME = "小盈数据备份_$TIMESTAMP"
$BACKUP_PATH = Join-Path $BACKUP_DIR $BACKUP_NAME

Write-Host "工作区：$WORKSPACE"
Write-Host "备份到：$BACKUP_PATH"
Write-Host ""

New-Item -ItemType Directory -Path $BACKUP_PATH -Force | Out-Null

Write-Host "[1/6] 复制 sessions..." -ForegroundColor Yellow
robocopy "$WORKSPACE\sessions" "$BACKUP_PATH\sessions" /E /NFL /NDL /NJH /NJS

Write-Host "[2/6] 复制配置文件..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\config.json" -Destination $BACKUP_PATH -Force
Copy-Item -Path "$WORKSPACE\automations.json" -Destination $BACKUP_PATH -Force
if (Test-Path "$WORKSPACE\skill-registry.json") {
    Copy-Item -Path "$WORKSPACE\skill-registry.json" -Destination $BACKUP_PATH -Force
}

Write-Host "[3/6] 复制 memory..." -ForegroundColor Yellow
robocopy "$WORKSPACE\memory" "$BACKUP_PATH\memory" /E /NFL /NDL /NJH /NJS

Write-Host "[4/6] 复制 skills..." -ForegroundColor Yellow
robocopy "$WORKSPACE\skills" "$BACKUP_PATH\skills" /E /NFL /NDL /NJH /NJS
robocopy "$WORKSPACE\skills-dev" "$BACKUP_PATH\skills-dev" /E /NFL /NDL /NJH /NJS

Write-Host "[5/6] 复制 sources..." -ForegroundColor Yellow
robocopy "$WORKSPACE\sources" "$BACKUP_PATH\sources" /E /NFL /NDL /NJH /NJS

Write-Host "[6/6] 复制迁移指南..." -ForegroundColor Yellow
Copy-Item -Path "$WORKSPACE\小盈数据迁移指南.md" -Destination $BACKUP_PATH -Force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  备份完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "备份位置：$BACKUP_PATH" -ForegroundColor Cyan
Write-Host ""
Write-Host "请手动将此文件夹复制到新机器即可。"
