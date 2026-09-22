import requests
import json
import datetime

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

today = datetime.date(2026, 6, 2)
weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
date_str = f"{today.year}年{today.month}月{today.day}日 {weekday_cn[today.weekday()]}"

# ========== 构建飞书卡片 ==========

# 板块一：国内外要闻
section1_fields = []
news_items = [
    ("《求是》发表习近平重要文章", "第11期《求是》杂志发表习近平总书记重要文章《前瞻布局和发展未来产业》，强调超前布局未来产业。"),
    ("长征十二号乙遥一火箭发射成功", "6月1日16:40，长征十二号乙首飞成功，顺利送入千帆极轨08组卫星，系长征系列第647次发射。"),
    ("我国全面进入汛期", "6月1日起全国进入汛期，南方地区进入主汛期，各地防汛工作全面启动。"),
    ("2026年国家医保目录调整启动", "医保药品目录调整工作正式启动，进一步优化报销范围，惠及亿万参保群众。"),
    ("网络餐饮新规今起施行", "外卖食品安全新规实施，明确平台责任，严打'幽灵外卖'，保障消费者权益。"),
    ("英伟达GTC 2026：正式进军PC芯片", "黄仁勋发布RTX Spark处理器，采用台积电3nm Arm架构，集成Blackwell GPU，挑战英特尔主导地位。"),
    ("美伊冲突升级，霍尔木兹海峡告急", "伊朗暂停与美谈判，计划封锁霍尔木兹海峡；国际油价飙升，布伦特原油突破95美元/桶。"),
    ("特朗普称黎以达成停火", "特朗普表示黎真主党同意与以停火，但与伊朗核谈仍有细节待敲定。现货黄金逼近4500美元。"),
    ("天涯社区正式重启", "停服三年后，天涯社区6月1日启用tianya.net域名恢复访问，'天涯神帖'冲上热搜。"),
    ("A股6月开门红", "沪指微涨0.02%，4200+股上涨；电力、煤炭、白酒等低位蓝筹领涨，AI应用活跃。"),
]

for title, desc in news_items:
    section1_fields.append({
        "is_short": False,
        "text": {
            "tag": "lark_md",
            "content": f"**{title}**\n{desc}"
        }
    })

# 板块二：各平台热搜 Top 5
section2_fields = []
platforms = [
    ("微博", [
        ("天涯社区重启", "互联网"),
        ("英伟达进军PC芯片", "科技"),
        ("六一儿童节", "社会"),
        ("美伊冲突升级", "国际"),
        ("马思唯汪苏泷演唱会", "娱乐"),
    ]),
    ("百度", [
        ("长征十二号火箭发射", "科技"),
        ("美伊冲突霍尔木兹危机", "国际"),
        ("医保目录调整启动", "民生"),
        ("网络餐饮新规实施", "社会"),
        ("A股六月开门红", "财经"),
    ]),
    ("抖音", [
        ("六一儿童节快乐", "社会"),
        ("美伊局势最新进展", "国际"),
        ("马思唯演唱会后台", "娱乐"),
        ("黑龙江极端天气", "社会"),
        ("汪苏泷演唱会徒手捏虫", "娱乐"),
    ]),
    ("知乎", [
        ("英伟达进军PC芯片有何影响", "科技"),
        ("美伊冲突为何反复升级", "国际关系"),
        ("天涯社区重启意味着什么", "互联网"),
        ("如何理解未来产业布局", "政策"),
        ("霍尔木兹海峡危机分析", "能源"),
    ]),
]

for platform_name, items in platforms:
    lines = [f"**{platform_name}热搜 Top 5**"]
    for i, (title, cat) in enumerate(items, 1):
        lines.append(f"{i}. {title} `{cat}`")
    section2_fields.append({
        "is_short": False,
        "text": {
            "tag": "lark_md",
            "content": "\n".join(lines)
        }
    })

# 板块三：跨平台热点
section3_fields = []
cross_hot = [
    ("美伊冲突与霍尔木兹海峡危机", "微博 · 百度 · 知乎 · 抖音", "美伊关系反复、海峡封锁风险引发全球油价与资本市场剧烈波动，成全网最热话题。"),
    ("英伟达GTC 2026 进军PC芯片", "微博 · 百度 · 知乎", "黄仁勋宣布推出RTX Spark处理器挑战英特尔，定义AI时代PC新形态，科技圈热议。"),
    ("天涯社区正式重启", "微博 · 知乎", "停服三年的天涯社区回归，'天涯神帖'引发全网怀旧潮，互联网情怀再次被点燃。"),
    ("六一国际儿童节", "微博 · 抖音 · 百度", "总书记回信勉励少先队员，1.12亿少先队员数据发布，儿童友好建设全域覆盖。"),
]

for title, platforms_str, desc in cross_hot:
    section3_fields.append({
        "is_short": False,
        "text": {
            "tag": "lark_md",
            "content": f"**{title}**\n覆盖平台：{platforms_str}\n{desc}"
        }
    })

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": f"\U0001F4F0 每日新闻播报 | {date_str}"},
        "template": "blue"
    },
    "elements": [
        # 板块一
        {"tag": "div", "text": {"tag": "lark_md", "content": "**\U0001F30D 一、国内外要闻**"}},
        {"tag": "div", "fields": section1_fields},
        {"tag": "hr"},
        # 板块二
        {"tag": "div", "text": {"tag": "lark_md", "content": "**\U0001F525 二、各平台热搜 Top 5**"}},
        {"tag": "div", "fields": section2_fields},
        {"tag": "hr"},
        # 板块三
        {"tag": "div", "text": {"tag": "lark_md", "content": "**\U0001F4E2 三、跨平台热点**"}},
        {"tag": "div", "fields": section3_fields},
        {"tag": "hr"},
        {"tag": "div", "text": {"tag": "lark_md", "content": "\U0001F4CA **今日市场速览**：沪指 +0.02% | WTI原油 $92.30/桶 | 现货黄金 $4485/盎司 | 美股三大指数收涨"}},
    ],
    "note": {"tag": "plain_text", "content": "由 Incaier Agent 自动生成 | 数据来源：新闻联播、各平台热搜"}
}

payload = {
    "msg_type": "interactive",
    "card": card
}

resp = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json; charset=utf-8"})
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")