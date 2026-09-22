import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 10条精选新闻
news_items = [
    {
        "title": "A股三大指数集体收跌，成交缩量至2.89万亿",
        "summary": "5月18日沪指跌0.09%，深成指跌0.20%，创业板指跌0.36%，结束连续8日成交破3万亿态势。油气、存储芯片、CPO板块领涨，贵金属、汽车整车领跌。",
        "source": "格隆汇/东方财富 | 2026-05-18"
    },
    {
        "title": "李强总理调研：推动AI与先进制造业深度融合",
        "summary": "李强5月18日在北京调研，强调促进智能机器人迭代升级，推进AI全方位赋能制造业，加快培育经济发展新动能新优势。",
        "source": "腾讯网/新浪财经 | 2026-05-19"
    },
    {
        "title": "丁薛祥调研算力网建设，强调算力是综合国力体现",
        "summary": "丁薛祥在北京、河北、内蒙古调研，要求推进全国一体化算力网建设和集约高效利用，统筹布局有序建设。",
        "source": "新浪财经 | 2026-05-19"
    },
    {
        "title": "商务部将出台\"人工智能+消费\"政策体系",
        "summary": "商务部副部长盛秋平宣布抓紧筹划出台AI+消费政策，利好消费电子、AI应用、数字服务等赛道。",
        "source": "东方财富网 | 2026-05-19"
    },
    {
        "title": "衍生品新规正式落地，11月16日起施行",
        "summary": "新规进一步规范衍生品市场交易、风控及监管体系，完善资本市场风险管理机制，促进市场健康发展。",
        "source": "四大证券报/东方财富 | 2026-05-19"
    },
    {
        "title": "华润新能源245亿IPO获批，将创深交所历史纪录",
        "summary": "证监会同意华润新能源IPO注册，募资245亿元，为红筹企业回归A股提供重要范本，预计最快7月挂牌。",
        "source": "今日头条 | 2026-05-19"
    },
    {
        "title": "美股涨跌不一，科技股承压，降息预期渺茫",
        "summary": "纳指跌0.51%，标普跌0.07%。美债收益率飙升冲击科技股，能源价格上涨放大通胀担忧，美联储短期内降息可能性渺茫。",
        "source": "新浪财经 | 2026-05-19"
    },
    {
        "title": "全球债市抛售潮冲击股市，重新定价风险升温",
        "summary": "美英日等国国债收益率飙升，G7财长将债市暴跌列入议程，投资者担忧通胀卷土重来、美联储或转向加息。",
        "source": "今日头条 | 2026-05-19"
    },
    {
        "title": "美伊局势紧张，特朗普推迟军事打击计划",
        "summary": "白宫认为伊朗核协议提案无实质改进，特朗普原考虑军事行动，后在多国领导人要求下推迟打击计划。",
        "source": "新浪财经 | 2026-05-19"
    },
    {
        "title": "中美元首会晤达成经贸成果，互减商品关税",
        "summary": "中美达成\"建设性战略稳定关系\"共识，考虑互减300亿美元非关键领域商品关税，成立贸易和投资理事会。",
        "source": "新浪财经/搜狐 | 2026-05-17"
    }
]

# 构建卡片元素
elements = []
for i, news in enumerate(news_items):
    # 每条新闻的div块
    content = f"**{news['title']}**\n{news['summary']}\n_{news['source']}_"
    elements.append({
        "tag": "div",
        "fields": [
            {
                "is_short": False,
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            }
        ]
    })
    # 最后一条不加分割线
    if i < len(news_items) - 1:
        elements.append({"tag": "hr"})

# 构建完整卡片
card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "📈 每日股市简报 - 2026年5月19日"
        },
        "template": "red"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成"
    }
}

# 发送请求
payload = {
    "msg_type": "interactive",
    "card": card
}

response = requests.post(webhook_url, json=payload, timeout=10)
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")