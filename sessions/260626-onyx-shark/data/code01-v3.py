# 代码01 v3.2 — MCP 网关回归 + 内置品牌回退 + SSE 解析
# 修复：v3.1 直接调 api.firecrawl.dev 在 HiAgent 沙箱失败
# 改回通过 MCP 网关调用，兼容 SSE 流响应格式

import json
import re
import ssl
import urllib.request
import urllib.error
from datetime import datetime

ACCESS_KEY = "pk_b1fb70c791093782097c3405bb9854cd18cccfe520714fa89932b20f8239f625"
FC_MCP = "https://market.haierfhtech.com/prod-api/capabilitymarket/mcp/http/cap_719957985ee345948726696a4cb59f7c"
BOCHA_MCP = "https://market.haierfhtech.com/prod-api/capabilitymarket/mcp/http/cap_66abf82820f1468dbf60175c3f529670"

def handler(params):
    input_data = params.get('input', '{}')

    if isinstance(input_data, str):
        try:
            plan = json.loads(input_data)
        except:
            return {"searchResult": json.dumps([{"error": "无法解析输入JSON"}], ensure_ascii=False)}
    else:
        plan = input_data

    # 兼容多种输入格式
    if isinstance(plan, dict) and 'name' in plan and 'tasks' in plan and 'brands' not in plan:
        plan = {"region": "未知区域", "brands": [plan]}
    if isinstance(plan, dict) and 'raw_output' in plan:
        try:
            inner = json.loads(plan['raw_output'])
            if isinstance(inner, dict):
                if 'name' in inner and 'tasks' in inner:
                    plan = {"region": inner.get('region', '未知区域'), "brands": [inner]}
                elif 'brands' in inner:
                    plan = inner
        except:
            pass

    region = plan.get('region', '未知区域')
    brands = plan.get('brands', [])

    if not brands:
        brands = fallback_brands(region)

    if not brands:
        return {"searchResult": json.dumps([{"error": f"未找到 {region} 的品牌数据"}], ensure_ascii=False)}

    all_results = []
    for brand_info in brands:
        brand_name = brand_info.get('name', '未知品牌')
        tasks = brand_info.get('tasks', [])
        brand_result = {"brand": brand_name, "region": region, "scrape": None, "ecommerce": None, "news": None}

        for task in tasks:
            ttype = task.get('type', '')
            if ttype == 'scrape':
                brand_result['scrape'] = do_scrape(task.get('url', ''), task.get('search_cn', ''), brand_name)
            elif ttype in ('ecommerce', 'ecom'):
                brand_result['ecommerce'] = do_ecommerce(task.get('url', ''), task.get('search_cn', ''), brand_name)
            elif ttype == 'news':
                brand_result['news'] = do_news(task.get('search_cn', ''), task.get('search_en', ''), brand_name)

        all_results.append(brand_result)

    return {"searchResult": json.dumps(all_results, ensure_ascii=False)}


# ─── MCP 网关调用（兼容 SSE 响应）─────────────────────────────

def _ctx():
    c = ssl.create_default_context()
    c.check_hostname = False
    c.verify_mode = ssl.CERT_NONE
    return c

def mcp_call(mcp_url, tool, args, timeout=60):
    """通过 MCP 网关调用工具，兼容 SSE 格式响应"""
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": args}
    }).encode('utf-8')

    req = urllib.request.Request(mcp_url, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-Platform-Access-Key', ACCESS_KEY)

    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=timeout) as resp:
            raw = resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {str(e)[:200]}"}
    except Exception as e:
        return {"error": str(e)[:200]}

    # 解析 SSE 格式: event:message\ndata:{json}\n\n
    if 'event:' in raw or 'data:' in raw:
        for line in raw.split('\n'):
            if line.startswith('data:'):
                data_str = line[5:].strip()
                if data_str:
                    try:
                        return json.loads(data_str)
                    except:
                        continue

    # 回退：直接 JSON 解析
    try:
        return json.loads(raw)
    except:
        return {"error": "无法解析响应", "raw": raw[:500]}


