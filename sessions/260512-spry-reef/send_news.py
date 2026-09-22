# -*- coding: utf-8 -*-
import requests
import json

# 飞书 Webhook URL (从 memory 中获取)
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 新闻内容 - 2026 年 5 月 11 日
news_content = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "新闻播报 | 2026 年 5 月 11 日",
                "content": [
                    [
                        {"tag": "text", "text": "【国内要闻】\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "1. 特朗普将于 5 月 13-15 日对中国进行国事访问\n"}
                    ],
                    [
                        {"tag": "text", "text": "2. 天舟十号货运飞船发射成功，已与空间站完成对接\n"}
                    ],
                    [
                        {"tag": "text", "text": "3. 长三角一体化发展取得新突破，十五五开局良好\n"}
                    ],
                    [
                        {"tag": "text", "text": "4. 两高发布司法解释：惩治非法占用耕地行为 (5 月 18 日起施行)\n"}
                    ],
                    [
                        {"tag": "text", "text": "5. 经济数据：4 月 CPI 同比上涨 1.2%，新能源汽车销量增长 9.7%\n"}
                    ],
                    [
                        {"tag": "text", "text": "6. 伦敦世乒赛：中国队包揽男女团双冠\n"}
                    ],
                    [
                        {"tag": "text", "text": "7. 沪指站上 4200 点，创近 11 年新高\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【国际要闻】\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "1. 伊朗要求美国解除海上封锁，美方称回应不可接受\n"}
                    ],
                    [
                        {"tag": "text", "text": "2. 普京：乌克兰冲突正接近尾声\n"}
                    ],
                    [
                        {"tag": "text", "text": "3. 俄驻日大使：俄日关系陷入冰河期\n"}
                    ],
                    [
                        {"tag": "text", "text": "4. 沙特：全球石油供应两个月减少约 10 亿桶\n"}
                    ],
                    [
                        {"tag": "text", "text": "5. 法国颁布简化归还非法所得文物法律\n"}
                    ],
                    [
                        {"tag": "text", "text": "6. 第十一届法国中国电影节在巴黎开幕，17 部国产影片将展映\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "日期：2026 年 5 月 12 日 星期二"}
                    ]
                ]
            }
        }
    }
}

# 发送请求
headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, json=news_content, headers=headers)

print("发送状态码:", response.status_code)
print("响应内容:", response.text)

if response.status_code == 200:
    result = response.json()
    if result.get("code") == 0 or result.get("StatusCode") == 0:
        print("消息发送成功!")
    else:
        print("发送失败:", result)
else:
    print("HTTP 错误:", response.status_code)
