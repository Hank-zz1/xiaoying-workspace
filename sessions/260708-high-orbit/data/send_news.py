import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# Build card elements
elements = []

# Section 1: 国内外要闻
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**📌 一、国内外要闻**"
    }
})

news_items = [
    ("🇦🇷 世界杯：阿根廷3-2史诗逆转埃及，15分钟连进3球",
     "梅西扳平、劳塔罗绝杀，赛后埃及足协正式申诉裁判偏袒，埃及主帅炮轰"为商业保阿根廷"，主裁勒泰西耶关闭社媒。"),
    ("🏆 世界杯8强全部出炉：欧洲占6席",
     "法国、摩洛哥、西班牙、比利时、英格兰、挪威、阿根廷、瑞士晋级，三个东道主均止步。"),
    ("🕊️ 七七事变89周年：郑丽文在台北发声",
     "中国国民党主席郑丽文表示，民众要记得的不只是当年的耻辱，更要认清历史的教训。"),
    ("⛈️ 甘肃陇南滑坡致21人遇难",
     "7月7日宕昌县岷江林场发生滑坡，33人被困。截至8日上午确认21人遇难，救援仍在继续。"),
    ("🌊 台风"美莎克"重创广西，6死11失联",
     "台风在广西停留26小时，贵港高中近4000名师生被困，解放军冲锋舟救援。超强台风"巴威"逼近华东，江苏紧急暂停线下教学。"),
    ("🏗️ 我国人形机器人整机产量有望破十万台",
     "工信部数据显示，2026年上半年人形机器人产业发展迅猛，全年产量有望突破10万台。"),
    ("🚀 中国海军成功试射潜射战略导弹",
     "中方强调为例行试射不针对特定国家，日本连续发表两份声明，俄罗斯表态支持中国。"),
    ("🇺🇸 美军称开始对伊朗发动一系列有力打击",
     "伊朗南部格什姆岛及锡里克地区传出多次爆炸声，中东局势骤然紧张。"),
    ("📉 美股三大指数集体收跌，英特尔跌超9%",
     "道指跌0.25%，纳指跌1.16%，标普500跌0.45%，SpaceX跌超6%创IPO收盘新低。"),
    ("🏅 "七一勋章"第二次颁授，8人获党内最高荣誉",
     "这是继2021年建党百年首次颁授后，党中央第二次颁授"七一勋章"。"),
]

for title, desc in news_items:
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{title}**\n{desc}"
            }
        }]
    })

elements.append({"tag": "hr"})

# Section 2: 各平台热搜 Top 5
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**🔥 二、各平台热搜 Top 5**"
    }
})

platforms = [
    {
        "name": "🔵 百度热搜",
        "items": [
            ("1. 勋章无言 — 七一勋章颁授", "政治"),
            ("2. 世界杯8强出炉", "体育"),
            ("3. 埃及队赛后嘲讽阿根廷队", "体育"),
            ("4. 强对流天气如何避险？紧急提示", "社会"),
            ("5. 甘肃陇南滑坡致21人遇难", "社会"),
        ]
    },
    {
        "name": "🔴 头条热榜",
        "items": [
            ("1. 世界杯8强全部出炉", "体育"),
            ("2. 甘肃陇南滑坡共造成21人遇难", "社会"),
            ("3. 我国人形机器人整机产量有望破十万台", "科技"),
            ("4. 近4000名被困师生欢呼解放军来了", "社会"),
            ("5. 美军称开始对伊朗发动一系列有力打击", "军事"),
        ]
    },
]

for platform in platforms:
    platform_text = f"**{platform['name']}**\n"
    for item, tag in platform['items']:
        platform_text += f"  {item}  `{tag}`\n"
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": platform_text
            }
        }]
    })

elements.append({"tag": "hr"})

# Section 3: 跨平台热点
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**🌐 三、跨平台热点**"
    }
})

cross_platform = [
    ("⚽ 世界杯阿根廷vs埃及争议判罚",
     "覆盖：百度/头条/微博/抖音/知乎",
     "阿根廷3-2逆转埃及引发巨大争议，埃及足协申诉、球迷冲突、裁判被网暴关闭社媒，成为全网第一热点。"),
    ("⛈️ 甘肃陇南滑坡 & 台风/洪水灾害",
     "覆盖：百度/头条/微博",
     "陇南滑坡21人遇难，广西台风致6死11失联，湖北黄冈龙卷风，四川宜宾5.0级地震，多地遭遇极端天气。"),
    ("🚀 中国海军潜射导弹试射",
     "覆盖：百度/头条/微博",
     "中方例行试射引日本强烈反应，俄罗斯表态支持中国，地缘博弈持续升温。"),
    ("🇺🇸 美军打击伊朗 中东局势紧张",
     "覆盖：百度/头条",
     "伊朗南部传出多次爆炸声，美军宣布对伊朗发动打击，国际油价应声上涨。"),
    ("🤖 人形机器人产业爆发 & 美股科技股下跌",
     "覆盖：头条/百度",
     "中国人形机器人产量有望破十万台，但同时美股科技股集体下跌，英特尔跌超9%。"),
]

for title, platforms, desc in cross_platform:
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{title}**\n`{platforms}`\n{desc}"
            }
        }]
    })

# Build card JSON
card = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "📰 每日新闻播报 — 2026年7月8日"
        },
        "template": "blue"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成"
    }
}

payload = {
    "msg_type": "interactive",
    "card": card
}

resp = requests.post(webhook_url, json=payload, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")