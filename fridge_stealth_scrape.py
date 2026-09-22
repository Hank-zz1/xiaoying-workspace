# -*- coding: utf-8 -*-
"""澳新冰箱新品监控 · 通用隐身抓取脚本（固定模式版）
用法:
  python fridge_stealth_scrape.py <url> [选项]
选项:
  --headed        有头模式（LG 等 Akamai 强反爬站点必须加）
  --wait=N        页面加载后额外等待秒数（默认 10）
  --scroll=N      向下滚动次数，触发懒加载（默认 3）
  --mode=jsonld   提取 JSON-LD 产品数据（三星站产品在 JSON-LD 里）
  --mode=hrefs    提取产品链接
  --href-kw=kw    链接过滤关键词（可多个；默认 product/fridge/refriger）
  --model-re=RE   型号正则（可多个），从全文提取型号列表
  --shot          保存截图（默认关：某些站等待字体加载会卡死截图）
  --savehtml      保存 HTML 到 fridge_scrape.html
输出: 单行 JSON（截断至 200KB）
"""
import json, re, sys, time, random

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def parse(argv):
    url = None
    o = dict(headed=False, wait=10, scroll=3, mode="all", href_kws=[],
             model_res=[], shot=False, savehtml=False, retries=3, nav_timeout=90)
    for a in argv:
        if a == "--headed":
            o["headed"] = True
        elif a == "--shot":
            o["shot"] = True
        elif a == "--savehtml":
            o["savehtml"] = True
        elif a.startswith("--wait="):
            o["wait"] = int(a.split("=", 1)[1])
        elif a == "--retries-off":
            o["retries"] = 1
        elif a.startswith("--retries="):
            o["retries"] = int(a.split("=", 1)[1])
        elif a.startswith("--nav="):
            o["nav_timeout"] = int(a.split("=", 1)[1])
        elif a.startswith("--scroll="):
            o["scroll"] = int(a.split("=", 1)[1])
        elif a.startswith("--mode="):
            o["mode"] = a.split("=", 1)[1]
        elif a.startswith("--href-kw="):
            o["href_kws"].append(a.split("=", 1)[1].lower())
        elif a.startswith("--model-re="):
            o["model_res"].append(a.split("=", 1)[1])
        elif not a.startswith("-") and url is None:
            url = a
    return url, o


def _walk(node):
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def extract_jsonld(html):
    items, seen = [], set()
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        for node in _walk(data):
            t = node.get("@type")
            t = " ".join(t) if isinstance(t, list) else (t or "")
            name = node.get("name")
            url = node.get("url")
            if not (isinstance(name, str) and name.strip()) or "Product" not in t:
                continue
            key = (name[:50], (url or "")[:100])
            if key in seen:
                continue
            seen.add(key)
            items.append({"name": name[:120], "url": (url or "")[:200]})
    return items


def extract_hrefs(html, kws):
    out, seen = [], set()
    for h in re.findall(r'href="([^"]+)"', html):
        h = h.split("?")[0]
        if not h.startswith(("/", "http")):
            continue
        if any(k in h.lower() for k in kws):
            if h in seen:
                continue
            seen.add(h)
            out.append(h)
    return out


def extract_models(html, res):
    out = {}
    for pat in res:
        out[pat] = sorted(set(re.findall(pat, html)))
    return out


def main():
    url, o = parse(sys.argv[1:])
    if not url:
        print(json.dumps({"error": "no url given"}))
        return
    from playwright.sync_api import sync_playwright
    result = {"url": url, "jsonld_items": [], "hrefs": [], "models": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not o["headed"],
            args=["--disable-blink-features=AutomationControlled",
                  "--no-sandbox", "--lang=en-NZ"],
        )
        ctx = browser.new_context(
            user_agent=UA, viewport={"width": 1366, "height": 768},
            locale="en-NZ", timezone_id="Pacific/Auckland",
        )
        ctx.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
        page = ctx.new_page()
        nav_err = None
        # 带退避重试：反爬限流（如 LG Akamai 临时封 IP）时自动等待后重试
        for attempt in range(int(o["retries"])):
            try:
                page.goto(url, wait_until="domcontentloaded",
                          timeout=int(o["nav_timeout"]) * 1000)
                nav_err = None
                break
            except Exception as e:
                nav_err = type(e).__name__ + ": " + str(e)[:80]
                if int(o["retries"]) > 1 and attempt < int(o["retries"]) - 1:
                    time.sleep(20 + 20 * attempt)
                    continue
        for _ in range(o["scroll"]):
            try:
                page.mouse.wheel(0, 2000)
            except Exception:
                break
            page.wait_for_timeout(1200)
        page.wait_for_timeout(int(o["wait"] * 1000) + random.randint(0, 800))
        try:
            html = page.content()
        except Exception as e:
            print(json.dumps({"url": url, "error": "content: %s" % str(e)[:80]}))
            browser.close()
            return
        result["final_url"] = page.url
        try:
            result["title"] = page.title()
        except Exception:
            pass
        result["content_length"] = len(html)
        if nav_err:
            result["nav_error"] = nav_err
        if o["mode"] in ("jsonld", "all"):
            result["jsonld_items"] = extract_jsonld(html)
        if o["mode"] in ("hrefs", "all"):
            kws = o["href_kws"] or ["product", "fridge", "refriger"]
            result["hrefs"] = extract_hrefs(html, kws)
        if o["model_res"]:
            result["models"] = extract_models(html, o["model_res"])
        if o["shot"]:
            try:
                page.screenshot(path="fridge_scrape.png", timeout=20000)
                result["screenshot"] = "fridge_scrape.png"
            except Exception:
                pass
        if o["savehtml"]:
            with open("fridge_scrape.html", "w", encoding="utf-8") as f:
                f.write(html)
            result["html_saved"] = "fridge_scrape.html"
        browser.close()
    print(json.dumps(result, ensure_ascii=False)[:200000])


if __name__ == "__main__":
    main()