import json
import re

# 奔驰品牌页面HTML片段（从fetch结果提取）
benz_html = """
奔驰E级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438032982_1723174492049_180x135.jpg
奔驰GLC
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/05/c0/576722038_1764899702513_180x135.jpg
奔驰CLA级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2603/04/c3/631493692_1772593164963_180x135.jpg
奔驰A级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c2/438045665_1723182705958_180x135.jpg
奔驰EQA
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c28/436606127_1722498910691_180x135.jpg
奔驰EQB
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c29/436607242_1722499383060_180x135.jpg
奔驰EQE
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/20/c21/465059454_1732086410026_180x135.jpg
奔驰EQE SUV
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2404/26/c13/419721287_1714092287217_180x135.jpg
奔驰GLA
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c15/396650684_1702361163616_180x135.jpg
奔驰GLB
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c18/396660114_1702365891493_180x135.jpg
奔驰C级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/05/c0/576788734_1764901405820_180x135.jpg
奔驰GLE
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2307/14/c6/371036873_1689332845232_180x135.jpg
奔驰CLA级(进口)
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/06/c0/568517340_1762363138748_180x135.jpg
奔驰CLE
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/20/c6/475350829_1737356599480_180x135.jpg
奔驰GLC轿跑(进口)
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2602/05/c3/609182805_1770263435980_180x135.jpg
奔驰GLE轿跑
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/28/c13/467121628_1732775673978_180x135.jpg
奔驰GLS
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2405/23/c6/424492781_1716450576204_180x135.jpg
奔驰G级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/19/c0/475190069_1737286175120_180x135.jpg
奔驰S级
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438039521_1723178316074_180x135.jpg
奔驰EQS
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c0/465259236_1732156665860_180x135.jpg
AMG GT
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/23/c1/539769822_1753235373025_180x135.jpg
"""

# 宝马品牌页面HTML片段
bmw_html = """
宝马2系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2504/02/c9/497117255_1743589146604_180x135.jpg
宝马3系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2409/29/c21/452310497_1727602620752_180x135.jpg
宝马5系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438035604_1723176559317_180x135.jpg
宝马X1
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c59/564997046_1761208935471_180x135.jpg
宝马X3
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2601/24/c3/599134501_1769264387491_180x135.jpg
宝马X5
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c59/564996992_1761208826437_180x135.jpg
宝马i3
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c44/564990175_1761205054899_180x135.jpg
宝马iX1
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2508/26/c83/548721620_1756223378162_180x135.jpg
宝马iX3
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2311/27/c0/394106317_1701049609771_180x135.jpg
宝马4系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/02/c12/467675515_1733128537256_180x135.jpg
宝马i4
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/04/c22/467931962_1733281492879_180x135.jpg
宝马2系(进口)
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2601/09/c14/588522754_1767951575357_180x135.jpg
宝马7系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/19/c4/363506221_1684459832502_180x135.jpg
宝马8系
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c20/465289094_1732168496404_180x135.jpg
宝马X2(进口)
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c17/465277985_1732162158873_180x135.jpg
宝马X6
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c17/465277985_1732162158873_180x135.jpg
宝马X7
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/24/c36/363783087_1684933911376_180x135.jpg
宝马Z4
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c13/465275286_1732161050395_180x135.jpg
宝马iX
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2502/07/c0/479442276_1738900178806_180x135.jpg
宝马i7
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/19/c38/464822570_1731999510559_180x135.jpg
"""

# 奥迪品牌页面HTML片段
audi_html = """
奥迪A6L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2603/25/c19/648283830_1774406013099_180x135.jpg
奥迪A3
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/01/c14/460499604_1730469207566_180x135.jpg
奥迪A4L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/05/c1/468087269_1733377937274_180x135.jpg
奥迪A5L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/08/c20/577660111_1765181128108_180x135.jpg
奥迪Q2L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/11/c6/570165423_1762851375812_180x135.jpg
奥迪Q3
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c18/396661138_1702366907185_180x135.jpg
奥迪Q3 Sportback
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/29/c1/541390337_1753772043488_180x135.jpg
奥迪Q4 e-tron
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2111/23/c73/285079703_1637638779857_180x135.jpg
奥迪Q5L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2602/02/c0/606062618_1769996853876_180x135.jpg
奥迪Q5L Sportback
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/24/c24/476285378_1737715782300_180x135.jpg
奥迪A5L Sportback
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/06/c53/568753443_1762421197561_180x135.jpg
奥迪A7L
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2506/10/c0/522785845_1749521634591_180x135.jpg
奥迪Q6
https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/24/c26/540182356_1753352126708_180x135.jpg
"""