def fc_scrape(url):
    """通过 MCP 网关抓取网页"""
    resp = mcp_call(FC_MCP, "firecrawl_scrape", {"url": url, "formats": ["markdown"], "waitFor": 3000})
    # 兼容多种响应格式
    if isinstance(resp, dict):
        # 格式1: {"data": {"markdown": "..."}}
        data = resp.get('data', {})
        if isinstance(data, dict) and data.get('markdown'):
            return data['markdown']
        # 格式2: {"markdown": "..."}
        if resp.get('markdown'):
            return resp['markdown']
        # 格式3: {"content": [{"text": "..."}]}  (JSON-RPC result)
        content = resp.get('content', [])
        if content and isinstance(content, list):
            try:
                inner = json.loads(content[0].get('text', '{}'))
                if isinstance(inner, dict):
                    d = inner.get('data', inner)
                    return d.get('markdown', '') or ''
            except:
                pass
        # 格式4: {"result": {"content": [...]}}
        result = resp.get('result', {})
        if isinstance(result, dict):
            rcontent = result.get('content', [])
            if rcontent and isinstance(rcontent, list):
                try:
                    inner = json.loads(rcontent[0].get('text', '{}'))
                    if isinstance(inner, dict):
                        d = inner.get('data', inner)
                        return d.get('markdown', '') or ''
                except:
                    pass
    return ""


def fc_search(query, limit=5):
    """通过 MCP 网关搜索"""
    resp = mcp_call(FC_MCP, "firecrawl_search", {"query": query, "limit": limit, "lang": "zh"})
    articles = []

    def extract_pages(obj):
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            # 格式1: {"data": [...]}
            if 'data' in obj and isinstance(obj['data'], list):
                return obj['data']
            # 格式2: {"content": [{"text": "..."}]}
            content = obj.get('content', [])
            if content and isinstance(content, list):
                try:
                    inner = json.loads(content[0].get('text', '{}'))
                    return extract_pages(inner)
                except:
                    pass
            # 格式3: {"result": {"content": [...]}}
            result = obj.get('result', {})
            if isinstance(result, dict):
                return extract_pages(result)
        return []

    pages = extract_pages(resp)
    for p in pages[:limit]:
        if isinstance(p, dict):
            articles.append({
                "title": (p.get('title', '') or '').replace('\\', ''),
                "snippet": (p.get('description', '') or '')[:200],
                "url": p.get('url', ''),
                "source": p.get('source', '')
            })
    return articles


# ─── 内置品牌注册表 ──────────────────────────────────────────

