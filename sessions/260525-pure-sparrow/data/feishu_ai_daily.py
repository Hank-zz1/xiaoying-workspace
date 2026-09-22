import requests, json

webhook = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

news = [
    {"title": "DeepSeek V4-Pro 逆市永久降价75%", "summary": "旗舰模型 API 价格降至每百万 Tokens 仅 0.025 元，创全球新低。依托自研稀疏注意力机制与国产算力深度适配实现成本优势。", "source": "太平洋科技", "date": "2026-05-25"},
    {"title": "荣耀发布首款自进化 AI 原生手机 Magic8 系列", "summary": "搭载 MagicOS 10 自进化 AI 智能体 YOYO，具备「看见」与「执行」能力，覆盖衣食住行购全场景智能服务。", "source": "新浪网", "date": "2026-05-25"},
    {"title": "阿里云发布全新 AI 产品官网「千问云」", "summary": "为 AI Agent 而生，上线 Qwen/GLM/Kimi/DeepSeek 等 150+ 主流模型 API，采用 Agent-Friendly 设计理念。", "source": "新浪网", "date": "2026-05-20"},
    {"title": "Manus 1.6 正式发布，推出 Max 高性能模式", "summary": "Manus Max 针对复杂工作流优化，显著提升任务执行效率与成功率，巩固通用 AI Agent 领先地位。", "source": "CSDN", "date": "2026-05-23"},
    {"title": "百度发布 DuMate App，首提 DAA（日活智能体数）概念", "summary": "李彦宏在发布会强调 AI 日常应用潜力，同步推出秒哒 App 深化社交与 AI 融合。", "source": "搜狐", "date": "2026-05-13"},
    {"title": "腾讯元宝新增一键总结微信群聊功能", "summary": "利用 AI 快速提取群聊关键信息，提升沟通效率，体现社交场景 AI 技术深度融入。", "source": "搜狐", "date": "2026-05-13"},
    {"title": "蚂蚁集团「蚂蚁阿福」AI 健康助手全面升级", "summary": "基于百灵大模型，从医疗工具转向有温度的 AI 健康朋友，聚焦健康问答、陪伴与服务三大功能。", "source": "CSDN", "date": "2026-05-23"},
    {"title": "阿里高管预计阿里云 AI 收入占比将突破 50%", "summary": "反映企业加速智能化转型，AI 产品覆盖数据分析到智能客服，市场份额有望持续增长。", "source": "搜狐", "date": "2026-05-13"},
    {"title": "ChatGLM 大模型取得技术新突破", "summary": "在语言理解精准度、知识推理能力方面大幅提升，能深入理解隐喻/双关等修辞，赋能智能客服与写作场景。", "source": "智简AI", "date": "2026-05-13"},
    {"title": "Google Gemini AI 拓展至笔记本电脑", "summary": "Android 17 新功能将 Gemini AI 系统引入笔记本端，更多用户可体验 AI 便捷，提升操作系统智能化水平。", "source": "搜狐", "date": "2026-05-13"},
]

# 构建卡片元素
elements = []
for i, n in enumerate(news):
    content = f"**{i+1}. {n['title']}**\n{n['summary']}\n📅 {n['date']}  |  来源：{n['source']}"
    elements.append({
        "tag": "div",
        "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": content}}]
    })
    if i < len(news) - 1:
        elements.append({"tag": "hr"})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "🤖 AI 产品/技术日报 — 2026年5月25日"},
        "template": "green"
    },
    "elements": elements,
    "note": {"tag": "plain_text", "content": "由 Incaier Agent 自动生成"}
}

body = {"msg_type": "interactive", "card": card}
r = requests.post(webhook, json=body, timeout=15)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")