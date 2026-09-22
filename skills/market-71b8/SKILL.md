---
name: "版本升级后自动检测修复"
description: "Incaier Agent 平台版本升级后，自动扫描工作区中所有能力（技能、自动化、配置、数据源、部署平台），检测并修复因版本升级导致的逻辑错误，确保所有能力在新版本下正常运行。适用于任何用户的任何工作区，不绑定特定邮箱或多维表格。"
alwaysAllow: ["Bash", "read", "grep", "find", "Glob", "ls", "config_validate"]
---

# 版本升级后自动检测修复

## 概述

当 Incaier Agent 平台发布新版本后，自动扫描工作区中所有配置和能力，检测并修复因升级导致的兼容性问题。本技能是**通用工具**，不绑定任何特定用户、邮箱、多维表格或业务场景。

## 触发条件

- 用户说"检查版本升级问题"、"修正发版错误"、"修复升级后的问题"
- 平台版本更新后手动触发
- 定时任务行为异常（如重复执行、未执行）时

## 扫描范围（8 大类）

本技能会扫描工作区中以下所有内容：

| # | 扫描对象 | 文件/路径 | 检查要点 |
|---|---------|----------|---------|
| 1 | 技能（Skills） | `skills-dev/*/SKILL.md`、`skills/*/SKILL.md` | 硬编码路径、参数变更、YAML 有效性 |
| 2 | 自动化（Automations） | `automations.json` | 事件名、Cron、Label、内联 Prompt |
| 3 | 工作区配置 | `config.json` | 源列表、权限默认值 |
| 4 | 数据源（Sources） | `sources/*/config.json` | 连接状态、认证配置 |
| 5 | 标签（Labels） | `labels/config.json` | 标签引用有效性 |
| 6 | 部署平台（Webapps） | `market-mcp-create-webapp` 相关 | 运行时契约、API 兼容 |
| 7 | 历史执行记录 | `automations-history.jsonl` | 重复执行、失败模式 |
| 8 | 跨能力一致性 | 全局 | 技能与自动化之间的引用一致性 |

---

## 一、技能（Skills）检测

### 1.1 硬编码用户路径

**问题**：技能中包含特定用户路径（如 `C:/Users/00593289/...`），导致其他用户无法使用。

**检测方式**：
```bash
grep -rn "C:/Users/" skills-dev/*/SKILL.md skills/*/SKILL.md
```

**自动修复**：
- 将硬编码路径替换为 `{SKILL_DIR}` 或 `$HOME` 等可移植变量
- 在 SKILL.md 顶部添加"配置参数"表格，让用户自行修改

### 1.2 CLI 参数兼容性

**已知问题**：某些 CLI 工具在 `--incaier-mode` 下存在 JSON 解析 bug（如 mailcli 的 `email get`）。

**检测方式**：
- 检查所有 `--incaier-mode` 使用场景，交叉对比已知 bug 列表
- 检查 `--user-id` 和 `--incaier-mode` 的正确使用场景

**已知问题清单**（持续更新）：

| 工具 | 命令 | 问题 | 修复 |
|------|------|------|------|
| mailcli | `email get --incaier-mode` | JSON 解析错误 `invalid character ':' after top-level value` | 改用 `--user-id "用户名"` |
| mailcli | `email search --incaier-mode` | 正常 | 无需修改 |
| mailcli | `auth login --incaier-mode` | 正常 | 无需修改 |
| lark-cli | `+record-list`（非 `base +record-list`） | 子命令层级错误 | 必须用 `lark-cli base +record-list` |

### 1.3 YAML 前置元数据

**检测方式**：
```bash
# 检查所有技能是否包含必要字段
for f in skills-dev/*/SKILL.md skills/*/SKILL.md; do
  echo "=== $f ==="
  head -10 "$f" | grep -E "^name:|^description:"
done
```

**自动修复**：确保每个 SKILL.md 包含：
- `name`：显示名称
- `description`：技能说明
- `alwaysAllow`（如需要）

### 1.4 硬编码 Token/密码

**检测方式**：
```bash
grep -rn "NAlebl9\|sk-[a-zA-Z0-9]\|ghp_\|xoxb-" skills-dev/*/SKILL.md skills/*/SKILL.md
```

**自动修复**：将 Token 提取到"配置参数"表格中，添加注释说明用户需自行替换。

---

## 二、自动化（Automations）检测

### 2.1 事件名称废弃

**检测**：`automations.json` 中是否使用了已废弃的事件名。

**已知废弃事件**：
- `TodoStateChange` → 应改为 `SessionStatusChange`

**检测方式**：
```bash
grep -n "TodoStateChange" automations.json
```

### 2.2 Cron 表达式有效性

**检测**：验证 cron 字段格式（5 字段：分 时 日 月 周）。

**常见错误**：
- 6 字段 cron（带了秒）
- 非法值（如 `0 25 * * *`）
- 缺少 `timezone` 字段

### 2.3 标签（Labels）引用有效性

**检测**：自动化中引用的 label ID 是否在 `labels/config.json` 中存在。

**检测方式**：
1. 读取 `labels/config.json` 获取所有有效 label ID
2. 检查 `automations.json` 中每个 `labels` 数组中的值是否存在于配置中
3. 不存在的 label → 自动替换为 `"other"`

### 2.4 内联 Prompt 体积

**问题**：自动化 prompt 过长（>500 字），难以维护，不便于复用。

**检测**：检查每个 action 的 prompt 字段长度。

**自动修复**：
- 如果 prompt 超过 500 字且包含完整流程步骤，建议提取为技能
- 将 prompt 改为简洁的 `@skill-name 执行xxx` 格式

