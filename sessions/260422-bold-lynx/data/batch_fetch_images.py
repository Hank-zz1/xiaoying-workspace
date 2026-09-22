import re
import urllib.request
import json

# 车型系列ID映射 - 太平洋汽车
# 已知ID从之前的搜索和抓取中获取
model_ids = {
    # === 奔驰 (Mercedes-Benz) ===
    "benz_a": 22951,
    "benz_c": 3178,
    "benz_e": 1603,
    "benz_s": 267,
    "benz_cla": 7750,
    "benz_cle": 29162,
    "benz_gla": 12181,
    "benz_glb": 24905,
    "benz_glc": 12975,
    "benz_g": 138,
    "benz_gls": 13361,
    "benz_glc_coupe": 11532,
    # 以下ID需要查找
    "benz_gle": None,
    "benz_gle_coupe": None,
    "benz_amg_gt": None,
    "benz_eqa": None,
    "benz_eqb": None,
    "benz_eqe": None,
    "benz_eqe_suv": None,
    "benz_eqs": None,

    # === 宝马 (BMW) ===
    "bmw_1": None,
    "bmw_2gc": None,
    "bmw_3": 424,
    "bmw_4": None,
    "bmw_5": None,
    "bmw_6gt": None,
    "bmw_7": None,
    "bmw_8gc": None,
    "bmw_z4": None,
    "bmw_x1": 7209,
    "bmw_x2": None,
    "bmw_x3": None,
    "bmw_x4": None,
    "bmw_x5": None,
    "bmw_x6": None,
    "bmw_x7": None,
    "bmw_ix": None,
    "bmw_ix1": None,
    "bmw_ix3": None,
    "bmw_i3": None,
    "bmw_i4": None,
    "bmw_i7": None,

    # === 奥迪 (Audi) ===
    "audi_a3": None,
    "audi_a4": None,
    "audi_a5": None,
    "audi_a6": None,
    "audi_a7": None,
    "audi_a8": None,
    "audi_tt": None,
    "audi_r8": None,
    "audi_q2": None,
    "audi_q3": None,
    "audi_q3_sb": None,
    "audi_q5": None,
    "audi_q7": None,
    "audi_q8": None,
    "audi_q4": None,
    "audi_etron_gt": None,
}

# 常见车型系列ID（从网上搜索补充）
# 奔驰
model_ids.update({
    "benz_gle": 10700,
    "benz_gle_coupe": 27491,
    "benz_amg_gt": 23676,
    "benz_eqa": 27844,
    "benz_eqb": 28457,
    "benz_eqe": 28708,
    "benz_eqe_suv": 29164,
    "benz_eqs": 27843,
})

# 宝马
model_ids.update({
    "bmw_1": 5545,
    "bmw_2gc": 26618,
    "bmw_4": 10790,
    "bmw_5": 2931,
    "bmw_6gt": 21265,
    "bmw_7": 1387,
    "bmw_8gc": 23501,
    "bmw_z4": 5612,
    "bmw_x2": 21834,
    "bmw_x3": 2993,
    "bmw_x4": 7748,
    "bmw_x5": 4093,
    "bmw_x6": 5851,
    "bmw_x7": 23500,
    "bmw_ix": 28178,
    "bmw_ix1": 29482,
    "bmw_ix3": 25762,
    "bmw_i3": 29216,
    "bmw_i4": 28179,
    "bmw_i7": 28706,
})

# 奥迪
model_ids.update({
    "audi_a3": 2658,
    "audi_a4": 2933,
    "audi_a5": 5435,
    "audi_a6": 2995,
    "audi_a7": 8854,
    "audi_a8": 2679,
    "audi_tt": 2650,
    "audi_r8": 4100,
    "audi_q2": 16291,
    "audi_q3": 8860,
    "audi_q3_sb": 25614,
    "audi_q5": 5653,
    "audi_q7": 4140,
    "audi_q8": 23274,
    "audi_q4": 27819,
    "audi_etron_gt": 27845,
})

def fetch_gallery(sg_id):
    """Fetch the gallery page and extract first image URL"""
    if sg_id is None:
        return None
    url = f"https://price.pcauto.com.cn/cars/sg{sg_id}-o1-3/"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        # Extract all img.pcauto.com.cn image URLs
        pattern = r'https://img\.pcauto\.com\.cn/images/upload/upc/tx/auto5/[^"\'\s]+_400x300\.jpg'
        matches = re.findall(pattern, html)
        if matches:
            return matches[0]
        return None
    except Exception as e:
        return f"ERROR: {str(e)}"

# Fetch all
results = {}
for model_id, sg_id in model_ids.items():
    if sg_id is None:
        continue
    print(f"Fetching {model_id} (sg{sg_id})...", flush=True)
    img_url = fetch_gallery(sg_id)
    results[model_id] = {
        'sg_id': sg_id,
        'image_url': img_url,
        'status': 'OK' if img_url and not img_url.startswith('ERROR') else 'FAILED'
    }
    if img_url:
        print(f"  -> {img_url[:80]}..." if len(img_url) > 80 else f"  -> {img_url}")
    else:
        print(f"  -> No image found")

# Output JSON
print("\n\n=== RESULTS ===")
print(json.dumps(results, indent=2, ensure_ascii=False))
