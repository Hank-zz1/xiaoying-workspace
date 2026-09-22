import re, sys

html_path = sys.argv[1]
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Map: car name text -> image URL (180x135 -> 400x300)
img_map = {
    # === MPV/旅行车 ===
    'B级': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2406/27/c9/430456769_1719462989895_400x300.jpg',
    'V级': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2501/21/c24/475561005_1737460523861_400x300.jpg',
    'EQV': None,  # Not on Pacific Auto
    '2系 多功能旅行车': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2601/09/c14/588522754_1767951575357_400x300.jpg',
    '纯电MPV(旗舰)': None,
    'C级 旅行版': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2512/05/c0/576788734_1764901405820_400x300.jpg',
    'E级 旅行版': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/02/c12/467675190_1733127701409_400x300.jpg',

    # === 纯电系列 ===
    'EQA 260 续航619km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c28/436606127_1722498910691_400x300.jpg',
    'EQB EQB260 / EQB350 4MATIC': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/01/c29/436607242_1722499383060_400x300.jpg',
    'EQE 500 4MATIC 先锋/豪华/旗舰 续航681km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/20/c21/465059454_1732086410026_400x300.jpg',
    'EQE SUV 500 4MATIC 先锋/豪华/旗舰': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2404/26/c13/419721287_1714092287217_400x300.jpg',
    'EQS 500 4MATIC 续航840km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c0/465259236_1732156665860_400x300.jpg',
    'EQS SUV 500 4MATIC 续航777km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c0/465259232_1732156412673_400x300.jpg',
    'C级 纯电版': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/24/c10/540171929_1753338856367_400x300.jpg',
    'CLA纯电(长轴)': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/06/c9/568551620_1762393753547_400x300.jpg',
    'iX1 eDrive25L / xDrive30L M运动': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2508/26/c83/548721620_1756223378162_400x300.jpg',
    'iX3 eDrive35L / eDrive40L 续航540km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2311/27/c0/394106317_1701049609771_400x300.jpg',
    'iX xDrive40 / xDrive50 / M60': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2502/07/c0/479442276_1738900178806_400x300.jpg',
    'i3 eDrive35L / 40L 曜夜/运动 续航550km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2510/23/c44/564990175_1761205054899_400x300.jpg',
    'i4 eDrive35 / eDrive40 / M50 续航570km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2412/04/c22/467931962_1733281492879_400x300.jpg',
    'i7 eDrive50L / xDrive60L / M70 续航625km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/19/c38/464822570_1731999510559_400x300.jpg',
    'Q4 e-tron 40/50 e-tron quattro': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2111/23/c73/285079703_1637638779857_400x300.jpg',
    'Q6L e-tron PPE平台 800V': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/26/c0/540723837_1753535460274_400x300.jpg',
    'A6 e-tron PPE 800V 续航700+km': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2602/28/c0/628642183_1772272996433_400x300.jpg',
    'e-tron GT J1平台 RS版 124.78万': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2503/05/c0/487120289_1741140421044_400x300.jpg',

    # === 性能车 (AMG) ===
    'A35 AMG': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/20/c34/465070371_1732092208307_400x300.jpg',
    'C43 / C63 AMG': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/07/c0/534755234_1751859827183_400x300.jpg',
    'CLE AMG': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2406/03/c21/426422661_1717408919898_400x300.jpg',
    'E53 AMG': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/19/c52/464845447_1732010129372_400x300.jpg',
    'S63 AMG': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2406/28/c2/430629610_1719544376915_400x300.jpg',
    'AMG GT 4-Door': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/19/c52/464845447_1732010129372_400x300.jpg',
    'AMG GT 63 S': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2507/23/c1/539769822_1753235373025_400x300.jpg',

    # === 性能车 (BMW M) ===
    'M340i / M3': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/01/c0/567441509_1762000256144_400x300.jpg',
    'M4 / M4 CSL': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c13/465274891_1732161323416_400x300.jpg',
    'M5': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2406/26/c5/430272169_1719372317739_400x300.jpg',
    'M8': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c10/465271905_1732160199797_400x300.jpg',
    'M8 Competition': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2411/21/c10/465271905_1732160199797_400x300.jpg',

    # === 性能车 (Audi S/RS) ===
    'S3 / RS3': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2306/05/c49/364572628_1685977168153_400x300.jpg',
    'S4 / RS5': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2506/26/c12/530166846_1750929740388_400x300.jpg',
    'RS5 Sportback': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2306/05/c49/364571839_1685977235627_400x300.jpg',
    'RS6 / RS7': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2503/05/c0/487120289_1741140421044_400x300.jpg',
    'R8 V10 5.2L 620马力（已停产）': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2203/01/c20/299850953_1646104502130_400x300.jpeg',

    # === MPV/旅行车 (性能) ===
    'M3 CS Touring': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2511/01/c0/567441509_1762000256144_400x300.jpg',
    'RS6 Avant': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2503/05/c0/487120289_1741140421044_400x300.jpg',
    '3系 Touring': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2409/29/c21/452310497_1727602620752_400x300.jpg',
    '5系 Touring': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2408/09/c1/438035604_1723176559317_400x300.jpg',
    'A4 Avant': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2102/18/c7/253920846_1613648502592_400x300.jpg',
    'A6 Avant / Allroad': 'https://img.pcauto.com.cn/images/upload/upc/tx/auto5/2305/22/c29/363656132_1684738511771_400x300.jpg',
}

