import json, sys

# 太平洋汽车CDN图片URL映射 (中国大陆可访问)
car_images = {
    # === 奔驰 ===
    "benz_a": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c2/438045665_1723182705958_400x300.jpg",
    "benz_c": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/05/c0/576788734_1764901405820_400x300.jpg",
    "benz_e": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438032982_1723174492049_400x300.jpg",
    "benz_s": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438039521_1723178316074_400x300.jpg",
    "benz_cla": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2603/04/c3/631493692_1772593164963_400x300.jpg",
    "benz_cle": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/20/c6/475350829_1737356599480_400x300.jpg",
    "benz_gla": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c15/396650684_1702361163616_400x300.jpg",
    "benz_glb": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c18/396660114_1702365891493_400x300.jpg",
    "benz_glc": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/05/c0/576722038_1764899702513_400x300.jpg",
    "benz_gle": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2307/14/c6/371036873_1689332845232_400x300.jpg",
    "benz_gls": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2405/23/c6/424492781_1716450576204_400x300.jpg",
    "benz_g": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/19/c0/475190069_1737286175120_400x300.jpg",
    "benz_gle_coupe": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/28/c13/467121628_1732775673978_400x300.jpg",
    "benz_glc_coupe": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2602/05/c3/609182805_1770263435980_400x300.jpg",
    "benz_amg_gt": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/23/c1/539769822_1753235373025_400x300.jpg",
    "benz_eqa": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c28/436606127_1722498910691_400x300.jpg",
    "benz_eqb": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c29/436607242_1722499383060_400x300.jpg",
    "benz_eqe": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/20/c21/465059454_1732086410026_400x300.jpg",
    "benz_eqe_suv": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2404/26/c13/419721287_1714092287217_400x300.jpg",
    "benz_eqs": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c0/465259236_1732156665860_400x300.jpg",
    # === 宝马 ===
    "bmw_1": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2504/02/c9/497117255_1743589146604_400x300.jpg",
    "bmw_2gc": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2601/09/c14/588522754_1767951575357_400x300.jpg",
    "bmw_3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2409/29/c21/452310497_1727602620752_400x300.jpg",
    "bmw_5": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438035604_1723176559317_400x300.jpg",
    "bmw_7": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/19/c4/363506221_1684459832502_400x300.jpg",
    "bmw_4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/02/c12/467675515_1733128537256_400x300.jpg",
    "bmw_6gt": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c20/465289094_1732168496404_400x300.jpg",
    "bmw_8gc": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c20/465289094_1732168496404_400x300.jpg",
    "bmw_z4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c13/465275286_1732161050395_400x300.jpg",
    "bmw_x1": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c59/564997046_1761208935471_400x300.jpg",
    "bmw_x2": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c17/465277985_1732162158873_400x300.jpg",
    "bmw_x3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2601/24/c3/599134501_1769264387491_400x300.jpg",
    "bmw_x4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/23/c39/363722208_1684830738284_400x300.jpg",
    "bmw_x5": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c59/564996992_1761208826437_400x300.jpg",
    "bmw_x6": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c17/465277985_1732162158873_400x300.jpg",
    "bmw_x7": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/24/c36/363783087_1684933911376_400x300.jpg",
    "bmw_ix": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2502/07/c0/479442276_1738900178806_400x300.jpg",
    "bmw_ix1": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2508/26/c83/548721620_1756223378162_400x300.jpg",
    "bmw_ix3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2311/27/c0/394106317_1701049609771_400x300.jpg",
    "bmw_i3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c44/564990175_1761205054899_400x300.jpg",
    "bmw_i4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/04/c22/467931962_1733281492879_400x300.jpg",
    "bmw_i7": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/19/c38/464822570_1731999510559_400x300.jpg",
    # === 奥迪 ===
    "audi_a3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/01/c14/460499604_1730469207566_400x300.jpg",
    "audi_a4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/05/c1/468087269_1733377937274_400x300.jpg",
    "audi_a5": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/08/c20/577660111_1765181128108_400x300.jpg",
    "audi_a6": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2603/25/c19/648283830_1774406013099_400x300.jpg",
    "audi_a7": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c62/465323582_1732183091496_400x300.jpg",
    "audi_a8": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2406/28/c1/430589023_1719540132520_400x300.jpg",
    "audi_q2": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/11/c6/570165423_1762851375812_400x300.jpg",
    "audi_q3": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2312/12/c18/396661138_1702366907185_400x300.jpg",
    "audi_q3_sb": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/29/c1/541390337_1753772043488_400x300.jpg",
    "audi_q5": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2602/02/c0/606062618_1769996853876_400x300.jpg",
    "audi_q7": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2407/30/c6/436164226_1722313190899_400x300.jpg",
    "audi_q8": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/01/c13/460480490_1730457274138_400x300.jpg",
    "audi_q4": "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2111/23/c73/285079703_1637638779857_400x300.jpg",
}

