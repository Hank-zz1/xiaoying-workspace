import re
import urllib.request
import json

# 直接从品牌页面提取系列ID和缩略图
def fetch_page(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode('utf-8', errors='ignore')

# 1. 提取奔驰品牌页面中的所有车型系列ID和缩略图
print("=== 提取奔驰车型 ===")
benz_html = fetch_page('https://price.pcauto.com.cn/auto/nb4/')

# 找所有 sgXXXX 链接和对应的图片
# 模式: 图片URL后面跟着车型名称，再后面有 sgXXXX 链接
pattern = r'(https://img\.pcauto\.com\.cn/[^\'"]+?_180x135\.jpg)'
img_positions = [(m.start(), m.group(1)) for m in re.finditer(pattern, benz_html)]

# 找所有 sgXXXX
sg_pattern = r'sg(\d+)'
sg_matches = [(m.start(), m.group(1)) for m in re.finditer(sg_pattern, benz_html)]

# 匹配图片到最近的sg
results = {}
for pos, img_url in img_positions:
    # 找这个图片之后最近的sg
    best_sg = None
    best_dist = float('inf')
    for sg_pos, sg_id in sg_matches:
        dist = sg_pos - pos
        if 0 < dist < 2000 and dist < best_dist:
            best_dist = dist
            best_sg = sg_id
    if best_sg:
        results[f"benz_sg{best_sg}"] = {"img": img_url, "sg": best_sg}

# 找车型名称
name_pattern = r'([\u4e00-\u9fa5a-zA-Z0-9\u2022\s\(\)（）+]+?)\s*\n*\s*(?:万|暂无报价|购置税)'
for pos, img_url in img_positions:
    # 在图片后找车型名称
    chunk = benz_html[pos:pos+500]
    name_match = re.search(r'>([\u4e00-\u9fa5A-Za-z0-9\u2022\(\)\+]+?)\s*<', chunk)
    if name_match:
        name = name_match.group(1).strip()
        best_sg = None
        best_dist = float('inf')
        for sg_pos, sg_id in sg_matches:
            dist = sg_pos - pos
            if 0 < dist < 2000 and dist < best_dist:
                best_dist = dist
                best_sg = sg_id
        if best_sg and len(name) < 30:
            results[name] = {"img": img_url, "sg": best_sg}

for name, info in sorted(results.items()):
    print(f"  {name}: sg{info['sg']} -> {info['img'][:80]}...")

print(f"\n共找到 {len(results)} 个奔驰车型")

# 2. 提取宝马品牌页面
print("\n=== 提取宝马车型 ===")
bmw_html = fetch_page('https://price.pcauto.com.cn/auto/nb20/')

img_positions = [(m.start(), m.group(1)) for m in re.finditer(pattern, bmw_html)]
sg_matches = [(m.start(), m.group(1)) for m in re.finditer(sg_pattern, bmw_html)]

bmw_results = {}
for pos, img_url in img_positions:
    chunk = bmw_html[pos:pos+500]
    name_match = re.search(r'>([\u4e00-\u9fa5A-Za-z0-9\u2022\(\)\+iX]+?)\s*<', chunk)
    if name_match:
        name = name_match.group(1).strip()
        best_sg = None
        best_dist = float('inf')
        for sg_pos, sg_id in sg_matches:
            dist = sg_pos - pos
            if 0 < dist < 2000 and dist < best_dist:
                best_dist = dist
                best_sg = sg_id
        if best_sg and len(name) < 30:
            bmw_results[name] = {"img": img_url, "sg": best_sg}

for name, info in sorted(bmw_results.items()):
    print(f"  {name}: sg{info['sg']} -> {info['img'][:80]}...")

print(f"\n共找到 {len(bmw_results)} 个宝马车型")

# 3. 提取奥迪品牌页面
print("\n=== 提取奥迪车型 ===")
audi_html = fetch_page('https://price.pcauto.com.cn/auto/nb3/')

img_positions = [(m.start(), m.group(1)) for m in re.finditer(pattern, audi_html)]
sg_matches = [(m.start(), m.group(1)) for m in re.finditer(sg_pattern, audi_html)]

audi_results = {}
for pos, img_url in img_positions:
    chunk = audi_html[pos:pos+500]
    name_match = re.search(r'>([\u4e00-\u9fa5A-Za-z0-9\u2022\(\)\+e-tron]+?)\s*<', chunk)
    if name_match:
        name = name_match.group(1).strip()
        best_sg = None
        best_dist = float('inf')
        for sg_pos, sg_id in sg_matches:
            dist = sg_pos - pos
            if 0 < dist < 2000 and dist < best_dist:
                best_dist = dist
                best_sg = sg_id
        if best_sg and len(name) < 30:
            audi_results[name] = {"img": img_url, "sg": best_sg}

for name, info in sorted(audi_results.items()):
    print(f"  {name}: sg{info['sg']} -> {info['img'][:80]}...")

print(f"\n共找到 {len(audi_results)} 个奥迪车型")

# 输出JSON
print("\n\n=== JSON OUTPUT ===")
print(json.dumps({"benz": results, "bmw": bmw_results, "audi": audi_results}, indent=2, ensure_ascii=False))
