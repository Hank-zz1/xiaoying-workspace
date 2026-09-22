import json, requests, sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    card = json.load(f)

payload = {"msg_type": "interactive", "card": card}
resp = requests.post(
    "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9",
    json=payload,
    timeout=10
)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")