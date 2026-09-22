# 代码01 v2.0 — 多源竞品搜索执行器
# HiAgent Python 代码节点
# 输入: 大模型01 输出的 JSON（含 brands[].tasks[]）
# 输出: searchResult JSON 数组

import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl

def handler(params):
    input_data = params.get('input', '{}')

    # 解析输入 - 兼容多种格式
    if isinstance(input_data, str):
        try:
            plan = json.loads(input_data)
        except:
            return {"searchResult": json.dumps([{"error": "无法解析输入JSON"}], ensure_ascii=False)}
    else:
        plan = input_data

    # 兼容格式1: 单个品牌对象 {name, tasks} → 自动包裹
    if isinstance(plan, dict) and 'name' in plan and 'tasks' in plan and 'brands' not in plan:
        plan = {"region": "未知区域", "brands": [plan]}

    # 兼容格式2: raw_output 中可能包含完整 JSON
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
        return {"searchResult": json.dumps([{"error": f"未找到 {region} 的品牌数据"}], ensure_ascii=False)}

    all_results = []

    for brand_info in brands:
        brand_name = brand_info.get('name', '未知品牌')
        tasks = brand_info.get('tasks', [])

        brand_result = {
            "brand": brand_name,
            "region": region,
            "scrape": None,
            "ecommerce": None,
            "news": None
        }

        for task in tasks:
            task_type = task.get('type', '')

            # 兼容 "ecom" 和 "ecommerce" 两种写法
            if task_type == 'scrape':
                url = task.get('url', '')
                search_cn = task.get('search_cn', '')
                brand_result['scrape'] = do_scrape(url, search_cn, brand_name)

            elif task_type in ('ecommerce', 'ecom'):
                url = task.get('url', '')
                search_cn = task.get('search_cn', '')
                brand_result['ecommerce'] = do_ecommerce(url, search_cn, brand_name)

            elif task_type == 'news':
                search_cn = task.get('search_cn', '')
                search_en = task.get('search_en', '')
                brand_result['news'] = do_news(search_cn, search_en, brand_name)

        all_results.append(brand_result)

    return {"searchResult": json.dumps(all_results, ensure_ascii=False)}


def do_scrape(url, fallback_search_cn, brand_name):
    """官网抓取 - 失败时回退到 Firecrawl 搜索"""
    result = {"status": "failed", "url": url, "models": [], "error": ""}

    if not url:
        # 无可用URL，直接回退搜索
        if fallback_search_cn:
            return firecrawl_news_search(fallback_search_cn, "scrape_fallback")
        result["error"] = "无可用官网URL"
        return result

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        markdown = firecrawl_fetch(url, ctx)
        if not markdown:
            result["error"] = "官网抓取失败：无内容返回"
            if fallback_search_cn:
                return firecrawl_news_search(fallback_search_cn, "scrape_fallback")
            return result

        # 提取型号
        models = extract_models(markdown)
        if models:
            result["status"] = "success"
            result["models"] = models
            result["model_count"] = len(models)
            # 提取页面基本信息
            result["page_info"] = extract_page_info(markdown)
        else:
            result["status"] = "partial"
            result["error"] = "页面抓取成功但未提取到型号"
            result["markdown_preview"] = markdown[:800]

        return result

    except Exception as e:
        result["error"] = str(e)[:200]
        if fallback_search_cn:
            return firecrawl_news_search(fallback_search_cn, "scrape_fallback")
        return result


def do_ecommerce(url, fallback_search_cn, brand_name):
    """电商搜索 - Amazon 站点抓取"""
    result = {"status": "failed", "url": url, "products": [], "error": ""}

    if not url:
        result["error"] = "无可用电商URL"
        return result

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        markdown = firecrawl_fetch(url, ctx)
        if not markdown:
            result["error"] = "电商页面抓取失败"
            return result

        # 提取产品信息
        products = extract_amazon_products(markdown)
        if products:
            result["status"] = "success"
            result["products"] = products
            result["product_count"] = len(products)
        else:
            result["status"] = "partial"
            result["error"] = "未提取到产品信息"
            result["markdown_preview"] = markdown[:500]

        return result

    except Exception as e:
        result["error"] = str(e)[:200]
        return result


def do_news(search_cn, search_en, brand_name):
    """新闻搜索 - Firecrawl 搜索"""
    result = {"status": "failed", "articles": [], "error": ""}

    # 优先用中文关键词搜索
    queries = [q for q in [search_cn, search_en] if q]
    for query in queries:
        search_result = firecrawl_news_search(query, "news")
        if search_result.get("articles"):
            result["status"] = "success"
            result["articles"] = search_result["articles"]
            break
        result["error"] = search_result.get("error", "")

    return result