def fallback_brands(region):
    """大模型01 未生成 brands 时的内置回退"""
    registry = {
        "美洲": [
            {"name": "Samsung", "tasks": [
                {"type": "scrape", "url": "https://www.samsung.com/us/refrigerators/all-refrigerators/", "search_cn": "三星美国 冰箱 2026 新品"},
                {"type": "ecommerce", "url": "https://www.amazon.com/s?k=Samsung+refrigerator+2026", "search_cn": "三星冰箱 Amazon 美国"},
                {"type": "news", "search_cn": "三星冰箱 美洲 2026 新品", "search_en": "Samsung refrigerator US 2026 new model"}
            ]},
            {"name": "LG", "tasks": [
                {"type": "scrape", "url": "https://www.lg.com/us/refrigerators", "search_cn": "LG美国 冰箱 2026 新品"},
                {"type": "ecommerce", "url": "https://www.amazon.com/s?k=LG+refrigerator+2026", "search_cn": "LG冰箱 Amazon 美国"},
                {"type": "news", "search_cn": "LG冰箱 美洲 2026 新品", "search_en": "LG refrigerator US 2026 new model"}
            ]},
            {"name": "Whirlpool", "tasks": [
                {"type": "scrape", "url": "https://www.whirlpool.com/kitchen/refrigerators.html", "search_cn": "惠而浦美国 冰箱 2026"},
                {"type": "ecommerce", "url": "https://www.amazon.com/s?k=Whirlpool+refrigerator+2026", "search_cn": "惠而浦冰箱 Amazon"},
                {"type": "news", "search_cn": "惠而浦冰箱 美洲 2026", "search_en": "Whirlpool refrigerator US 2026"}
            ]},
            {"name": "GE Appliances", "tasks": [
                {"type": "scrape", "url": "https://www.geappliances.com/ge/refrigerators.htm", "search_cn": "GE冰箱美国 2026"},
                {"type": "news", "search_cn": "GE冰箱 美洲 2026", "search_en": "GE refrigerator US 2026"}
            ]},
            {"name": "Hisense", "tasks": [
                {"type": "news", "search_cn": "海信冰箱 美洲 2026", "search_en": "Hisense refrigerator US 2026"}
            ]},
        ],
        "欧洲": [
            {"name": "Samsung", "tasks": [
                {"type": "scrape", "url": "https://www.samsung.com/uk/refrigerators/all-refrigerators/", "search_cn": "三星欧洲 冰箱 2026"},
                {"type": "news", "search_cn": "三星冰箱 欧洲 2026", "search_en": "Samsung refrigerator Europe 2026"}
            ]},
            {"name": "LG", "tasks": [
                {"type": "scrape", "url": "https://www.lg.com/uk/refrigerators", "search_cn": "LG欧洲 冰箱 2026"},
                {"type": "news", "search_cn": "LG冰箱 欧洲 2026", "search_en": "LG refrigerator Europe 2026"}
            ]},
            {"name": "Bosch", "tasks": [
                {"type": "scrape", "url": "https://www.bosch-home.co.uk/products/fridge-freezers", "search_cn": "博世欧洲 冰箱 2026"},
                {"type": "news", "search_cn": "博世冰箱 欧洲 2026", "search_en": "Bosch refrigerator Europe 2026"}
            ]},
            {"name": "Miele", "tasks": [
                {"type": "scrape", "url": "https://www.miele.co.uk/c/refrigeration-1060.htm", "search_cn": "Miele冰箱 欧洲 2026"},
                {"type": "news", "search_cn": "Miele冰箱 欧洲 2026", "search_en": "Miele refrigerator Europe 2026"}
            ]},
            {"name": "Siemens", "tasks": [
                {"type": "scrape", "url": "https://www.siemens-home.bsh-group.com/uk/en/products/cooling", "search_cn": "西门子冰箱 欧洲 2026"},
                {"type": "news", "search_cn": "西门子冰箱 欧洲 2026", "search_en": "Siemens refrigerator Europe 2026"}
            ]},
            {"name": "Haier", "tasks": [
                {"type": "news", "search_cn": "海尔冰箱 欧洲 2026", "search_en": "Haier refrigerator Europe 2026"}
            ]},
        ],
        "澳洲": [
            {"name": "Samsung", "tasks": [
                {"type": "scrape", "url": "https://www.samsung.com/au/refrigerators/all-refrigerators/", "search_cn": "三星澳洲 冰箱 2026"},
                {"type": "news", "search_cn": "三星冰箱 澳洲 2026", "search_en": "Samsung refrigerator Australia 2026"}
            ]},
            {"name": "LG", "tasks": [
                {"type": "scrape", "url": "https://www.lg.com/au/refrigerators", "search_cn": "LG澳洲 冰箱 2026"},
                {"type": "news", "search_cn": "LG冰箱 澳洲 2026", "search_en": "LG refrigerator Australia 2026"}
            ]},
            {"name": "Hisense", "tasks": [
                {"type": "scrape", "url": "https://www.hisense.com.au/refrigerators/", "search_cn": "海信澳洲 冰箱 2026"},
                {"type": "news", "search_cn": "海信冰箱 澳洲 2026", "search_en": "Hisense refrigerator Australia 2026"}
            ]},
            {"name": "Westinghouse", "tasks": [
                {"type": "scrape", "url": "https://www.westinghouse.com.au/refrigeration", "search_cn": "西屋澳洲 冰箱 2026"},
                {"type": "news", "search_cn": "西屋冰箱 澳洲 2026", "search_en": "Westinghouse refrigerator Australia 2026"}
            ]},
            {"name": "Fisher & Paykel", "tasks": [
                {"type": "scrape", "url": "https://www.fisherpaykel.com/au/refrigeration.html", "search_cn": "斐雪派克 冰箱 2026"},
                {"type": "news", "search_cn": "Fisher&Paykel冰箱 澳洲 2026", "search_en": "Fisher & Paykel refrigerator Australia 2026"}
            ]},
        ],
        "亚洲": [
            {"name": "Samsung", "tasks": [
                {"type": "scrape", "url": "https://www.samsung.com/sg/refrigerators/all-refrigerators/", "search_cn": "三星亚洲 冰箱 2026"},
                {"type": "news", "search_cn": "三星冰箱 亚洲 2026", "search_en": "Samsung refrigerator Asia 2026"}
            ]},
            {"name": "LG", "tasks": [
                {"type": "scrape", "url": "https://www.lg.com/sg/refrigerators", "search_cn": "LG亚洲 冰箱 2026"},
                {"type": "news", "search_cn": "LG冰箱 亚洲 2026", "search_en": "LG refrigerator Asia 2026"}
            ]},
            {"name": "Panasonic", "tasks": [
                {"type": "scrape", "url": "https://www.panasonic.com/sg/consumer/kitchen-appliance/refrigerator.html", "search_cn": "松下冰箱 亚洲 2026"},
                {"type": "news", "search_cn": "松下冰箱 亚洲 2026", "search_en": "Panasonic refrigerator Asia 2026"}
            ]},
            {"name": "Hitachi", "tasks": [
                {"type": "scrape", "url": "https://www.hitachi-homeappliances.com/sg/products/refrigerator/", "search_cn": "日立冰箱 亚洲 2026"},
                {"type": "news", "search_cn": "日立冰箱 亚洲 2026", "search_en": "Hitachi refrigerator Asia 2026"}
            ]},
            {"name": "Haier", "tasks": [
                {"type": "news", "search_cn": "海尔冰箱 亚洲 2026", "search_en": "Haier refrigerator Asia 2026"}
            ]},
        ],
    }
    return registry.get(region, [])


