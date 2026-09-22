import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 每日新闻播报 | 2026年6月11日 星期四"},
        "template": "blue"
    },
    "elements": [
        # ===== 板块一：国内外要闻 =====
        {"tag": "div", "text": {"tag": "lark_md", "content": "**一、🌍 国内外要闻**"}},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**美伊冲突再度升级 互相袭击军事目标**\n美方称打击伊朗防空系统等目标，伊朗革命卫队回击科威特境内美军基地，中东局势持续紧张，国际油价承压上行。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**SpaceX 最快明日登陆纳斯达克 史上最大IPO**\n计划6月12日挂牌，募资750亿美元，估值约1.765万亿美元，将成为全球资本市场有史以来规模最大的IPO。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**2026年全国高考落幕 1290万考生迎战**\n全国高考于6月7-10日举行，报名人数达1290万人。多地预计6月下旬公布成绩和录取分数线，考生纷纷庆祝迎接世界杯。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**5月CPI总体平稳 PPI继续上涨**\n我国5月居民消费价格指数总体平稳，工业生产者出厂价格指数继续上涨，5月汽车出口延续快速增长态势。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**全球科技股集体大跌 费城半导体指数重挫超10%**\n受美联储加息预期影响，美股、韩股、日股科技板块大幅下挫，引发市场对科技牛市是否终结的广泛讨论。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**微软发布新一代量子芯片 目标2029年造实用量子计算机**\n微软发布重大量子计算突破，计划在2029年前制造出实用的量子计算机，引发科技界广泛关注。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**以色列空袭黎巴嫩南部 刚果(金)埃博拉疫情持续**\n以军空袭黎巴嫩南部提尔地区；刚果(金)埃博拉确诊病例升至598例；联合国举行\"文明对话国际日\"主题活动。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**前5月期货市场累计成交额同比增长40.13%**\n全国期货市场保持活跃，1-5月累计成交额大幅增长。全国水路客运量达1.2亿人次，《2026中国海洋经济发展指数》发布。"}}]},
        {"tag": "hr"},
        # ===== 板块二：各平台热搜 Top 5 =====
        {"tag": "div", "text": {"tag": "lark_md", "content": "**二、🔥 各平台热搜 Top 5**"}},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**📱 微博热搜**\n1. 高考结束/出分倒计时 [社会/教育]\n2. SpaceX IPO 史上最大 [科技/财经]\n3. 美伊冲突局势升级 [国际/军事]\n4. 2026世界杯即将开幕 [体育]\n5. 全球科技股大跌引关注 [财经]"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**🎵 抖音热搜**\n1. 高考结束各地考生放飞 [社会/教育]\n2. 世界杯热身赛精彩瞬间 [体育]\n3. 梅西C罗第六次征战世界杯 [体育/娱乐]\n4. 高温预警多地超40°C [社会/生活]\n5. 美伊冲突最新动态 [军事/国际]"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**🔍 百度热搜**\n1. SpaceX IPO 估值1.7万亿 [财经/科技]\n2. 高考录取分数线预测 [教育]\n3. 美伊冲突中东局势 [军事/国际]\n4. 世界杯赛程表正式公布 [体育]\n5. 软银超越丰田登顶日本市值榜首 [财经]"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**💡 知乎热榜**\n1. 如何评价 SpaceX 上市及其估值？[科技/财经]\n2. 2026 年中美关系会走向何方？[国际/政治]\n3. 今年高考难度如何？题目有什么特点？[教育]\n4. 2026 世界杯夺冠热门球队分析 [体育]\n5. 美伊冲突前景与中东地缘格局 [军事/国际]"}}]},
        {"tag": "hr"},
        # ===== 板块三：跨平台热点 =====
        {"tag": "div", "text": {"tag": "lark_md", "content": "**三、📊 跨平台热点**"}},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**🔥 全平台热搜第一：SpaceX IPO**\n覆盖：微博 · 抖音 · 百度 · 知乎\n马斯克旗下SpaceX拟6月12日登陆纳斯达克，募资750亿美元，估值1.765万亿美元，引发全球资本圈和科技圈共同关注。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**⚔️ 美伊军事冲突升级**\n覆盖：微博 · 百度 · 知乎 · 抖音\n美军与伊朗互相打击对方军事目标，中东局势急剧升温，国际油价波动加剧，多国呼吁双方克制。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**⚽ 2026美加墨世界杯开幕在即**\n覆盖：微博 · 抖音 · 百度 · 知乎\n全部阵容确定，梅西、C罗第六次征战世界杯。高考结束后大批考生将成为观赛主力，"考完看世界杯"成热门话题。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**📝 2026年全国高考**\n覆盖：微博 · 百度 · 知乎 · 抖音\n全国1290万考生参试，各平台热议考题难度和录取分数线。高考结束标志着新一轮毕业季的开始。"}}]},
        {"tag": "div", "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": "**📉 全球科技股大幅回调**\n覆盖：微博 · 知乎 · 百度\n费城半导体指数单日重挫超10%，美联储加息预期升温引发科技股抛售潮，市场热议AI泡沫是否来临。"}}]},
    ],
    "note": {"tag": "plain_text", "content": "由 Incaier Agent 自动生成 · 数据来源：新闻联播、微博、抖音、百度、知乎"}
}

payload = {"msg_type": "interactive", "card": card}
resp = requests.post(webhook_url, json=payload, timeout=10)
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")