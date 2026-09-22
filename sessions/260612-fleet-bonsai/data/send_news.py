import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# Build card elements
elements = []

# ===== 板块一：国内外要闻 =====
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**📌 一、国内外要闻**"
    }
})

news_items = [
    ("🌍 伊朗宣布关闭霍尔木兹海峡",
     "美军空袭伊朗南部目标后，伊朗全面封锁海峡，全球能源航运受冲击。特朗普称美伊协议或本周末签署。"),
    ("⚽ 2026美加墨世界杯揭幕战",
     "墨西哥2:0战胜南非，打破96年「世界杯揭幕战东道主不败」魔咒，夏奇拉开幕式献唱。"),
    ("💥 广西兴安县发生爆炸致7死17伤",
     "警方已排除管道燃气等因素引起，事故原因仍在调查中。"),
    ("🏦 欧洲央行宣布加息25个基点",
     "存款便利利率升至1.85%，IMF下调欧元区2026年GDP增长预测至0.9%。"),
    ("🚀 SpaceX创纪录IPO上市",
     "贝莱德已下达至少50亿美元认购订单，华尔街热捧与质疑交织，市值预期达2.2万亿美元。"),
    ("📉 现货黄金跌破4200美元关口",
     "黄金进入技术性熊市，国内金饰克价跌至1280元左右。"),
    ("🇬🇧 英国掀起反移民抗议潮",
     "欧洲多国升级边境管控，反移民情绪持续蔓延。"),
    ("🔬 中国海事扫测完成台岛东部海底地图",
     "首次补齐台岛东部海底地形数据，为海洋科学研究与航运安全提供重要支撑。"),
    ("🏓 孙颖莎登《时代》百大体育榜",
     "全球唯一上榜的乒乓球选手，中国乒乓球再获国际认可。"),
    ("🇷🇸 武契奇称计划很快辞职",
     "塞尔维亚总统武契奇公开表态，引发巴尔干地区政治关注。"),
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

# ===== 板块二：各平台热搜 Top 5 =====
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**🔥 二、各平台热搜 Top 5**"
    }
})

platforms = [
    {
        "name": "📱 微博热搜",
        "items": [
            ("1. 香港大火 洗黑钱4000万", "社会"),
            ("2. 黄金进入熊市", "财经"),
            ("3. 特朗普说今晚将重创伊朗", "国际"),
            ("4. 莫离热度", "娱乐"),
            ("5. 张新成演技", "娱乐"),
        ]
    },
    {
        "name": "📢 百度热搜",
        "items": [
            ("1. 世界杯迎来最不吃压力的中国裁判", "体育"),
            ("2. 中宣部制裁菲律宾国防部长", "时政"),
            ("3. 高考报志愿 考生最关心的都在这里", "教育"),
            ("4. 微信新功能上线 被赞工作党福音", "科技"),
            ("5. 特朗普称取消对伊猛烈打击 伊朗回应", "国际"),
        ]
    },
    {
        "name": "🎵 抖音热搜",
        "items": [
            ("1. 世界杯开幕式「大半夜吓我一跳」", "体育"),
            ("2. 女子外卖备注牛蛙不要烧收到活蛙", "社会"),
            ("3. 北京天气好像开了挂", "生活"),
            ("4. 高速上徒手拖走80斤铁架司机找到了", "社会"),
            ("5. 夏奇拉开幕式献唱燃爆全场", "娱乐"),
        ]
    },
    {
        "name": "💡 知乎热榜",
        "items": [
            ("1. 欧洲央行加息对全球经济有何影响", "财经"),
            ("2. 2026世界杯揭幕战如何评价", "体育"),
            ("3. SpaceX IPO对科技行业意味着什么", "科技"),
            ("4. 美伊冲突会升级为全面战争吗", "国际"),
            ("5. 如何看待AI行业最新动态", "科技"),
        ]
    },
]

for p in platforms:
    items_text = "\n".join([f"{item}（{tag}）" for item, tag in p["items"]])
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{p['name']}**\n{items_text}"
            }
        }]
    })

elements.append({"tag": "hr"})

# ===== 板块三：跨平台热点 =====
elements.append({
    "tag": "div",
    "text": {
        "tag": "lark_md",
        "content": "**🔗 三、跨平台热点**"
    }
})

cross_platform = [
    ("美伊冲突与中东局势升级",
     "覆盖：微博、百度、知乎、抖音、财联社、华尔街见闻\n美军空袭伊朗，伊朗封锁霍尔木兹海峡，特朗普称协议或本周末签署，全球关注。"),
    ("2026美加墨世界杯开幕",
     "覆盖：微博、百度、抖音、知乎、B站、头条\n揭幕战墨西哥2:0南非，夏奇拉献唱，中国裁判亮相，全网热议。"),
    ("SpaceX创纪录IPO上市",
     "覆盖：财联社、华尔街见闻、IT之家、百度、头条\n贝莱德50亿美元认购，市值预期2.2万亿美元，科技与财经领域共同关注。"),
    ("高考结束·志愿填报季",
     "覆盖：百度、微博、知乎、抖音\n高考落幕，志愿填报、专业选择成为毕业生和家长关注焦点。"),
    ("欧洲央行加息与全球金融市场",
     "覆盖：财联社、华尔街见闻、金十数据、知乎\n欧央行加息25基点，黄金进入熊市，全球市场波动加剧。"),
]

for title, desc in cross_platform:
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

# Build card
card = {
    "config": {
        "wide_screen_mode": True
    },
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "📰 每日新闻播报 | 2026年6月12日"
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

resp = requests.post(webhook_url, json=payload, timeout=15)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
