import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 构建富文本消息内容
payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "📰 每日播报 · 2026 年 5 月 13 日",
                "content": [
                    [
                        {"tag": "text", "text": "📅 日期：2026 年 5 月 13 日 星期三\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "📺 新闻联播速览（5 月 12 日）\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【外交动态】\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 习近平欢迎塔吉克斯坦总统访华并举行会谈\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 习近平会见文莱王储、联合国教科文组织总干事\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 李强会见塔吉克斯坦总统，祝贺毛焦尔任匈牙利总理\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 赵乐际会见塔吉克斯坦总统，韩正同文莱王储会谈\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【国内要闻】\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 我国未来产业布局提速，农村供水保障水平提升\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 防灾减灾科普教育开展，护士队伍持续壮大\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 2026 世界数字教育大会发布八项成果\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 西十高铁全线拉通试验启动\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 东北最长跨海大桥主线钢栈桥首段合龙\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【国际焦点】\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 国际社会关注中美元首会晤\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 伊朗呼吁美国接受其方案\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 日本实际家庭消费连续 4 个月下滑\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "🔥 全网热点 Top 5\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【微博热搜】\n"}
                    ],
                    [
                        {"tag": "text", "text": "1. #孙颖莎 11350 分女单世一# 🏓 体育\n"}
                    ],
                    [
                        {"tag": "text", "text": "2. 樊振东加盟杜塞上百家企业竞价赞助 🏓 体育\n"}
                    ],
                    [
                        {"tag": "text", "text": "3. 从 4 月先行指标看我国经济持续向好 📈 财经\n"}
                    ],
                    [
                        {"tag": "text", "text": "4. 白鹿演唱会过审 🎤 娱乐\n"}
                    ],
                    [
                        {"tag": "text", "text": "5. 4 月汽车销量前 10 仅 1 款油车 🚗 汽车\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【抖音热点】\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 抖音求真辟谣：山西忻州车祸系谣言\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 明星热度榜：张凌赫、王一博等\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "【知乎热榜】\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 盐言故事《错嫁有喜》登古偶短剧热度 TOP1\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "📊 跨平台热点分析\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 体育赛事：孙颖莎、樊振东动态引发全网关注\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 经济数据：4 月经济指标、汽车销量持续热度\n"}
                    ],
                    [
                        {"tag": "text", "text": "• 娱乐明星：白鹿、张凌赫、王一博等受关注\n\n"}
                    ],
                    [
                        {"tag": "text", "text": "—— 小盈 · 每日播报 ——"}
                    ]
                ]
            }
        }
    }
}

# 发送请求
response = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"})
result = response.json()

print(f"发送状态码：{response.status_code}")
print(f"发送结果：{result}")

if result.get("code") == 0 or result.get("StatusCode") == 0 or result.get("Extra") == "success":
    print("\n[OK] 消息发送成功！")
else:
    print(f"\n[Error] 消息发送失败：{result}")
