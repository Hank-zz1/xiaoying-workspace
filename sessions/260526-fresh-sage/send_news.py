import requests
import json
import traceback

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📰 每日新闻播报 — 2026年5月26日"},
        "template": "blue"
    },
    "elements": [
        # ===== 板块一：国内外要闻 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "📌 **一、国内外要闻**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**1. 习近平会见塞尔维亚总统、巴基斯坦总理**\n习近平举行仪式欢迎塞尔维亚总统武契奇访华并会谈；会见巴基斯坦总理夏巴兹，大国外交\"北京时间\"持续。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**2. 神舟二十三号发射成功，太空会师**\n5月24日23时08分，神舟二十三号载人飞船发射圆满成功，朱杨柱、张志远、黎家盈三名航天员顺利进入中国空间站，两个乘组完成第8次\"太空会师\"。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**3. 《习近平谈治国理政》第五卷多文版出版**\n法、俄、阿、西、葡、德、日及中文繁体8个文版由外文出版社出版，面向海内外发行。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**4. 重庆永川暴雨致9死11失联**\n重庆永川遭遇特大暴雨灾害，各地各部门积极应对持续强降雨，网警发布防汛抗灾网络文明倡议书。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**5. 美伊谈判取得进展，国际油价大跌**\n美伊就资产解冻问题达成谅解，霍尔木兹海峡航运有望全面恢复，WTI原油跌破90美元/桶，布伦特跌7.2%。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**6. 宇树科技冲刺\"人形机器人第一股\"**\n宇树科技科创板IPO于6月1日上会，3月获受理并完成两轮问询答复。Q1扣非净利润下滑超五成。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**7. 华为发布半导体\"韬(τ)定律\"**\n华为董事何庭波在ISCAS 2026发表主旨演讲，提出半导体产业新指导原则，预计2031年达1.4纳米制程。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**8. 第22届文博会闭幕，AI亮点纷呈**\n深圳文博会闭幕，AI\"智\"爆全场吸引全球客商，再次彰显\"中国文化产业第一展\"标杆地位。"}},
            ]
        },
        {"tag": "hr"},
        # ===== 板块二：各平台热搜 Top 5 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "🔥 **二、各平台热搜 Top 5**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🔵 微博热搜**\n1. 这一幕中塞铁杆友谊具象化了 [社会]\n2. 戴耳环引争议女干部回应恶评 [社会]\n3. iPhone20原型机偷跑 [科技]\n4. 智能机器人加速走进日常生活 [科技]\n5. 郑钦文vs赫瓦林斯卡 [体育]"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🎵 抖音热点**\n1. 中方强烈谴责巴基斯坦恐袭事件 [时政]\n2. 第一视角看神舟二十三号发射 [科技]\n3. 中国盾构机向世界输出中国方案 [科技]\n4. 重庆永川暴雨致9死11失联 [社会]\n5. 山西煤矿爆炸瞬间监控曝光 [社会]"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**💡 知乎热榜**\n1. 静音车厢柔性劝阻该升级硬性管理吗？[社会]\n2. NBA在国内怎么没什么热度了？[体育]\n3. 美伊达成谅解，中东局势会降温吗？[国际]\n4. 于正称《给阿嬷的情书》为\"超级商业片\" [娱乐]\n5. \"天才少年\"熊羽诺去大专任教引热议 [教育]"}},
            ]
        },
        {"tag": "hr"},
        # ===== 板块三：跨平台热点 =====
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "🔗 **三、跨平台热点**"}
        },
        {
            "tag": "div",
            "fields": [
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🚀 神舟二十三号太空会师**\n覆盖：新闻联播 / 微博 / 抖音 / 知乎\n中国航天第8次\"太空会师\"，三名航天员顺利入驻中国空间站。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🌍 美伊谈判与油价暴跌**\n覆盖：新闻联播 / 微博 / 知乎\n美伊就资产解冻达成谅解，国际油价大跌超6%，霍尔木兹海峡航运有望恢复。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🌧️ 重庆永川特大暴雨**\n覆盖：抖音 / 微博 / 新闻\n暴雨致9死11失联，多部门紧急响应防汛抗灾。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**🇨🇳 中塞外交\"铁杆友谊\"**\n覆盖：新闻联播 / 微博\n塞尔维亚总统武契奇访华，两国元首会谈，中塞关系再升温。"}},
                {"is_short": False, "text": {"tag": "lark_md", "content": "**⛏️ 山西煤矿爆炸事故**\n覆盖：抖音 / 新闻\n山西煤矿爆炸瞬间监控曝光，山西省安委会召开扩大会议部署安全整治。"}},
            ]
        },
        {"tag": "hr"},
        {
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": "🤖 由 Incaier Agent 自动生成 | 数据来源：新闻联播、微博、抖音、知乎、百度热搜"}]
        }
    ]
}

payload = {
    "msg_type": "interactive",
    "card": card
}

try:
    resp = requests.post(webhook_url, json=payload, timeout=15)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    if resp.status_code == 200:
        print("✅ 飞书卡片发送成功！")
    else:
        print(f"❌ 发送失败: {resp.text}")
except Exception as e:
    print(f"❌ 异常: {e}")
    traceback.print_exc()