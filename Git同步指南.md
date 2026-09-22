# 小盈工作区 Git 同步指南

使用 Git 同步工作区，实现多设备数据共享和版本管理。

---

## 📋 准备工作

### 1. 安装 Git

**Windows 下载地址**: https://git-scm.com/download/win

安装时保持默认选项即可。

### 2. 配置 Git 用户信息

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. 创建远程仓库

**推荐平台**:
- **GitHub**: https://github.com (国际通用)
- **Gitee**: https://gitee.com (国内访问快)
- **GitLab**: https://gitlab.com

**创建步骤**:
1. 登录平台
2. 点击 "New Repository" / "新建仓库"
3. 仓库名建议：`xiaoying-workspace` 或 `incaier-my-workspace`
4. **不要**勾选"Initialize this repository with a README"
5. 创建后复制仓库地址

---

##  初始化设置 (只需做一次)

### 步骤 1: 初始化 Git 仓库

**方式 A: 使用自动脚本 (推荐)**

双击运行:
```
setup-git-sync.bat
```

**方式 B: 手动执行**

```bash
cd C:\Users\26011970\.incaier-agent\workspaces\my-workspace
git init
```

### 步骤 2: 设置远程仓库

```bash
setup-git-remote.bat
```

然后输入你的仓库地址，例如:
- HTTPS: `https://github.com/yourname/xiaoying-workspace.git`
- SSH: `git@github.com:yourname/xiaoying-workspace.git`

### 步骤 3: 首次推送

```bash
# 确保分支名为 main
git branch -M main

# 推送到远程仓库
git push -u origin main
```

---

## 🔄 日常同步流程

### 在当前机器提交更改

```bash
# 1. 查看更改
git status

# 2. 添加所有更改
git add -A

# 3. 提交更改
git commit -m "描述你的更改，例如：添加新的冰箱监控会话数据"

# 4. 推送到远程仓库
git push
```

### 在新机器上恢复工作区

```bash
# 1. 克隆仓库到新机器
git clone <你的仓库地址> C:\Users\<用户名>\.incaier-agent\workspaces\my-workspace

# 2. 安装小盈 Agent

# 3. 打开 Agent，工作区会自动识别
```

### 在多台机器间同步

**机器 A (提交更改)**:
```bash
git add -A
git commit -m "更新内容"
git push
```

**机器 B (拉取更改)**:
```bash
cd C:\Users\<用户名>\.incaier-agent\workspaces\my-workspace
git pull
```

---

## ⚠️ 重要注意事项

### 1. .gitignore 已自动配置

以下文件**不会**被同步:
- `__pycache__/`, `node_modules/` - 临时文件
- `.vscode/`, `.idea/` - IDE 配置
- `*.log` - 日志文件
- `data/` - 大型数据文件 (默认不同步，可选择性同步)

### 2. 大文件处理

如果工作区超过 100MB，建议使用:

**方案 A: Git LFS (Large File Storage)**
```bash
# 安装 Git LFS
git lfs install

# 跟踪大文件类型
git lfs track "*.pdf"
git lfs track "sessions/*/attachments/*"

# 提交 .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS"
```

**方案 B: 排除大型会话数据**

编辑 `.gitignore`，添加:
```
# 排除大型附件
sessions/*/attachments/*
sessions/*/data/*
```

### 3. 敏感信息

**不要提交敏感信息**:
- API 密钥
- 数据库密码
- 私人密钥

如果已提交，需要:
```bash
# 从历史中删除敏感文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch PATH_TO_FILE" \
  --prune-empty --tag-name-filter cat -- --all
```

---

## 🛠️ 常见问题

### Q1: 推送失败，提示远程仓库已有内容

**解决**:
```bash
git pull --rebase
git push
```

### Q2: 冲突如何解决？

```bash
# 1. 拉取时如果有冲突
git pull

# 2. 查看冲突文件
git status

# 3. 手动编辑冲突文件，解决冲突标记

# 4. 标记为解决
git add <文件名>

# 5. 继续 rebase 或提交
git rebase --continue
# 或
git commit -m "解决冲突"
```

### Q3: 如何只同步部分数据？

编辑 `.gitignore`:

**同步所有会话数据**:
```
# 注释掉排除规则
# sessions/*/data/*
# sessions/*/attachments/*
```

**仅同步最近会话**:
```bash
# 手动清理旧会话
# 然后提交
git add -A
git commit -m "清理旧会话数据"
git push
```

---

## 📊 最佳实践

### 提交频率建议

- **每天下班前**: 提交当天的工作区更改
- **完成重要任务后**: 立即提交
- **切换机器前**: 确保已推送

### 提交信息规范

```
<类型>: <简短描述>

例如:
feat: 添加新西兰冰箱监控定时任务
fix: 修复 LG 官网抓取超时问题
data: 更新澳洲冰箱基线数据
```

### 分支管理 (可选)

```bash
# 创建开发分支
git checkout -b dev

# 在开发分支测试新功能
git add -A
git commit -m "测试新功能"

# 测试完成后合并到 main
git checkout main
git merge dev
git push
```

---

## 🔐 SSH 认证 (推荐)

使用 SSH 比 HTTPS 更方便:

### 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

### 添加公钥到 GitHub/Gitee

1. 查看公钥:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 复制输出内容

3. 在 GitHub/Gitee 设置中添加 SSH Key:
   - GitHub: Settings → SSH and GPG keys → New SSH key
   - Gitee: 设置 → SSH 公钥 → 添加公钥

### 使用 SSH 地址

```
git remote set-url origin git@github.com:yourname/xiaoying-workspace.git
git push -u origin main
```

---

## 📝 总结

### ✅ Git 同步的优势

- ✅ 自动版本管理
- ✅ 多设备无缝切换
- ✅ 数据备份到云端
- ✅ 可追溯历史记录
- ✅ 支持多人协作

### 📋 快速参考

```bash
# 首次设置
git init
git add -A
git commit -m "Initial commit"
git remote add origin <仓库地址>
git push -u origin main

# 日常使用
git add -A
git commit -m "更新说明"
git push

# 在新机器恢复
git clone <仓库地址> <目标路径>
```

---

**需要帮助？** 查看 Git 官方文档: https://git-scm.com/doc
