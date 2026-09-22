import json, requests

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

news = [
    {
        "title": "伯克利发布FST框架，突破大模型持续学习死局",
        "summary": "伯克利等机构发布FST框架，通过快慢分层机制解决大模型持续学习中的灾难性遗忘问题，被预言2026年持续学习即将爆发。",
        "source": "新浪网 · 2026-05-19"
    },
    {
        "title": "OpenAI 发布 GPT-5.5 Instant，成为 ChatGPT 默认模型",
        "summary": "GPT-5.5 Instant 推理速度与准确性显著提升，高风险领域幻觉率降低 52.5%，同步上线广告平台实现商业化。",
        "source": "CSDN · 2026-05-18"
    },
    {
        "title": "苹果 iOS 27 将支持用户自由选择不同 AI 模型",
        "summary": "苹果在 iOS 27 中允许用户在各功能中选择不同 AI 模型，标志着苹果 AI 生态布局的重要战略转变。",
        "source": "CSDN · 2026-05-18"
    },
    {
        "title": "月之暗面估值突破 200 亿美元，成中国 AI 独角兽之最",
        "summary": "Moonshot AI 完成新一轮融资，估值突破 200 亿美元，旗下 Kimi 智能助手在长文本和多模态交互方面表现出色。",
        "source": "CSDN · 2026-05-18"
    },
    {
        "title": "上海\"十五五\"规划：推动 10 万台人形机器人进工厂",
        "summary": "上海全面实施\"人工智能+\"行动，力争到十五五末规上工业企业智能体应用普及率超 80%。",
        "source": "上海证券报 · 2026-05-18"
    },
    {
        "title": "微软前副总裁炮轰：微软已错失 AI 浪潮",
        "summary": "微软前技术顾问公开表示微软正重蹈互联网与移动时代覆辙，AI 领域投入与产出存巨大反差。",
        "source": "快科技 · 2026-05-18"
    },
    {
        "title": "OpenAI 砸 40 亿美元成立新公司，加速企业 AI 落地",
        "summary": "OpenAI 成立新公司，初始投资超 40 亿美元（约 272 亿人民币），联合 19 家机构帮企业搭建并落地 AI。",
        "source": "东方财富网 · 2026-05-17"
    },
    {
        "title": "腾讯阿里同步加码 AI 基建，资本支出创新高",
        "summary": "腾讯 Q1 AI 资本支出 370 亿创单季新高；阿里 AI 投入将远超原定 3800 亿，平头哥自研 GPU 已量产。",
        "source": "搜狐 · 2026-05-14"
    },
    {
        "title": "MCP 协议生态扩张：AI Agent 从概念验证迈向规模化",
        "summary": "MCP 注册表服务器近 2000 个，微软、谷歌、OpenAI 及国内 BAT 纷纷布局，2026 年将成 Agent 商业爆发节点。",
        "source": "CSDN · 2026-05-16"
    },
    {
        "title": "谷歌 Gemini 2.5 Pro I/O 版发布，编程能力登顶全球",
        "summary": "Gemini 2.5 Pro 在 WebDev Arena 以 1499 分登顶，超越 Claude 3.7 和 GPT-4o，首次在代码评测全面领先。",
        "source": "CSDN · 2026-05-07"
    },
]

elements = []
for i, item in enumerate(news):
    content = f"**{item['title']}**\n{item['summary']}\n<font color='grey'>{item['source']}</font>"
    elements.append({
        "tag": "div",
        "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": content}}]
    })
    if i < len(news) - 1:
        elements.append({"tag": "hr"})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "🤖 AI 产品/技术日报 · 2026年5月19日"},
        "template": "green"
    },
    "elements": elements,
    "note": {"tag": "plain_text", "content": "由 Incaier Agent 自动生成"}
}

payload = {"msg_type": "interactive", "card": card}

resp = requests.post(webhook_url, json=payload, timeout=15)
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")