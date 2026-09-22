---
name: "飞书 iHaier 通知"
description: "通过飞书 Webhook 机器人向 iHaier 群组发送消息通知，支持 @ 指定用户。当用户提到'发送到我iHaier'、'发我iHaier'、'发到iHaier'、'发iHaier'、'发个通知'或类似发送消息到iHaier的请求时使用此技能。"
---

# 飞书 iHaier 通知技能

通过飞书 Webhook 机器人向 iHaier 群组发送消息通知。

## 使用场景

当用户提出以下需求时触发此技能：
- "发送到我iHaier"
- "发我iHaier"
- "发到iHaier"
- "发iHaier"
- "发个通知"
- 其他类似发送到 iHaier 群组消息的请求

## 前置准备

1. 获取飞书自定义机器人 Webhook 地址
2. 确认 iHaier 群组的 Webhook URL
3. 如需 @ 用户，获取对应的 open_id 或 user_id

## 消息发送

### 1. 发送文本消息

使用 `curl` 或 Python `requests` 库向 Webhook 发送 POST 请求：

```bash
curl -X POST "WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "消息内容"
    }
  }'
```

### 2. 发送富文本消息（支持 @ 用户）

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "通知标题",
        "content": [
          [
            {
              "tag": "text",
              "text": "你好 "
            },
            {
              "tag": "at",
              "user_id": "ou_xxxxxxxxxxxxxxxx",
              "user_name": "用户名"
            },
            {
              "tag": "text",
              "text": "，这是一条通知消息。"
            }
          ]
        ]
      }
    }
  }
}
```

### 3. @ 所有人

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "通知标题",
        "content": [
          [
            {
              "tag": "at",
              "user_id": "all"
            },
            {
              "tag": "text",
              "text": " 这是一条全员通知。"
            }
          ]
        ]
      }
    }
  }
}
```

## 实现步骤

1. **确认消息内容**：与用户确认要发送的消息文本、标题、需要 @ 的用户
2. **获取 Webhook URL**：如果用户未提供，询问飞书机器人的 Webhook 地址
3. **构建请求体**：根据消息类型（纯文本/富文本）构建 JSON 请求体
4. **发送请求**：使用 Python 或 curl 发送 POST 请求
5. **验证结果**：检查返回状态码，确认消息发送成功

## Python 示例

```python
import requests

webhook_url = "YOUR_WEBHOOK_URL"

# 富文本消息（带 @）
payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "系统通知",
                "content": [
                    [
                        {"tag": "text", "text": "任务已完成，请查看。"},
                    ]
                ]
            }
        }
    }
}

response = requests.post(webhook_url, json=payload)
print(response.json())
```

## 注意事项

- Webhook URL 是敏感信息，不要硬编码到文件中，应通过用户输入或环境变量获取
- @ 用户需要知道对应用户的 `user_id` 或 `open_id`
- 飞书消息长度有限制，长消息建议分段发送
- 发送频率不要太高，避免被限流
- 如果发送失败，重试 2-3 次并返回错误信息给用户