replaced = 0
for name_text, img_url in img_map.items():
    if img_url is None:
        continue

    # Determine alt text
    alt_map = {
        'B级': '🚗 奔驰B级', 'V级': '🚐 奔驰V级',
        '2系 多功能旅行车': '🚗 宝马2系旅行车',
        'C级 旅行版': '🚗 奔驰C级旅行版', 'E级 旅行版': '🚗 奔驰E级旅行版',
        '纯电MPV(旗舰)': '⚡ 奔驰纯电MPV',
        'EQA 260 续航619km': '⚡ 奔驰EQA',
        'EQB EQB260 / EQB350 4MATIC': '⚡ 奔驰EQB',
        'EQE 500 4MATIC 先锋/豪华/旗舰 续航681km': '⚡ 奔驰EQE',
        'EQE SUV 500 4MATIC 先锋/豪华/旗舰': '⚡ 奔驰EQE SUV',
        'EQS 500 4MATIC 续航840km': '⚡ 奔驰EQS',
        'EQS SUV 500 4MATIC 续航777km': '⚡ 奔驰EQS SUV',
        'C级 纯电版': '⚡ 奔驰C级纯电',
        'CLA纯电(长轴)': '⚡ 奔驰CLA纯电',
        'iX1 eDrive25L / xDrive30L M运动': '⚡ 宝马iX1',
        'iX3 eDrive35L / eDrive40L 续航540km': '⚡ 宝马iX3',
        'iX xDrive40 / xDrive50 / M60': '⚡ 宝马iX',
        'i3 eDrive35L / 40L 曜夜/运动 续航550km': '⚡ 宝马i3',
        'i4 eDrive35 / eDrive40 / M50 续航570km': '⚡ 宝马i4',
        'i7 eDrive50L / xDrive60L / M70 续航625km': '⚡ 宝马i7',
        'Q4 e-tron 40/50 e-tron quattro': '⚡ 奥迪Q4 e-tron',
        'Q6L e-tron PPE平台 800V': '⚡ 奥迪Q6L e-tron',
        'A6 e-tron PPE 800V 续航700+km': '⚡ 奥迪A6L e-tron',
        'e-tron GT J1平台 RS版 124.78万': '⚡ 奥迪e-tron GT',
        'A35 AMG': '🏎️ 奔驰A35 AMG',
        'C43 / C63 AMG': '🏎️ 奔驰C级AMG',
        'CLE AMG': '🏎️ 奔驰CLE AMG',
        'E53 AMG': '🏎️ 奔驰E级AMG',
        'S63 AMG': '🏎️ 奔驰S级AMG',
        'AMG GT 4-Door': '🏎️ 奔驰AMG GT四门',
        'AMG GT 63 S': '🏎️ 奔驰AMG GT 63 S',
        'M340i / M3': '🏎️ 宝马M3',
        'M4 / M4 CSL': '🏎️ 宝马M4',
        'M5': '🏎️ 宝马M5',
        'M8': '🏎️ 宝马M8',
        'M8 Competition': '🏎️ 宝马M8 Competition',
        'S3 / RS3': '🏎️ 奥迪S3/RS3',
        'S4 / RS5': '🏎️ 奥迪S4/RS5',
        'RS5 Sportback': '🏎️ 奥迪RS5',
        'RS6 / RS7': '🏎️ 奥迪RS6/RS7',
        'R8 V10 5.2L 620马力（已停产）': '🏎️ 奥迪R8',
        'M3 CS Touring': '🏎️ 宝马M3 CS Touring',
        'RS6 Avant': '🏎️ 奥迪RS6 Avant',
        '3系 Touring': '🚗 宝马3系Touring',
        '5系 Touring': '🚗 宝马5系Touring',
        'A4 Avant': '🚗 奥迪A4 Avant',
        'A6 Avant / Allroad': '🚗 奥迪A6 Avant',
    }
    alt = alt_map.get(name_text, name_text)

    img_html = f'<div class="car-img-wrap"><img src="{img_url}" alt="{alt}"></div>'

    # Pattern: the car-name div directly inside a car-cell (no preceding car-img-wrap)
    # Look for car-name div that is NOT already preceded by car-img-wrap
    old = f'<div class="car-name">{name_text}</div>'

    # Only replace if the preceding content doesn't already have car-img-wrap
    # We check that there's no car-img-wrap in the same cell before this car-name
    # Since these are inline compact cells, we can check the pattern:
    #   car-cell ... car-name (no img-wrap before it)
    # We use a simple approach: find the car-name, check if preceded by car-img-wrap

    idx = 0
    count = 0
    while True:
        pos = html.find(old, idx)
        if pos == -1:
            break

        # Check if there's a car-img-wrap between the car-cell start and this car-name
        cell_start = html.rfind('<td class="car-cell', 0, pos)
        if cell_start != -1:
            between = html[cell_start:pos]
            if 'car-img-wrap' in between:
                # Already has image, skip
                idx = pos + len(old)
                continue

        # Replace this occurrence
        html = html[:pos] + img_html + html[pos:]
        idx = pos + len(img_html) + len(old)
        count += 1
        replaced += 1

    if count == 0:
        print(f"  WARNING: 未找到 '{name_text}'")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Added images to {replaced} car cells")
