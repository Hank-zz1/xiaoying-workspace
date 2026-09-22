import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# Build card elements as a list
elements = []

# --- Section 1: 国内外要闻 ---
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**\ud83d\udccc 一、国内外要闻**"}
})

news_items = [
    ("**1. 李强在辽宁大连调研，将出席夏季达沃斯论坛**\n"
     "国务院总理李强在大连调研产业升级与科技创新，并将出席第十七届夏季达沃斯论坛。"),
    ("**2. 丁薛祥出席第四届中国国际供应链促进博览会**\n"
     "丁薛祥出席开幕式并作主旨讲话，强调全球供应链合作与开放共赢。"),
    ("**3. 48名中国开发者联名举报苹果**\n"
     "要求苹果兑现全球最低费率承诺，引发业内对App Store抽成政策的广泛讨论。"),
    ("**4. 政府采购法迎来修订**\n"
     "强化权力监督与制度反腐，推动政府采购更加公开透明、公平竞争。"),
    ("**5. 穗莞深城际机前段全线电通**\n"
     "深圳机场至前海将实现10分钟内直达，大湾区轨道交通建设取得重大进展。"),
    ("**6. 浙江发布共同富裕规划**\n"
     "明确到2030年取得决定性进展，多雨带西移北扩，北方暴雨频次和强度均有增加。"),
    ("**7. 多地殡仪馆由私营向公立转型**\n"
     "推动殡葬服务回归公益属性，上海高考成绩今日公布，本科志愿填报7月1日启动。"),
    ("**8. 索尼集团时隔30年拟再发美元债**\n"
     "新财年巨亏3000多亿日元，公司寻求多元化融资渠道以应对经营压力。"),
]

fields = []
for item in news_items:
    fields.append({"is_short": False, "text": {"tag": "lark_md", "content": item}})

elements.append({"tag": "div", "fields": fields})
elements.append({"tag": "hr"})

# --- Section 2: 各平台热搜Top5 ---
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**\ud83d\udd25 二、各平台热搜 Top 5**"}
})

platforms = [
    ("\ud83d\udd35 百度热搜", [
        "1. 治国之要 首在用人 [时政]",
        "2. 姆巴佩世界波 [体育]",
        "3. 雷暴致本届世界杯首次休赛 [体育]",
        "4. 今天开始高考查分 [教育]",
        "5. 端午节假期666.7万人出游 [社会]",
    ]),
    ("\ud83d\udfe0 微博热搜", [
        "1. 今天开始高考查分 [教育]",
        "2. 首个高考成绩被屏蔽的人出现了 [社会]",
        "3. 字母哥被交易至热火 [体育]",
        "4. 女生高考查分701后质疑自己 [社会]",
        "5. 姆巴佩世界波 [体育]",
    ]),
    ("\u266b 抖音热搜", [
        "1. 今天开始高考查分 [教育]",
        "2. 哈兰德梅开二度 [体育]",
        "3. 字母哥被交易至热火 [体育]",
        "4. 高考查分仪式感 [社会]",
        "5. 雷暴致世界杯首次休赛 [体育]",
    ]),
    ("\ud83d\udca1 知乎热榜", [
        "1. 如何评价2026年高考分数线？[教育]",
        "2. 48名中国开发者举报苹果会产生什么影响？[科技]",
        "3. 浙江共同富裕规划能否实现2030年目标？[时政]",
        "4. 政府采购法修订对营商环境有何影响？[财经]",
        "5. 2026世界杯赛事讨论 [体育]",
    ]),
]

for i, (platform_name, items) in enumerate(platforms):
    content = "**" + platform_name + "**\n" + "\n".join(items)
    elements.append({
        "tag": "div",
        "text": {"tag": "lark_md", "content": content}
    })
    if i < len(platforms) - 1:
        elements.append({"tag": "hr"})

elements.append({"tag": "hr"})

# --- Section 3: 跨平台热点 ---
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md", "content": "**\ud83c\udf10 三、跨平台热点**"}
})

cross_platform = [
    ("**\ud83c\udfc6 高考查分季全面启动** [覆盖：微博/百度/抖音/知乎/B站]\n"
     "全国多地高考成绩陆续公布，查分仪式感、首个成绩被屏蔽、701分学霸等话题引爆全网，热度超270万。"),
    ("**\u26bd 2026世界杯热潮持续** [覆盖：百度/微博/抖音/B站]\n"
     "姆巴佩世界波、哈兰德梅开二度、雷暴致世界杯首次休赛，多场比赛话题霸榜各平台。"),
    ("**\ud83c\udfc0 字母哥被交易至热火** [覆盖：百度/B站]\n"
     "NBA重磅交易传闻引爆篮球圈，百度热度4.1万，B站热度166.6万，跨平台关注度极高。"),
]

cp_fields = []
for item in cross_platform:
    cp_fields.append({"is_short": False, "text": {"tag": "lark_md", "content": item}})

elements.append({"tag": "div", "fields": cp_fields})
elements.append({"tag": "hr"})

# Data note
elements.append({
    "tag": "div",
    "text": {"tag": "lark_md",
             "content": "**\ud83d\udcca 数据说明**：以上新闻和热搜数据综合自新闻联播、百度热搜、微博、抖音、知乎等平台，采集时间为2026年6月24日上午。"}
})

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "\ud83d\udcf0 每日新闻播报 - 2026年6月24日"},
        "template": "blue"
    },
    "elements": elements,
    "note": {"tag": "plain_text", "content": "由 Incaier Agent 自动生成"}
}

payload = {
    "msg_type": "interactive",
    "card": card
}

response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")