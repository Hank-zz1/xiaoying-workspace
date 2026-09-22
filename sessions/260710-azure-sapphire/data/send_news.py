#!/usr/bin/env python3
"""每日新闻播报 - 飞书卡片消息发送"""
import requests
import json

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 每日新闻播报 | 2026年7月10日 星期五"},
        "template": "blue"
    },
    "elements": []
}

# ===== 板块一：国内外要闻 =====
elements = card["elements"]

elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**📌 一、国内外要闻**"}
})

news_items = [
    ("国家科学技术奖励大会在京召开",
     "2025年度国家科学技术奖揭晓，上海获奖数量创历年新高。陈立泉院士、贲德院士等获表彰。"),
    ("超强台风"巴威"来袭，多地停工停运停航",
     "台风路径持续调整，沿海多地启动防台应急响应，部分航班、列车停运。"),
    ("广西贵港洪灾：万名师生被洪水围困",
     "多所学校师生因洪水被困校园，"救援航母"紧急驰援，32岁青年游泳送物资。"),
    ("甘肃宕昌山体滑坡致21人遇难",
     "7名伤者均无生命危险，救援工作仍在紧张进行中。"),
    ("福建泉州鞋厂火灾致28人死亡",
     "附近住户称家属在厂里上班被及时疏散，事故原因正在调查。"),
    ("强对流天气袭击湖北多地",
     "省委书记要求全力做好救灾工作，省长赴现场指导抢险救灾。"),
    ("美军强力打击伊朗，国际油价应声上涨",
     "中东局势再度紧张，国际原油价格显著波动，引发全球市场关注。"),
    ("全国暑期文旅消费季启动，发放超4.5亿元消费券",
     "文化和旅游部联合多地启动暑期消费促进活动，涵盖景区、酒店、演出等。"),
    ("民政部：城乡三级养老服务网络聚焦失能失智照护",
     "重点满足失能失智老年人刚性照护需求，加强养老服务网络建设管理。"),
    ("台积电变"美积电"担忧升温，国台办回应",
     "岛内舆论对台积电赴美后产业空心化表示担忧，国台办做出回应。"),
]

for title, desc in news_items:
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {"tag": "lark_md", "content": f"**{title}**\n{desc}"}
        }]
    })

elements.append({"tag": "hr"})

# ===== 板块二：各平台热搜 Top 5 =====
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**🔥 二、各平台热搜 Top 5**"}
})

platforms = [
    ("📱 微博热搜", [
        ("姆巴佩受伤，法国队世界杯晋级", "体育"),
        ("超强台风巴威路径再调整", "社会"),
        ("广西加油共渡难关", "社会"),
        ("福建鞋厂火灾28人遇难", "社会"),
        ("国家科学技术奖励大会召开", "时事"),
    ]),
    ("🔍 百度热搜", [
        ("国家科学技术奖揭晓", "时事"),
        ("超强台风巴威来袭", "社会"),
        ("广西万名师生被洪水围困", "社会"),
        ("甘肃山体滑坡致21人遇难", "社会"),
        ("2026年国补政策落地", "财经"),
    ]),
    ("🎵 抖音热搜", [
        ("抗洪救灾一线感人瞬间", "社会"),
        ("世界杯法国队比赛精彩集锦", "体育"),
        ("暑期旅游消费券怎么领", "生活"),
        ("华为乾崑回应智驾断网里程上涨", "科技"),
        ("只此青绿在台湾演出受欢迎", "文化"),
    ]),
    ("💡 知乎热榜", [
        ("如何评价2025年度国家科学技术奖？", "科技"),
        ("强对流天气致灾性为何这么强？", "科学"),
        ("城乡三级养老服务网络如何落地？", "社会"),
        ("台积电加速赴美对台湾产业影响多大？", "财经"),
        ("弘扬科学家精神，我们该怎么做？", "教育"),
    ]),
]

for platform_name, items in platforms:
    lines = [f"**{platform_name}**"]
    for i, (title, tag) in enumerate(items, 1):
        lines.append(f"{i}. {title} `{tag}`")
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": "\n".join(lines)}
    })

elements.append({"tag": "hr"})

# ===== 板块三：跨平台热点 =====
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**🌐 三、跨平台热点**"}
})

cross_items = [
    ("防汛抗洪救灾", "微博 · 百度 · 抖音 · 知乎",
     "广西、湖北、甘肃等多地遭遇洪涝和地质灾害，全国上下齐心抗灾，成为各平台最关注话题。"),
    ("国家科学技术奖励大会", "微博 · 百度 · 知乎",
     "2025年度国家科学技术奖揭晓，习近平出席大会，弘扬科学家精神成为热议焦点。"),
    ("超强台风巴威", "微博 · 百度 · 抖音",
     "台风路径持续调整，沿海多地启动应急响应，停工停运停航引发广泛关注。"),
    ("世界杯赛事", "微博 · 抖音",
     "法国队姆巴佩表现出色，世界杯赛事持续占据社交平台热搜。"),
    ("暑期经济与消费券", "百度 · 抖音 · 知乎",
     "全国暑期文旅消费季启动，超4.5亿元消费券发放，各地暑期经济升温。"),
]

for title, platforms_str, desc in cross_items:
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {"tag": "lark_md", "content": f"**{title}**\n覆盖平台：{platforms_str}\n{desc}"}
        }]
    })

elements.append({"tag": "hr"})

card["elements"] = elements
card["note"] = {"tag": "plain_text", "content": "由 Incaier Agent 自动生成 | 数据来源：腾讯新闻、微博、百度、抖音、知乎"}

# 发送请求
resp = requests.post(
    WEBHOOK_URL,
    json={"msg_type": "interactive", "card": card},
    headers={"Content-Type": "application/json"}
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
result = resp.json()
print(f"Code: {result.get('code')}, Msg: {result.get('msg')}")