def extract_model_images(html_text):
    """Extract model name -> thumbnail URL mapping"""
    lines = html_text.strip().split('\n')
    results = {}
    for i in range(0, len(lines)-1):
        line = lines[i].strip()
        next_line = lines[i+1].strip()
        if next_line.startswith('https://img.pcauto.com.cn') and '_180x135.jpg' in next_line:
            results[line] = next_line
    return results

print("=== 奔驰车型缩略图 ===")
benz_models = extract_model_images(benz_html)
for name, url in sorted(benz_models.items()):
    print(f"  {name}: {url}")

print("\n=== 宝马车型缩略图 ===")
bmw_models = extract_model_images(bmw_html)
for name, url in sorted(bmw_models.items()):
    print(f"  {name}: {url}")

print("\n=== 奥迪车型缩略图 ===")
audi_models = extract_model_images(audi_html)
for name, url in sorted(audi_models.items()):
    print(f"  {name}: {url}")

# 映射到HTML中的车型ID
# 需要根据HTML中使用的placeholder名称来匹配
mapping = {
    # 奔驰
    "benz_a": "奔驰A级",
    "benz_c": "奔驰C级",
    "benz_e": "奔驰E级",
    "benz_s": "奔驰S级",
    "benz_cla": "奔驰CLA级",
    "benz_cle": "奔驰CLE",
    "benz_gla": "奔驰GLA",
    "benz_glb": "奔驰GLB",
    "benz_glc": "奔驰GLC",
    "benz_gle": "奔驰GLE",
    "benz_gls": "奔驰GLS",
    "benz_g": "奔驰G级",
    "benz_gle_coupe": "奔驰GLE轿跑",
    "benz_glc_coupe": "奔驰GLC轿跑(进口)",
    "benz_amg_gt": "AMG GT",
    "benz_eqa": "奔驰EQA",
    "benz_eqb": "奔驰EQB",
    "benz_eqe": "奔驰EQE",
    "benz_eqe_suv": "奔驰EQE SUV",
    "benz_eqs": "奔驰EQS",

    # 宝马
    "bmw_1": None,  # 页面没有1系，用宝马2系替代
    "bmw_2gc": "宝马2系(进口)",
    "bmw_3": "宝马3系",
    "bmw_5": "宝马5系",
    "bmw_7": "宝马7系",
    "bmw_4": "宝马4系",
    "bmw_6gt": None,  # 页面没有6系GT
    "bmw_8gc": "宝马8系",
    "bmw_z4": "宝马Z4",
    "bmw_x1": "宝马X1",
    "bmw_x2": "宝马X2(进口)",
    "bmw_x3": "宝马X3",
    "bmw_x4": None,  # 页面没有X4
    "bmw_x5": "宝马X5",
    "bmw_x6": "宝马X6",
    "bmw_x7": "宝马X7",
    "bmw_ix": "宝马iX",
    "bmw_ix1": "宝马iX1",
    "bmw_ix3": "宝马iX3",
    "bmw_i3": "宝马i3",
    "bmw_i4": "宝马i4",
    "bmw_i7": "宝马i7",

    # 奥迪
    "audi_a3": "奥迪A3",
    "audi_a4": "奥迪A4L",
    "audi_a5": "奥迪A5L",
    "audi_a6": "奥迪A6L",
    "audi_a7": None,  # 页面没有A7
    "audi_a8": None,  # 页面没有A8
    "audi_tt": None,  # 页面没有TT
    "audi_r8": None,  # 页面没有R8
    "audi_q2": "奥迪Q2L",
    "audi_q3": "奥迪Q3",
    "audi_q3_sb": "奥迪Q3 Sportback",
    "audi_q5": "奥迪Q5L",
    "audi_q7": None,  # 页面没有Q7
    "audi_q8": None,  # 页面没有Q8
    "audi_q4": "奥迪Q4 e-tron",
    "audi_etron_gt": None,  # 页面没有e-tron GT
}

# 升级URL：180x135 -> 400x300
def upgrade_url(url):
    if url is None:
        return None
    return url.replace('_180x135.jpg', '_400x300.jpg')

print("\n\n=== 映射结果 ===")
final_images = {}
for model_id, page_name in mapping.items():
    if page_name and page_name in benz_models:
        url = upgrade_url(benz_models[page_name])
        final_images[model_id] = url
        print(f"  {model_id} -> {page_name} -> {url}")
    elif page_name and page_name in bmw_models:
        url = upgrade_url(bmw_models[page_name])
        final_images[model_id] = url
        print(f"  {model_id} -> {page_name} -> {url}")
    elif page_name and page_name in audi_models:
        url = upgrade_url(audi_models[page_name])
        final_images[model_id] = url
        print(f"  {model_id} -> {page_name} -> {url}")
    else:
        print(f"  {model_id} -> NOT FOUND (page_name: {page_name})")

# 输出JSON
print("\n\n=== JSON OUTPUT ===")
print(json.dumps(final_images, indent=2, ensure_ascii=False))
