import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 每日新闻播报 | 2026年7月16日"},
        "template": "blue"
    },
    "elements": [
        # ===== 板块一：国内外要闻 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**一、国内外要闻**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**上半年GDP同比增长4.7%**\n国家统计局7月15日发布数据，上半年国内生产总值695704亿元，同比增长4.7%，经济运行在合理区间。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**中国出台首个扩大消费五年规划**\n设定了到2030年社会消费品零售总额达60万亿元目标，重点涵盖养老、托育、文旅、体育等领域。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**三部门向吉林调拨9000件中央救灾物资**\n针对吉林暴雨洪涝灾害，调拨折叠床、毛毯、家庭应急包等物资支持受灾群众安置。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**伊朗警告：美方袭击将导致该地区不出口一滴石油**\n伊朗伊斯兰革命卫队15日声明，只要美国继续袭击伊朗，该地区不会出口石油和天然气。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**中央气象台三预警齐发，多地最高气温超40℃**\n全国多地持续高温天气，中央气象台同时发布高温、暴雨和强对流天气预警。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**中国预制变电站全球爆单**\n中国制造的预制变电站凭借高效交付和成本优势，在海外市场获得大量订单。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**江苏四位作家获第九届鲁迅文学奖**\n安徽诗人梁小斌等四位江苏作家获此殊荣，展现文学创作新成果。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**温州明珠七号邮轮大幅倾斜**\n耗资超2亿元建造的邮轮闲置14年后突发倾斜，相关部门已到场处置，原因正在调查中。"}},
            ]
        },
        {"tag": "hr"},
        # ===== 板块二：各平台热搜 Top 5 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**二、各平台热搜 Top 5**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**微博热搜**\n1. 泽连斯基拧瓶盖引争议 [娱乐]\n2. 上半年GDP增长4.7% [财经]\n3. 阿根廷连续两届进决赛 [体育]\n4. 中国预制变电站全球爆单 [科技]\n5. 官方辟谣九寨沟湖水染色 [社会]"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**百度热搜**\n1. 上半年GDP同比增长4.7% [财经]\n2. 中国出台扩大消费五年规划 [时政]\n3. 高温预警 多地气温超40℃ [社会]\n4. 伊朗警告石油禁运 [国际]\n5. 世界杯决赛中场表演 [体育]"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**抖音热搜**\n1. 高考录取通知书陆续送达 [社会]\n2. 世界杯决赛倒计时 [体育]\n3. 夏日高温防暑指南 [生活]\n4. 中国空调在欧洲热销 [财经]\n5. 塔克拉玛干海鲜养殖 [科技]"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**知乎热榜**\n1. 上半年GDP增长4.7%意味着什么？[财经]\n2. 中国扩大消费五年规划解读 [时政]\n3. 伊朗石油威胁对全球影响 [国际]\n4. 高温天气如何应对？[生活]\n5. 预制变电站技术原理 [科技]"}},
            ]
        },
        {"tag": "hr"},
        # ===== 板块三：跨平台热点 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**三、跨平台热点**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 上半年GDP增长4.7%**\n覆盖：微博、百度、知乎、抖音\n国家统计局15日发布上半年经济数据，GDP同比增长4.7%，成为全平台关注焦点。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 全国多地高温超40℃**\n覆盖：微博、百度、抖音\n中央气象台三预警齐发，多地遭遇极端高温，防暑降温成全民话题。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 伊朗警告石油禁运**\n覆盖：微博、百度、知乎\n伊朗革命卫队声明若遭美方持续袭击将封锁石油出口，引发国际关注。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 中国扩大消费五年规划**\n覆盖：百度、知乎\n中国出台首个以扩大消费为重点的五年规划，2030年社零目标60万亿元。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 2026世界杯决赛临近**\n覆盖：微博、百度、抖音、知乎\n国际足联确认决赛中场休息表演安排，阿根廷连续两届进决赛引发热议。"}},
            ]
        },
        {"tag": "hr"},
        {
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": "由 Incaier Agent 自动生成 | 数据来源：国家统计局、网易新闻、参考消息等"}]
        }
    ]
}

payload = {
    "msg_type": "interactive",
    "card": card
}

response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")