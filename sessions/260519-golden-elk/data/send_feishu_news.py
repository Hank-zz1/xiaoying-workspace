import json
import requests

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

news_items = [
    ("GPT-5.4/6系列密集发布：OpenAI推Symphony架构+200万Token上下文，千万级Token突破",
     "GPT-5.4系列包含Pro/Thinking/xhigh三版本，编程SWE-Bench Pro达57.7%；GPT-6默认百万Token上下文。",
     "CSDN · 2026-05-16"),

    ("Anthropic发布Claude Opus 4.6与Sonnet 4.6",
     "100万上下文全面开放并取消长文本溢价，推理效率大幅提升，架构改进超越单纯参数规模扩展。",
     "CSDN · 2026-05-14"),

    ("中国AI应用产业加速落地：从技术赋能到价值创造",
     "覆盖医疗、工业、教育等领域，形成超300个专业数据集；端云协同新范式推动AI向中小企业普及。",
     "新浪网/中研网 · 2026-05-14"),

    ("米哈游发布LPM 1.0表演大模型：攻克\"不可能三角\"",
     "创新解决AI生成\"创意性、可控性、效率\"三者难以兼顾的问题，为游戏NPC智能对话带来毫秒级响应。",
     "CSDN · 2026-05-15"),

    ("开源Agent框架OpenClaw突破31万GitHub Stars",
     "支持多智能体协作、复杂工具调用和长程任务规划，兼容OpenAI/Anthropic/DeepSeek等主流API。",
     "CSDN · 2026-05-15"),

    ("大模型技术全景演进：混合架构成基座新标配",
     "Transformer与SSM(Mamba2)混合架构完成从论文到边端化全面跃迁，实现线性复杂度推理与训练。",
     "CSDN · 2026-05-12"),

    ("Google Gemini月活突破7.5亿：全球最大AI服务",
     "API每分钟处理100亿Token，集成Android/Workspace生态，通过MCP协议推动跨平台AI应用标准化。",
     "SegmentFault · 2026-02-25"),

    ("轻量小模型时代来临：端侧AI全面爆发",
     "千亿参数模型可在移动端/IoT设备高效运行，国产开源模型以小参数跑出接近GPT-4的性能。",
     "CSDN · 2026-03-10"),

    ("中金展望2026：大模型在强化学习/记忆/上下文工程突破",
     "从短context生成到长思维链任务，从文本交互到原生多模态，向实现AGI长期目标更进一步。",
     "36氪/中金 · 2026-02-05"),

    ("全球大模型进入实用主义新时代：效率优先场景为王",
     "国产大模型全球调用量反超，旗舰模型登顶国际盲测；行业告别参数内卷，迈入生态重构阶段。",
     "CSDN · 2026-05-16"),
]

# Build card elements: each news item as a div followed by a divider
elements = []
for i, (title, summary, source) in enumerate(news_items):
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{title}**\n{summary}\n*{source}*"
            }
        }]
    })
    if i < len(news_items) - 1:
        elements.append({"tag": "hr"})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "AI 产品/技术日报 · 2026年5月19日"
        },
        "template": "green"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成"
    }
}

payload = {"msg_type": "interactive", "card": card}
resp = requests.post(webhook_url, json=payload, timeout=15)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")