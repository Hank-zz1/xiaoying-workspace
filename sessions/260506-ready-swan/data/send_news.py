# -*- coding: utf-8 -*-
"""
新闻播报发送脚本 - 发送到飞书 iHaier 群
"""

# 2026 年 5 月 5 日新闻联播及海内外重要新闻摘要

news_content = """📰 新闻播报 2026 年 5 月 5 日

【国内要闻】
1. 习近平对湖南长沙浏阳市烟花厂爆炸事故作出重要指示，要求抓好风险隐患排查整治，加强公共安全管理
2. "五一"假期全社会跨区域人员流动量预计超 15 亿人次，创历史同期新高
3. "五一"假期消费活力持续释放，入境游升温
4. 第 139 届广交会闭幕，"华龙一号"太平岭核电厂 2 号机组进入带核调试阶段
5. 我国数据基础设施已覆盖 15 个行业
6. 立夏时节各地抢抓农时，强化科技支撑夯实粮食生产基础

【国际新闻】
1. 中东局势紧张：美伊在霍尔木兹海峡对峙，阿联酋富查伊拉石油工业区遭伊朗无人机袭击
2. 国际油价大涨：美油收涨 3.14% 报 105.14 美元/桶，布油涨 5.24% 报 113.84 美元/桶
3. 贵金属期货收跌：COMEX 黄金跌 2.41% 报 4532.40 美元/盎司
4. 中国代表在联合国指出：国际社会应高度警惕日本涉核消极动向
5. 美国称将推进对欧盟汽车加征关税计划，欧方表示将予以反制
6. 俄乌分别宣布本周将实施停火
7. 欧洲政治共同体峰会聚焦加强自主

【财经简讯】
• 港交所正准备重启黄金期货交易
• Coinbase 以推进 AI 转型为由裁员 14%
"""

# 用户需要提供 Webhook URL
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

if not webhook_url:
    print("请提供飞书 Webhook URL")
    exit(1)

import requests

payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "📰 新闻播报 2026 年 5 月 5 日",
                "content": [
                    [{"tag": "text", "text": news_content}]
                ]
            }
        }
    }
}

response = requests.post(webhook_url, json=payload)
print(f"发送状态：{response.status_code}")
print(f"响应内容：{response.text}")