def firecrawl_fetch(url, ctx):
    """通过 Firecrawl HTTP API 抓取网页"""
    try:
        api_url = "https://api.firecrawl.dev/v1/scrape"
        data = json.dumps({
            "url": url,
            "formats": ["markdown"],
            "waitFor": 3000
        }).encode('utf-8')

        req = urllib.request.Request(api_url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer fc-VZ9DGaMhg9wkq74YyiDoRh8FS5HZUgjnmtE0ltwlEh9l7KDW33TW1XsKqc98')

        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            return body.get('data', {}).get('markdown', '')

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')[:300]
        return ""
    except Exception as e:
        return ""


def firecrawl_news_search(query, source_type):
    """Firecrawl 网页搜索"""
    result = {"articles": [], "raw": None}
    try:
        api_url = "https://api.firecrawl.dev/v1/search"
        data = json.dumps({
            "query": query,
            "limit": 5,
            "lang": "zh",
            "scrapeOptions": {"formats": ["markdown"]}
        }).encode('utf-8')

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(api_url, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Bearer fc-VZ9DGaMhg9wkq74YyiDoRh8FS5HZUgjnmtE0ltwlEh9l7KDW33TW1XsKqc98')

        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            result["raw"] = body

            pages = body.get('data', [])
            for p in pages[:5]:
                result["articles"].append({
                    "title": (p.get('title', '') or '').replace('\\', ''),
                    "snippet": (p.get('description', '') or '')[:200],
                    "url": p.get('url', ''),
                    "source": p.get('source', '')
                })

        return result

    except Exception as e:
        result["error"] = str(e)[:200]
        return result


def extract_models(markdown):
    """从 markdown 中提取产品型号"""
    models = set()
    # 常见冰箱型号格式: 字母+数字组合，6-15字符
    patterns = [
        r'\b([A-Z]{2,6}[\-]?\d{2,6}[A-Z]{0,4}[A-Z0-9]{0,4})\b',
        r'\b([A-Z]{2,4}\d{2,4}[A-Z]{2,4})\b',
        r'Model\s*(?:NO\.|No|Number)?\s*[：:]*\s*([A-Z0-9\-]{6,15})',
        r'(?:型号|モデル|모델)[：:\s]*([A-Z0-9\-]{6,15})',
    ]
    for pattern in patterns:
        for m in re.finditer(pattern, markdown, re.IGNORECASE):
            model = m.group(1).strip()
            if 5 <= len(model) <= 20 and not model.isdigit():
                # 过滤掉明显不是型号的
                if not re.match(r'^(HTTP|HTTPS|WWW|CSS|HTML|JS|API)', model, re.IGNORECASE):
                    models.add(model)

    return list(models)[:30]


def extract_amazon_products(markdown):
    """从 Amazon 页面提取产品信息"""
    products = []
    # 提取价格模式
    price_pattern = r'(?:€|EUR|USD|\$)\s*[\d.,]+'
    # 提取评分模式
    rating_pattern = r'(\d+[.,]?\d*)\s*(?:out of|von|de)\s*5\s*(?:stars|Sternen|estrellas)'

    # 按行扫描，匹配产品标题+价格
    lines = markdown.split('\n')
    current_product = {}

    for line in lines:
        line = line.strip()
        if not line:
            if current_product.get('name'):
                products.append(current_product)
                current_product = {}
            continue

        # 跳过明显不是产品的行
        if re.match(r'^(Sponsored|Gesponsert|Results|Ergebnisse|Filter|Sort|Page|Seite)', line, re.IGNORECASE):
            continue

        # 检测产品名（较长的行，不含特殊符号）
        if len(line) > 30 and not line.startswith(('http', '//', '(', '[')):
            if not current_product.get('name'):
                current_product['name'] = line[:150]

        # 检测价格
        price_match = re.search(price_pattern, line)
        if price_match and not current_product.get('price'):
            current_product['price'] = price_match.group(0)

        # 检测评分
        rating_match = re.search(rating_pattern, line)
        if rating_match and not current_product.get('rating'):
            current_product['rating'] = rating_match.group(1)

    if current_product.get('name'):
        products.append(current_product)

    return products[:10]


def extract_page_info(markdown):
    """提取页面概要信息"""
    info = {}
    # 计算总产品数
    total_match = re.search(r'(?:(\d+)\s*(?:products|Produkte|results|Ergebnisse|items|models))', markdown, re.IGNORECASE)
    if total_match:
        info['total_shown'] = total_match.group(1)

    # 检查是否有 2026 相关
    if '2026' in markdown:
        info['has_2026'] = True

    return info