# 读入HTML
html_path = sys.argv[1]
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Additional images for discontinued models (found on mobile gallery pages)
car_images['audi_tt'] = "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/1810/08/c23/113200374_1538981971574_400x300.jpg"
car_images['audi_r8'] = "https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2203/01/c20/299850953_1646104502130_400x300.jpeg"

# 替换规则: alt text -> 新图片URL
replacements = [
    ('🚗 奔驰A级', car_images['benz_a']),
    ('🚗 奔驰C级', car_images['benz_c']),
    ('🚗 奔驰E级', car_images['benz_e']),
    ('🚗 奔驰S级', car_images['benz_s']),
    ('🚗 奔驰CLA', car_images['benz_cla']),
    ('🚗 奔驰CLE', car_images['benz_cle']),
    ('🚙 奔驰GLA', car_images['benz_gla']),
    ('🚙 奔驰GLB', car_images['benz_glb']),
    ('🚙 奔驰GLC', car_images['benz_glc']),
    ('🚙 奔驰GLE', car_images['benz_gle']),
    ('🚙 奔驰GLS', car_images['benz_gls']),
    ('🏔️ 奔驰G级', car_images['benz_g']),
    ('🚙 奔驰GLE Coupe', car_images['benz_gle_coupe']),
    ('🚙 奔驰GLC Coupe', car_images['benz_glc_coupe']),
    ('🏎️ AMG GT', car_images['benz_amg_gt']),
    ('🚗 宝马1系', car_images['bmw_1']),
    ('🚗 宝马2系GC', car_images['bmw_2gc']),
    ('🚗 宝马3系', car_images['bmw_3']),
    ('🚗 宝马5系', car_images['bmw_5']),
    ('🚗 宝马7系', car_images['bmw_7']),
    ('🚗 宝马4系', car_images['bmw_4']),
    ('🚗 宝马6系GT', car_images['bmw_6gt']),
    ('🚗 宝马8系GC', car_images['bmw_8gc']),
    ('🏎️ 宝马Z4', car_images['bmw_z4']),
    ('🚙 宝马X1', car_images['bmw_x1']),
    ('🚙 宝马X2', car_images['bmw_x2']),
    ('🚙 宝马X3', car_images['bmw_x3']),
    ('🚙 宝马X4', car_images['bmw_x4']),
    ('🚙 宝马X5', car_images['bmw_x5']),
    ('🚙 宝马X6', car_images['bmw_x6']),
    ('🚙 宝马X7', car_images['bmw_x7']),
    ('🚗 奥迪A3', car_images['audi_a3']),
    ('🚗 奥迪A4L/A5L', car_images['audi_a4']),
    ('🚗 奥迪A5', car_images['audi_a5']),
    ('🚗 奥迪A6L', car_images['audi_a6']),
    ('🚗 奥迪A7', car_images['audi_a7']),
    ('🚗 奥迪A8L', car_images['audi_a8']),
    ('🚙 奥迪Q2L', car_images['audi_q2']),
    ('🚙 奥迪Q3', car_images['audi_q3']),
    ('🚙 奥迪Q3 Sportback', car_images['audi_q3_sb']),
    ('🚙 奥迪Q5L', car_images['audi_q5']),
    ('🚙 奥迪Q7', car_images['audi_q7']),
    ('🚙 奥迪Q8', car_images['audi_q8']),
    ('🏎️ 奥迪TT', car_images['audi_tt']),
    ('🏎️ 奥迪R8', car_images['audi_r8']),
]

replaced = 0
for alt_text, new_url in replacements:
    # 匹配 <img src="..." alt="车型名">
    import re
    pattern = r'(<img\s+)src="[^"]*"\s+(alt="' + re.escape(alt_text) + '")'
    replacement = r'\1src="' + new_url + r'" \2'
    new_html, count = re.subn(pattern, replacement, html)
    if count > 0:
        replaced += count
        html = new_html
    else:
        print(f"  WARNING: 未找到 '{alt_text}' 的图片")

# 写回
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Replaced {replaced} image URLs with Pacific Auto CDN")
