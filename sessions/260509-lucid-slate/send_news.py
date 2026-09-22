import requests
import json

# 飞书 Webhook URL
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 新闻内容
news_content = """📰 2026 年 5 月 8 日新闻播报

【国内要闻】
1. 塔吉克斯坦总统将访华 - 应习近平邀请，拉赫蒙总统将于 5 月 11-14 日进行国事访问
2. 粤港澳大湾区建设 - "十五五"开局之年，加快打造高质量发展动力源
3. 行政复议法实施条例修订 - 李强签署国务院令，7 月 1 日起施行
4. 天舟十号准备发射 - 船箭组合体转运至发射区，近日择机发射
5. 营商环境改善 - 五项"一件事"政务服务改革完成，涉企检查"扫码入企"全面推行
6. 儿童用药保障 - 八部门出台 16 条措施破解"用药靠猜、剂量靠掰"

【国际要闻】
1. 美伊霍尔木兹海峡交火 - 美军驱逐舰遭伊朗导弹袭击后反击，伊媒称局势已恢复正常
2. 俄乌局势 - 俄国防部宣布实施胜利日停火
3. 美国关税政策违法 - 美法院裁定政府 10% 全球关税政策违法
4. 日本扩军修宪抗议 - 民众集会抗议高市政权危险动向
5. 中东粮食危机 - 粮农组织警告紧张局势冲击粮食供应
6. 日本核电故障 - 一核电机组因蒸汽泄漏暂停运转

—— 小盈晨报
"""

# 构建富文本消息
payload = {
    "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "📰 昨日新闻播报",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": news_content
                        }
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
print(f"返回结果：{json.dumps(result, ensure_ascii=False)}")

if result.get("code") == 0:
    print("[SUCCESS] 消息发送成功！")
else:
    print(f"[ERROR] 消息发送失败：{result.get('msg', '未知错误')}")
