import requests
import json
from datetime import datetime

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 整理新闻内容
news_content = """📰 **新闻早报 | 2026 年 5 月 7 日**

━━━━━━━━━━━━━━━━━━━

🇨🇳 **国内要闻**

• 消费市场活力迸发 — "五一"假期商品消费迭代焕新，服务消费持续升温

• 王沪宁会见孟加拉国外交部长卡利勒

• "十五五"规划 — 广西、浙江举行专题新闻发布会

• 人员流动量创新高 — "五一"假期全社会跨区域人员流动量达 15.17 亿人次，同比增长 3.49%

• 机器人出口开门红 — 一季度我国机器人出口实现良好开局

• 支付交易 7.85 万亿 — "五一"假期银联网联处理支付数据

• 海南离岛免税 — 购物金额 5.54 亿元

• 数据领域国际合作 — 上海综合试点正式启动

• 半导体板块大涨 — A 股半导体板块 29 只个股创历史新高

━━━━━━━━━━━━━━━━━━━

🌍 **国际新闻**

• 日本和平团体集会 — 抗议日本政府一系列危险动向

• 美伊谈判 — 伊朗称施压不会成功；美国称就全面协议取得重大进展

• 欧盟敦促美国遵守已有贸易协议

• 汉坦病毒邮轮 — "洪迪厄斯"号感染病例增至 8 人

• 印尼车祸 — 客车与油罐车相撞至少 16 人死亡

• 霍尔木兹局势 — 外交部：只有全面止战才能缓解紧张

━━━━━━━━━━━━━━━━━━━

☀️ 新的一天，加油！
"""

payload = {
    "msg_type": "text",
    "content": {
        "text": news_content
    }
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
result = response.json()

print(f"发送状态码：{response.status_code}")
print(f"返回结果：{result}")

if result.get("code") == 0:
    print("Success: 消息发送成功！")
else:
    print(f"Failed: 消息发送失败：{result}")