# ─── 任务处理 ────────────────────────────────────────────────

def do_scrape(url, fallback_search_cn, brand_name):
    """官网产品抓取"""
    result = {"status": "failed", "url": url, "models": [], "error": ""}

    if not url:
        if fallback_search_cn:
            articles = fc_search(fallback_search_cn, 5)
            return {"status": "fallback", "articles": articles}
        result["error"] = "无可用官网URL"
        return result

    try:
        md = fc_scrape(url)
        if not md:
            result["error"] = "官网抓取失败：无内容返回"
            if fallback_search_cn:
                articles = fc_search(fallback_search_cn, 5)
                return {"status": "fallback", "articles": articles}
            return result

        models = extract_from_md(md)
        if models:
            result["status"] = "success"
            result["models"] = models
            result["model_count"] = len(models)
        else:
            result["status"] = "partial"
            result["error"] = "页面抓取成功但未提取到产品"
            result["markdown_preview"] = md[:800]

        return result

    except Exception as e:
        result["error"] = str(e)[:200]
        if fallback_search_cn:
            articles = fc_search(fallback_search_cn, 5)
            return {"status": "fallback", "articles": articles}
        return result


def do_ecommerce(url, fallback_search_cn, brand_name):
    """电商页面抓取"""
    result = {"status": "failed", "url": url, "products": [], "error": ""}
    if not url:
        if fallback_search_cn:
            articles = fc_search(fallback_search_cn, 5)
            return {"status": "fallback", "articles": articles}
        result["error"] = "无可用电商URL"
        return result

    try:
        md = fc_scrape(url)
        if md:
            prods = extract_amazon(md)
            if prods:
                result["status"] = "success"
                result["products"] = prods
                result["product_count"] = len(prods)
            else:
                result["status"] = "partial"
                result["error"] = "未提取到产品"
                result["markdown_preview"] = md[:500]
        else:
            result["error"] = "电商页面抓取失败"
            if fallback_search_cn:
                articles = fc_search(fallback_search_cn, 5)
                return {"status": "fallback", "articles": articles}
        return result
    except Exception as e:
        result["error"] = str(e)[:200]
        if fallback_search_cn:
            articles = fc_search(fallback_search_cn, 5)
            return {"status": "fallback", "articles": articles}
        return result


