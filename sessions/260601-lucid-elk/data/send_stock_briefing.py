import json, requests, sys

data_file = sys.argv[1]
with open(data_file, 'r', encoding='utf-8') as f:
    news_items = json.load(f)

elements = []
for i, item in enumerate(news_items):
    elements.append({
        "tag": "div",
        "fields": [{
            "is_short": False,
            "text": {
                "tag": "lark_md",
                "content": f"**{i+1}. {item['title']}**\n{item['summary']}\n{chr(0x1F4CE)} {item['source']}"
            }
        }]
    })
    if i < len(news_items) - 1:
        elements.append({"tag": "hr"})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": f"{chr(0x1F4C8)} 每日股市简报 \u2014 2026年6月1日"},
        "template": "red"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成 | 数据来源：新浪财经、东方财富、证券之星、富途牛牛等"
    }
}

resp = requests.post(
    "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9",
    json={"msg_type": "interactive", "card": card},
    headers={"Content-Type": "application/json"}
)
print(f"Status: {resp.status_code}")
print(resp.text[:200])