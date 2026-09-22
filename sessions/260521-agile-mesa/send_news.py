import requests
import json

webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/608c82a6-6355-4bcb-b0b0-5c097602d2c9"

# 板块一：国内外要闻
section1_lines = [
    "**习近平同俄罗斯总统普京举行会谈**\n两国元首一致同意《中俄睦邻友好合作条约》继续延期，中俄联合声明发布。\n",
    "**中方对俄免签延长至2027年底**\n俄普通护照人员来华经商、旅游等不超过30天可免签入境。\n",
    "**塞尔维亚总统武契奇将访华**\n应习近平邀请，武契奇将于5月24日至28日对中国进行国事访问。\n",
    "**矿产资源法实施条例公布**\n李强签署国务院令，自2026年6月15日起施行，保障矿产资源安全。\n",
    "**前4月财政收入同比增长3.5%**\n全国一般公共预算收入8.34万亿元，证券交易印花税大增74.8%。\n",
    "**民营经济促进法施行一周年**\n发改委印发"法治护航民营经济"行动方案，深化优化发展环境专项行动。\n",
    "**美联储会议纪要放鹰**\n多数官员支持通胀持续高企时加息，多人倾向删除宽松倾向表述。\n",
    "**美伊冲突降温 原油大跌5.5%**\n特朗普称谈判处于"最终阶段"，伊朗称将在"强烈不信任"下继续推进。\n",
    "**神舟二十三号进行发射场区演练**\n载人飞行任务各系统全面开展发射场区联合演练。\n",
]

# 板块二：各平台热搜 Top 5
section2_lines = [
    "**微博热搜 Top 5** 🔥\n",
    "1. 普京访华 中俄元首会谈 `[时政]`\n",
    "2. 小米 YU7 GT 即将发布 雷军回应定价 `[科技/汽车]`\n",
    "3. 国乒莎头组合再次合体 WTT大满贯 `[体育]`\n",
    "4. 福建漳州"泡药杨梅"事件 5人被刑拘 `[社会]`\n",
    "5. 郑钦文法网赛程确定 中国金花2胜1负 `[体育]`\n",
    "\n**抖音热搜 Top 5** 🎵\n",
    "1. SpaceX 计划2028年部署轨道AI计算卫星 `[科技]`\n",
    "2. AI 短剧《天枢防线》致敬流浪地球 `[娱乐/科技]`\n",
    "3. 小米 YU7 GT 刷新纽北 SUV 圈速纪录 `[汽车]`\n",
    "4. 520 微信表白神器限时上线 `[社交]`\n",
    "5. 中国移动发布"超千兆宽带"可升级2000M `[科技]`\n",
    "\n**百度热搜 Top 5** 🔍\n",
    "1. 普京访华 中俄签署联合声明 `[时政]`\n",
    "2. 全国算力网加速建设 郑州超算集群投用 `[科技]`\n",
    "3. 民营经济促进法实施一周年 `[财经]`\n",
    "4. OpenAI 或本周五提交 IPO 申请 `[科技/财经]`\n",
    "5. 前4月快递业务量超645亿件 同比增5.1% `[社会]`\n",
    "\n**知乎热榜 Top 5** 💡\n",
    "1. 美联储放鹰：通胀高企时可能加息 `[财经]`\n",
    "2. 美伊冲突与谈判走向何方 `[国际]`\n",
    "3. OpenAI vs Anthropic：谁能先上市 `[科技]`\n",
    "4. 非遗武术大模型 2.0 发布 `[科技/文化]`\n",
    "5. 中俄教育年开幕 两国深化教育合作 `[教育/时政]`\n",
]

# 板块三：跨平台热点
section3_lines = [
    "**1. 普京访华 / 中俄关系** 🔥🔥🔥\n覆盖：微博、百度、抖音、知乎 | 元首会谈、联合声明、免签延长、教育年开幕等多项成果。\n",
    "**2. 小米 YU7 GT 发布** 🚗\n覆盖：微博、抖音 | 雷军回应定价"有点小贵"，刷新纽北SUV纪录，预计起售价40-50万元。\n",
    "**3. 美伊冲突与谈判** 🌍\n覆盖：百度、知乎、财经平台 | 特朗普称进入"最终阶段"，原油大跌5.5%，美联储放鹰。\n",
    "**4. OpenAI IPO 竞速** 💻\n覆盖：百度、知乎、微博 | 预测市场给出83%率先上市概率，AI军备竞赛进入资本市场阶段。\n",
    "**5. 国乒 / 体育赛事热点** 🏓\n覆盖：微博、百度 | 莎头组合合体出战WTT大满贯，郑钦文法网赛程确定，丁俊晖赵心童世锦赛德比。\n",
]

def build_section(title, lines):
    """构建一个板块的 card elements"""
    elements = []
    # 板块标题
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**{title}**"
        }
    })
    # 内容
    content = "".join(lines)
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": content
        }
    })
    return elements

# 构建完整卡片
elements = []

# 板块一
elements.extend(build_section("一、国内外要闻", section1_lines))
elements.append({"tag": "hr"})

# 板块二
elements.extend(build_section("二、各平台热搜 Top 5", section2_lines))
elements.append({"tag": "hr"})

# 板块三
elements.extend(build_section("三、跨平台热点", section3_lines))

card = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {
            "tag": "plain_text",
            "content": "📰 每日新闻播报 — 2026年5月21日"
        },
        "template": "blue"
    },
    "elements": elements,
    "note": {
        "tag": "plain_text",
        "content": "由 Incaier Agent 自动生成 | 数据来源：新闻联播、微博、抖音、百度、知乎"
    }
}

payload = {
    "msg_type": "interactive",
    "card": card
}

resp = requests.post(webhook_url, json=payload, timeout=15)
print(f"状态码: {resp.status_code}")
print(f"响应: {resp.text}")