def do_news(search_cn, search_en, brand_name):
    """新闻搜索 + 日期过滤"""
    result = {"status": "failed", "articles": [], "error": ""}
    queries = [q for q in [search_cn, search_en] if q]

    for query in queries:
        articles = fc_search(query, 5)
        if articles:
            filtered = filter_fresh(articles)
            if filtered:
                result["status"] = "success"
                result["articles"] = filtered
                return result
        result["error"] = "无相关新闻"

    return result


# ─── 提取与过滤 ──────────────────────────────────────────────

def extract_from_md(md):
    """从 markdown 提取产品名和型号"""
    seen = set()
    items = []

    # 1) 解析 markdown 链接 [name](url)
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', md):
        name = m.group(1).strip()
        url = m.group(2).strip()

        # 过滤图片/UI元素
        if re.search(r'\.(svg|png|jpg|gif|webp|ico)(\?|$)', name, re.IGNORECASE):
            continue
        if re.search(r'\$ORIGIN_IMG\$', name):
            continue

        # 过滤导航/非产品链接
        skip = ['home', 'support', 'cart', 'account', 'login', 'sign', 'menu',
                'search', 'facebook', 'twitter', 'youtube', 'instagram', 'footer',
                'privacy', 'terms', 'cookie', 'accessibility', 'sitemap', 'wishlist',
                'compare', 'store', 'find', 'chat', 'warranty', 'delivery', 'help']
        if any(w in url.lower() or w in name.lower() for w in skip):
            continue

        if 8 <= len(name) <= 200:
            if name not in seen:
                seen.add(name)
                items.append({"name": name, "url": url})

    # 2) 正则匹配纯型号
    model_rx = [
        r'\b([A-Z]{2,6}[\-]?\d{2,6}[A-Z]{0,4}[A-Z0-9]{0,4})\b',
        r'\b([A-Z]{2,4}\d{2,4}[A-Z]{2,4})\b',
        r'Model\s*(?:NO\.|No|Number)?\s*[：:]*\s*([A-Z0-9\-]{6,15})',
    ]
    for rx in model_rx:
        for m in re.finditer(rx, md, re.IGNORECASE):
            model = m.group(1).strip()
            if 5 <= len(model) <= 20 and not model.isdigit():
                if not re.match(r'^(HTTP|HTTPS|WWW|CSS|HTML|JS|API)', model, re.IGNORECASE):
                    if model not in seen:
                        seen.add(model)
                        items.append({"name": model, "model": model})

    return items[:30]


def extract_amazon(md):
    """Amazon 页面产品提取"""
    products = []
    price_rx = r'(?:€|EUR|USD|\$)\s*[\d.,]+'
    lines = md.split('\n')
    cur = {}

    for line in lines:
        line = line.strip()
        if not line:
            if cur.get('name'):
                products.append(cur)
                cur = {}
            continue
        if re.match(r'^(Sponsored|Gesponsert|Results|Ergebnisse|Filter|Sort|Page|Seite)', line, re.IGNORECASE):
            continue
        if len(line) > 30 and not line.startswith(('http', '//', '(', '[')):
            if not cur.get('name'):
                cur['name'] = line[:150]
        pm = re.search(price_rx, line)
        if pm and not cur.get('price'):
            cur['price'] = pm.group(0)
        rm = re.search(r'(\d+[.,]?\d*)\s*(?:out of|von|de)\s*5\s*(?:stars|Sternen)', line)
        if rm and not cur.get('rating'):
            cur['rating'] = rm.group(1)

    if cur.get('name'):
        products.append(cur)
    return products[:10]


def filter_fresh(articles):
    """过滤 2024 年之前的新闻"""
    this_year = datetime.now().year
    out = []
    for a in articles:
        text = a.get('title', '') + ' ' + a.get('snippet', '')
        years = re.findall(r'(20\d{2})', text)
        if years:
            if max(int(y) for y in years) >= this_year - 1:
                out.append(a)
        else:
            out.append(a)
    return out