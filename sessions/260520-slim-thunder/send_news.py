import json, requests

with open("data/news_card.json", "r", encoding="utf-8") as f:
    card = json.load(f)

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"
resp = requests.post(webhook_url, json=card, timeout=15)
print(f"Status: {resp.status_code}")
j = resp.json()
print(f"Code: {j.get('code')}, Msg: {j.get('msg')}")
print("SUCCESS" if j.get("code") == 0 else "FAILED")