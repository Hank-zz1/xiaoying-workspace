# -*- coding: utf-8 -*-
import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 构建富文本消息内容
message_content = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "每日播报 | 2026 年 5 月 14 日",
                "content": [
                    [
                        {"tag": "text", "text": "【国内外要闻】\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "1. 中美经贸磋商在韩国举行\n"}
                    ],
                    [
                        {"tag": "text", "text": "2. 4 月经济数据：CPI 涨 1.2%，新能源车渗透率首破 60%\n"}
                    ],
                    [
                        {"tag": "text", "text": "3. 医保基金监督检查五年行动计划印发\n"}
                    ],
                    [
                        {"tag": "text", "text": "4. 我国地震预警服务覆盖超 3.3 亿人\n"}
                    ],
                    [
                        {"tag": "text", "text": "5. 海南离岛免税新政半年增长 22.6%\n"}
                    ],
                    [
                        {"tag": "text", "text": "6. 第四代超导量子计算机上线\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【国际新闻】\n"}
                    ],
                    [
                        {"tag": "text", "text": "1. 美国总统特朗普访华\n"}
                    ],
                    [
                        {"tag": "text", "text": "2. 克宫称俄乌冲突已接近尾声\n"}
                    ],
                    [
                        {"tag": "text", "text": "3. 美国 4 月通胀率 3.8%\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【热搜榜 Top5】\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "微博：肖战/刘宇宁/王俊凯\n"}
                    ],
                    [
                        {"tag": "text", "text": "百度：中美磋商/特朗普访华/经济数据\n"}
                    ],
                    [
                        {"tag": "text", "text": "知乎：中美磋商/经济数据/新能源车\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "----------------\n生成时间：09:30"}
                    ]
                ]
            }
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(webhook_url, headers=headers, json=message_content, timeout=30)
result = response.json()

print(f"Status: {response.status_code}")
print(f"Result: {json.dumps(result, ensure_ascii=False)}")

if result.get("code") == 0:
    print("Success!")
else:
    print(f"Failed: {result}")
