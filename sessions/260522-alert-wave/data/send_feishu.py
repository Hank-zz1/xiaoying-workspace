import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

news_items = [
    {
        "title": "A股三大指数全线下挫，沪指失守4100点",
        "summary": "5月21日市场冲高回落，三大指数均跌超2%，科创50跌超3%，近4800只个股下跌。",
        "source": "证券时报网 / 2026-05-21"
    },
    {
        "title": "沪深两市成交额达3.48万亿",
        "summary": "5月21日沪深两市成交额达3.48万亿元，市场交投活跃度维持高位。",
        "source": "南方财富网 / 2026-05-21"
    },
    {
        "title": "沪指午盘震荡走高，创业板指涨近2%",
        "summary": "5月22日早盘沪指涨0.47%报4096点，深成指涨1.39%，超3600股飘红，成交约1.79万亿。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "金利华电连续3日20%涨停，公司发风险提示",
        "summary": "金利华电连续3个交易日20%涨停报52.87元，公司公告称股价严重偏离基本面，存在炒作风险。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "\"十五五\"新型储能发展实施方案编制完成",
        "summary": "方案已编制完成正在内部征求意见，待意见征求完毕后将正式发布。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "联想集团第四财季净利润同比增479.5%",
        "summary": "联想第四财季营收1495.4亿元同比增27.1%，全年营收5899亿元同比增20%，股价大涨14%创新高。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "智谱发布GLM-5.1高速版API",
        "summary": "面向企业客户提供GLM-5.1-highspeed，输出速度达400 tokens/s，刷新全球大模型API速度上限。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "湖南裕能拟赴港上市推进全球化战略",
        "summary": "头部锂电厂商湖南裕能筹划发行H股并在香港联交所上市，打造国际化资本平台。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "康尼机电成立新公司含AI及机器人业务",
        "summary": "江苏睿达科技成立，经营范围包含智能机器人研发、人工智能应用软件开发等。",
        "source": "证券时报网 / 2026-05-22"
    },
    {
        "title": "APEC贸易部长会议开幕，讨论区域经济一体化",
        "summary": "会议围绕建设亚太共同体、推进区域经济一体化、数字合作和绿色经济等议题展开讨论。",
        "source": "证券时报网 / 2026-05-22"
    },
]

# 构建卡片元素
elements = []
for i, item in enumerate(news_items):
    # 新闻内容块
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{item['title']}**\n{item['summary']}\n*{item['source']}*"
            }
        }]
    })
    # 分割线（最后一条不加）
    if i < len(news_items) - 1:
        elements.append({"tag": "hr"})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "📈 每日股市简报 - 2026年5月22日"},
        "template": "red"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成"
    }
}

payload = {
    "msg_type": "interactive",
    "card": card
}

resp = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"})
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")