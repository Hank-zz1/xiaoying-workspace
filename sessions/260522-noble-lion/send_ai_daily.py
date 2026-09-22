import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

card = {
    "msg_type": "interactive",
    "card": {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "AI 产品/技术日报 | 2026年5月22日"},
            "template": "green"
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**OpenAI 正式推送 GPT-5.5 全量版本**\nInstant 版面向所有用户免费开放，幻觉率下降 52.5%，推理速度提升 3 倍，上下文突破 100 万 Token。（来源：搜狐 · 5月20日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**阿里云发布全新 AI 产品官网「千问云」**\n上线 150+ 主流模型 API（Qwen/GLM/Kimi/DeepSeek 等），封装为 Agent 可调用的 Skills 与 CLI 工具。（来源：新浪财经 · 5月20日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**中国 AI 大模型周调用量达美国 2.1 倍**\nOpenrate 统计 5月4-10日中国周调用量 7.941 万亿 Token，远超美国 3.76 万亿，彰显 AI 产业活跃度。（来源：搜狐 · 5月20日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**腾讯混元 Hy3 登顶 OpenRouter 全球榜首**\n周调用量环比增长 799%，工具调用场景全球第一、代码生成全球第二，综合性能领先同参数量级模型。（来源：新华网 · 5月18日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**DeepSeek 完成创纪录融资，估值突破 500 亿美元**\n国家大基金领投、腾讯跟投，最高募资 500 亿元，21 天估值从 100 亿飙至 500 亿美元。（来源：科创板日报 · 5月18日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**Claude 收入同比增长 80 倍，编程市场份额达 54%**\nClaude Code 年收入达 25 亿美元，超越 OpenAI 成为企业市场采用率第一的 AI 工具。（来源：非凡产研 · 5月18日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**AI 终端智能化分级国家标准正式发布**\n工信部等联合发布 GB/Z 177—2026 标准，统一手机/电脑/电视等 AI 终端评价体系。（来源：新华网 · 5月15日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**百度发布文心大模型 5.1，训练成本仅行业 6%**\n「多维弹性预训练」技术实现效率跃升，总参数压缩至 1/3，以极致性价比达到领先水平。（来源：CSDN · 5月9日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**谷歌 Gemini 2.5 Pro 登顶 AI 编程评测**\n在 WebDev Arena 以 1499.95 分超越 Claude 3.7 Sonnet（1377分），单条提示即可生成完整 Web 应用。（来源：CSDN · 5月7日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**宇树科技 UniStore 全球上线，首个人形机器人应用商店**\n含用户广场、动作库、数据集、开发者中心四大模块，首批收录扭扭舞等热门技能包。（来源：CSDN · 5月7日）"
                        }
                    }
                ]
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**Anthropic 估值逼近 1 万亿美元，AI 格局加速重塑**\n融资 300 亿美元，OpenAI ChatGPT 周活用户突破 9 亿，产业竞争进入白热化。（来源：网易科技 · 5月15日）"
                        }
                    }
                ]
            }
        ],
        "note": {
            "tag": "plain_text",
            "content": "由 Incaier Agent 自动生成 | 数据综合自搜狐、新浪、新华网、CSDN等"
        }
    }
}

resp = requests.post(webhook_url, json=card, timeout=10, headers={"Content-Type": "application/json; charset=utf-8"})
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")