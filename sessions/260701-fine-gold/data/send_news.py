# -*- coding: utf-8 -*-
import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 每日新闻播报 — 2026年7月1日"},
        "template": "blue"
    },
    "elements": [],
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成"
    }
}

elements = card["elements"]

# Section 1
sec1 = {"tag": "div", "text": {"tag": "lark_md", "content": "**一、国内外要闻**\n"}}
elements.append(sec1)

news_items = [
    ("**庆祝中国共产党成立105周年大会在京隆重举行**\n7月1日上午在京举行，习近平会见白俄罗斯总统卢卡申科，各地开展主题党日活动迎七一。（来源：新华社、信阳日报）"),
    ("**李强签署国务院令，公布《退役军人就业创业促进条例》**\n新条例为退役军人提供就业创业支持，进一步健全退役军人服务保障体系。（来源：慧语简报）"),
    ("**程福波任国务院国资委党委书记**\n程福波正式出任国务院国有资产监督管理委员会党委书记。（来源：慧语简报）"),
    ("**2025年人口增长10强城市出炉，深圳增量第一**\n广东6城上榜，深圳以25.9万人增量位居首位，上海、苏州、北京、东莞排外贸前五。（来源：yyxw.com）"),
    ("**桂林市委原书记周家斌受贿1.98亿一审被判无期**\n河南省人大常委会原副主任刘满仓亦一审被判无期，退休后仍受贿1.7亿。（来源：慧语简报、yyxw.com）"),
    ("**7月1日起多项新规施行：快递包装不超2层/动力电池新国标**\n快递包装新规：非易碎品不超2层，易碎品不超4层；电动汽车动力蓄电池新国标要求不起火不爆炸。（来源：yyxw.com、网易）"),
    ("**保时捷在华持续收缩，确认终止多家门店销售业务**\n继此前收缩后，保时捷中国进一步削减门店数量，豪华车在华市场持续遇冷。（来源：慧语简报）"),
    ("**法国将于明年夏天前大选，空调议题或成关键胜负手**\n极端高温天气频发，空调普及率成为法国大选核心议题之一。（来源：慧语简报）"),
    ("**《网络测评活动规范》出台，让网络测评经得起检验**\n新规范针对网络测评乱象，要求测评内容真实、客观、可溯源。（来源：正义网）"),
    ("**香港廉署与警方打击假球赌博集团，拘捕19人**\n世界杯期间联合执法，打击跨境非法赌博活动。（来源：慧语简报）"),
]

for item in news_items:
    div = {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": item}}]}
    elements.append(div)

elements.append({"tag": "hr"})

# Section 2
sec2 = {"tag": "div", "text": {"tag": "lark_md", "content": "**二、各平台热搜 Top 5**\n"}}
elements.append(sec2)

platforms = [
    ("📱 微博热搜", [
        "1. #105年初心滚烫# 庆祝党的105岁生日（社会）",
        "2. 习近平推动中俄两国互信根基越扎越牢（时政）",
        "3. 《习近平的文化情缘》纪录片在老挝启播（文化）",
        "4. 加快推进贸易高质量发展（经济）",
        "5. 各地开展主题党日活动迎七一（社会）",
    ]),
    ("🔍 百度热搜", [
        "1. 庆祝中国共产党成立105周年大会（时政）",
        "2. 电动汽车动力蓄电池新国标7月1日施行（科技）",
        "3. 7月起快递包装新规实施（民生）",
        "4. 2025年人口增长10强城市出炉（社会）",
        "5. 程福波任国资委党委书记（时政）",
    ]),
    ("🎵 抖音热搜", [
        "1. 庆祝党的105岁生日（社会）",
        "2. 7月起开始实施这些新规（民生）",
        "3. AI帮忙填报高考志愿靠谱吗（科技）",
        "4. 上海暴雨预警（天气）",
        "5. 深中通道驾驶注意事项（交通）",
    ]),
    ("💡 知乎热榜", [
        "1. 电动汽车动力蓄电池新国标7月1日施行（科技）",
        "2. 7月新规盘点：快递包装新规等（社会）",
        "3. 《网络测评活动规范》出台（互联网）",
        "4. 保时捷在华持续收缩门店（财经）",
        "5. 法国大选空调议题成关键（国际）",
    ]),
]

for name, items in platforms:
    content = "**" + name + "**\n" + "\n".join(items)
    div = {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": content}}]}
    elements.append(div)

elements.append({"tag": "hr"})

# Section 3
sec3 = {"tag": "div", "text": {"tag": "lark_md", "content": "**三、跨平台热点**\n"}}
elements.append(sec3)

cross_items = [
    ("🔥 **庆祝中国共产党成立105周年**\n覆盖平台：微博、百度、抖音、知乎\n多地开展主题党日活动，全网致敬党的百年征程。"),
    ("🔥 **7月新规正式施行**\n覆盖平台：百度、抖音、知乎\n快递包装新规限制包装层数，动力电池新国标要求不起火不爆炸，一批新规影响日常生活。"),
    ("🔥 **中俄外交与高层互动**\n覆盖平台：微博、百度、六安新闻网\n习近平会见白俄罗斯总统，推动中俄两国互信根基越扎越牢，大国外交引关注。"),
]

for item in cross_items:
    div = {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": item}}]}
    elements.append(div)

resp = requests.post(webhook_url, json={"msg_type": "interactive", "card": card})
print("Status:", resp.status_code)
print("Response:", resp.text)