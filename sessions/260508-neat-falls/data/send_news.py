import requests
import json
import sys

# 设置 UTF-8 编码输出
sys.stdout.reconfigure(encoding='utf-8')

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 富文本消息格式
payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "5 月 7 日新闻播报",
                "content": [
                    [
                        {"tag": "text", "text": "【国内要闻】\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 习近平总书记强调能源保障和安全事关国计民生，我国加快推进新型能源体系建设\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 李强分别会见乌兹别克斯坦总理、美国国会参议员代表团\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 五一假期国内出游 3.25 亿人次，同比增长 3.6%\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 4 月末我国外汇储备 34105 亿美元，连续 9 个月稳定在 3.3 万亿美元之上\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 天舟九号货运飞船顺利撤离空间站并受控再入大气层\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 一季度我国机器人出口 113.2 亿元，清洁机器人成出口主力\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【国际要闻】\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 美国总统称对美伊达成协议表示乐观，伊朗称美国必须赔偿损失\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 俄外交部呼吁各国准备好及时从基辅撤离人员\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 黎以停火后以军首次空袭黎首都贝鲁特\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 法国民议会通过简化非法文物归还草案\n"}
                    ],
                    [
                        {"tag": "text", "text": "- 洪迪厄斯号汉坦病毒确诊病例上升\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "—— 小盈早报 · 2026 年 5 月 8 日"}
                    ]
                ]
            }
        }
    }
}

response = requests.post(webhook_url, json=payload)
result = response.json()

if result.get("code") == 0:
    print("[SUCCESS] 消息发送成功!")
else:
    print(f"[ERROR] 消息发送失败：{result}")