### 2.5 权限模式

**检测**：`permissionMode` 是否合理。

**规则**：
- 定时任务（含 `cron`）建议 `allow-all`
- 事件驱动任务建议 `ask` 或 `safe`
- 缺少 `permissionMode` 时自动补充

### 2.6 重复执行记录

**检测方式**：分析 `automations-history.jsonl`，检查同一 `id` 在同一时间窗口内是否多次触发。

**自动修复**：
- 在对应技能中添加幂等性保护逻辑
- 在自动化 prompt 中添加"执行前检查是否已有当日记录"的提示

---

## 三、工作区配置（config.json）检测

### 3.1 默认权限模式

**检测**：`defaults.permissionMode` 是否设置。

### 3.2 源列表有效性

**检测**：`defaults.enabledSourceSlugs` 中的源是否都存在。

**检测方式**：
```bash
# 列出所有已安装的源
ls sources/
# 对比 config.json 中的 enabledSourceSlugs
```

### 3.3 本地 MCP 服务器

**检测**：`localMcpServers.enabled` 是否设置（建议为 `true`）。

---

## 四、数据源（Sources）检测

### 4.1 配置完整性

**检测**：每个 `sources/*/config.json` 是否包含必要字段。

### 4.2 认证状态

**检测方式**：对每个源调用 `source_test`。

**常见问题**：
- OAuth token 过期
- API key 失效
- 连接 URL 变更

---

## 五、部署平台（Webapps）检测

### 5.1 运行时契约

**检测**：通过 `market-mcp-create-webapp` 的 `my_app_list` 获取所有部署的应用。

**检测要点**：
- 应用是否正常运行（`my_app_invoke` 测试）
- 是否使用了已废弃的 API
- 数据库连接是否正常

### 5.2 密钥管理

**检测**：通过 `my_app_secret_list` 检查密钥是否过期。

---

## 六、跨能力一致性检测

### 6.1 技能与自动化引用一致性

**检测**：自动化 prompt 中引用的 `@skill-name` 是否对应已安装的技能。

**检测方式**：
1. 提取所有自动化 prompt 中的 `@xxx` 引用
2. 与 `.skill-registry.json` 中的 slug 列表对比
3. 不匹配的引用 → 提示修复

### 6.2 技能之间的依赖一致性

**检测**：技能文档中引用的其他技能路径是否存在。

---

## 七、自动修复执行流程

### 完整扫描流程

```
1. 读取工作区结构
   ├── skills-dev/*/SKILL.md
   ├── skills/*/SKILL.md
   ├── automations.json
   ├── automations-history.jsonl
   ├── config.json
   ├── labels/config.json
   └── sources/*/config.json

2. 逐类扫描，记录所有问题
   ├── 严重（阻断性）：会导致功能完全失效
   ├── 警告（兼容性）：可能在未来版本失效
   └── 建议（优化）：可改进但不影响功能

3. 自动修复（安全操作，无需确认）
   ├── 替换硬编码路径为变量
   ├── 修正废弃事件名
   ├── 修正无效 label 引用
   ├── 补充缺失的 permissionMode
   └── 提取内联 prompt 为技能引用

4. 手动修复（高风险操作，需用户确认）
   ├── 修改 Token/密码
   ├── 删除表或记录
   └── 重新部署应用

5. 验证
   ├── config_validate --target automations
   ├── config_validate --target config
   └── skill_draft_validate（对修改的技能）
```

### 修复原则

1. **只修复因版本升级导致的问题**，不改变用户原有业务逻辑
2. **可逆操作**优先，修改前记录原始值
3. **Token 和密码绝不硬编码**，提取到配置参数表
4. **所有修改通过 config_validate 验证**后再提交
5. **通用化处理**：不假设任何特定用户、邮箱、表名

---

## 八、汇报格式

修复完成后，按以下格式汇报：

```markdown
## 版本升级检测修复报告

### 扫描概况
| 类别 | 检查项 | 通过 | 已修复 | 需手动处理 |
|------|--------|------|--------|-----------|
| 技能 | N | N | N | N |
| 自动化 | N | N | N | N |
| 配置 | N | N | N | N |
| 数据源 | N | N | N | N |
| 平台 | N | N | N | N |

### 已自动修复（N 项）
| # | 类别 | 位置 | 问题 | 修复 |
|---|------|------|------|------|

### 需手动处理（N 项）
| # | 类别 | 位置 | 问题 | 建议 |
|---|------|------|------|------|

### 验证结果
- automations.json: ✅/❌
- config.json: ✅/❌
- 技能验证: ✅/❌
```

---

## 九、已知平台版本变更记录

> **⚠️ 此章节需在每次平台升级后更新。** 记录已知的 breaking changes。

| 版本 | 变更类型 | 影响范围 | 说明 |
|------|---------|---------|------|
| 当前 | SchedulerTick 重复 | 自动化 | 定时任务偶发重复触发，需在技能中增加幂等性保护 |
| 当前 | mailcli `email get --incaier-mode` bug | 邮件技能 | JSON 解析错误，需改用 `--user-id` |
| 当前 | `TodoStateChange` 废弃 | 自动化 | 需改为 `SessionStatusChange` |
| 当前 | prompt 内联→技能引用 | 自动化 | 建议将长 prompt 提取为技能，通过 `@skill-name` 引用 |

---

## 十、其他用户使用指南

1. 安装此技能到你的工作区
2. 运行 `@upgrade-auto-fix` 触发扫描
3. 查看自动修复结果，确认需手动处理的项目
4. 如需针对你的业务场景定制，修改 SKILL.md 中"已知平台版本变更记录"章节