import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

news = [
    {
        "title": "A股热点高低切换，主要股指走势分化",
        "summary": "半导体、商业航天高位回调，券商、有色等传统行业反弹，上证跌0.17%，创业板涨0.54%。",
        "source": "上海证券报 | 2026-05-27"
    },
    {
        "title": "跌多涨少指数收红，市场分化加剧",
        "summary": "几十家跌停、300多家跌幅超5%，4000多家个股下跌，大盘在4150点位置失真。",
        "source": "腾讯新闻 | 2026-05-27"
    },
    {
        "title": "A股发出关键信号：PPO树脂满产满销，AI算力需求传导上游",
        "summary": "算力基建带火PPO树脂，PCB板块持续强势，英特尔加码玻璃基板量产。",
        "source": "证券之星 | 2026-05-27"
    },
    {
        "title": "周三早间三大重磅：美光暴涨、低空经济定调、商业航天提速",
        "summary": "美光单日暴涨19%市值破万亿美元，低空经济政策落地，鱼尾行情面临考验。",
        "source": "今日头条 | 2026-05-27"
    },
    {
        "title": "紧急提醒：A股高位震荡，机构资金分歧加剧",
        "summary": "外围利好难掩内部主力净流出，抱团松动、增量失真三大隐患显现。",
        "source": "网易财经 | 2026-05-27"
    },
    {
        "title": "元器件再创新高，大盘盘中调整与上周四有何不同",
        "summary": "三大指数涨跌不一，成交额3.26万亿放量374亿，大票风格受追捧。",
        "source": "每经网 | 2026-05-26"
    },
    {
        "title": "大盘收在4152站上10日均线，成交额重回3万亿",
        "summary": "指数站上10日均线短期向好，但个股普跌成常态，超跌板块补涨仍难。",
        "source": "老虎社区 | 2026-05-26"
    },
    {
        "title": "投资日历：周三资本市场大事提醒",
        "summary": "长鑫科技IPO上会，Meta年度会议，第十届集微半导体大会，500亿逆回购到期。",
        "source": "东方财富网 | 2026-05-27"
    },
    {
        "title": "AI短剧出海订单预计暴增5000%",
        "summary": "央视财经报道多家企业加码AI短剧出海布局，应用端有望迎来补涨行情。",
        "source": "央视财经 | 2026-05-27"
    },
    {
        "title": "证券时报今日导读：经开区高新区裁撤整合、广州收购二手房以旧换新",
        "summary": "夏季用电高峰关注电力设备股，宇树科技A股上市在即，网售处方药新规出台。",
        "source": "证券时报 | 2026-05-27"
    }
]

# Build card elements
elements = []
for i, item in enumerate(news):
    field_content = f"**{i+1}. {item['title']}**\n{item['summary']}\n*{item['source']}*"
    elements.append({
        "tag": "div",
        "fields": [{"is_short": False, "text": {"tag": "lark_md", "content": field_content}}]
    })
    elements.append({"tag": "hr"})

card = {
    "msg_type": "interactive",
    "card": {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": "\U0001F4C8 \u6BCF\u65E5\u80A1\u5E02\u7B80\u62A5\u00A0\u00A0|\u00A0\u00A02026\u5E745\u670827\u65E5"},
            "template": "red"
        },
        "elements": elements,
        "note": {
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": "\u7531 Incaier Agent \u81EA\u52A8\u751F\u6210\u00A0\u00A0|\u00A0\u00A0\u6570\u636E\u6765\u6E90\uFF1A\u516C\u5F00\u8D22\u7ECF\u5A92\u4F53"}]
        }
    }
}

resp = requests.post(webhook_url, json=card, headers={"Content-Type": "application/json; charset=utf-8"})
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
