import re, sys

html_path = sys.argv[1]
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 配置型号映射: 原车型名 -> 新车型名(含配置型号)
# 格式: (搜索文本, 替换文本)
replacements = [
    # === 轿车系列 ===
    # A级 (奔驰A级: A180L, A200L 时尚型)
    ('<div class="car-name">A级</div>', '<div class="car-name">A级 A180L / A200L</div>'),
    # 1系 (宝马1系: 120i M运动)
    ('<div class="car-name">1系</div>', '<div class="car-name">1系 120i / M运动</div>'),
    # A3 (奥迪A3: 35 TFSI / 40 TFSI, 进取/时尚/运动)
    ('<div class="car-name">A3</div>', '<div class="car-name">A3 35 TFSI / 40 TFSI</div>'),

    # C级 (奔驰C级: C200L 运动版 33.83万, C260L 运动版 36.03万, C260L 皓夜运动版 38.41万)
    ('<div class="car-name">C级</div>', '<div class="car-name">C级 C200L / C260L</div>'),
    # 3系 (宝马3系: 325i M运动 25.80万, 325Li M运动 27.80万, 330i/330Li M运动曜夜 29.80-33.80万)
    ('<div class="car-name">3系 🔥</div>', '<div class="car-name">3系 325i / 325Li / 330Li 🔥</div>'),
    # A4L/A5L (奥迪A4L: 40 TFSI 时尚/豪华 29.70-32.18万; 2025换代为A5L)
    ('<div class="car-name">A4L / A5L</div>', '<div class="car-name">A4L 40 TFSI → A5L 换代</div>'),

    # E级 (奔驰E级: E260L 经典版 42.99万, E260L 45.18万, E260L 4MATIC 47.78万, E300L 时尚/豪华/尊贵 49.98-59.98万)
    ('<div class="car-name">E级 🏆</div>', '<div class="car-name">E级 E260L / E300L 时尚/豪华/尊贵 🏆</div>'),
    # 5系 (宝马5系: 525Li 豪华/M运动 36.80万, 530Li 领先型 40.80万, 530Li xDrive 42.80万, 530Li 尊享型 44.80万)
    ('<div class="car-name">5系</div>', '<div class="car-name">5系 525Li / 530Li 领先/尊享/xDrive</div>'),
    # A6L (奥迪A6L: 40 TFSI 豪华动感 42.79万, 45 TFSI 臻选 45.49万, 45 TFSI quattro 臻选/尊享 47.99-49.98万, 55 TFSI quattro 尊享/旗舰 55.89-65.68万)
    ('<div class="car-name">A6L</div>', '<div class="car-name">A6L 40 TFSI / 45 TFSI / 55 TFSI quattro</div>'),

    # S级 (奔驰S级: S400L 商务/豪华 96.26-103.89万, S450L 4MATIC 130.26万, S500L 4MATIC 200.20万)
    ('<div class="car-name">S级</div>', '<div class="car-name">S级 S400L / S450L / S500L 4MATIC</div>'),
    # 7系 (宝马7系: 735Li M运动 82.80万, 740Li 领先型 106.80万, 740Li 尊享型 118.80万, 760Li xDrive 240.80万)
    ('<div class="car-name">7系</div>', '<div class="car-name">7系 735Li / 740Li / 760Li xDrive</div>'),
    # A8L (奥迪A8L: A8L 45 TFSI quattro 豪华型 82.98万, A8L 50 TFSI quattro 尊享型 88.98万, A8L 55 TFSI quattro 旗舰型 103.68万)
    ('<div class="car-name">A8L</div>', '<div class="car-name">A8L 45 TFSI / 50 TFSI / 55 TFSI quattro</div>'),

    # === 轿跑/跑车 ===
    # CLA级 (奔驰CLA: CLA200 29.98万, CLA220 37.28万, CLA260 4MATIC 40.98万)
    ('<div class="car-name">CLA级</div>', '<div class="car-name">CLA级 CLA200 / CLA220 / CLA260 4MATIC</div>'),
    # 2系 Gran Coupe (宝马2系GC: 225i M运动套装 26.98万, 225i M运动曜夜套装 29.98万)
    ('<div class="car-name">2系 Gran Coupe</div>', '<div class="car-name">2系GC 225i M运动/曜夜</div>'),

    # CLE Coupe (奔驰CLE: CLE260 轿跑 45.76万, CLE300 4MATIC 轿跑 55.23万, CLE260 敞篷 51.98万, CLE300 4MATIC 敞篷 59.63万)
    ('<div class="car-name">CLE Coupe</div>', '<div class="car-name">CLE CLE260 / CLE300 4MATIC 轿跑/敞篷</div>'),
    # 4系 Coupe (宝马4系: 425i M运动 37.99万, 430i M运动曜夜 47.99万)
    ('<div class="car-name">4系 Coupe</div>', '<div class="car-name">4系 425i / 430i M运动曜夜</div>'),
    # A5 Coupe (奥迪A5: A5 Coupe 进口, 40 TFSI / 45 TFSI quattro)
    ('<div class="car-name">A5 Coupe</div>', '<div class="car-name">A5 40 TFSI / 45 TFSI quattro 进口</div>'),

    # 6系 GT (宝马6系GT: 630i M运动 58.39万, 630i 豪华设计套装 63.39万, 630i M运动曜夜套装 68.39万)
    ('<div class="car-name">6系 GT</div>', '<div class="car-name">6系GT 630i M运动/豪华/曜夜</div>'),
    # A7/A7L (奥迪A7: A7 45 TFSI 臻选型 58.58万, A7 55 TFSI quattro 尊享型 78.48万; A7L 45 TFSI quattro 41.87万起)
    ('<div class="car-name">A7 / A7L</div>', '<div class="car-name">A7 45/55 TFSI / A7L 45 TFSI quattro</div>'),

    # 8系 Gran Coupe (宝马8系: 840i xDrive M运动 96.80万, 840i Gran Coupe 雷霆版 118.80万)
    ('<div class="car-name">8系 Gran Coupe</div>', '<div class="car-name">8系 840i xDrive / Gran Coupe 雷霆</div>'),

    # Z4 (宝马Z4: sDrive 25i M运动套装 48.98万, sDrive 30i M运动曜夜套装 63.38万)
    ('<div class="car-name">Z4</div>', '<div class="car-name">Z4 sDrive 25i / 30i M运动曜夜</div>'),
    # TT (奥迪TT: 40 TFSI 时尚型 45.38万, 45 TFSI quattro 性能版 52.18万)
    ('<div class="car-name">TT</div>', '<div class="car-name">TT 40 TFSI / 45 TFSI quattro 进口</div>'),

    # AMG GT (奔驰AMG GT: AMG GT50 134.48万, AMG GT55 161.68万, AMG GT63 S E Performance 228.50万)
    ('<div class="car-name">AMG GT</div>', '<div class="car-name">AMG GT GT50 / GT55 / GT63 S</div>'),
    # R8 (奥迪R8: 已停产, V10 Coupe Performance, 5.2L V10 自然吸气, 620马力)
    ('<div class="car-name">R8</div>', '<div class="car-name">R8 V10 5.2L 620马力（已停产）</div>'),

    # === SUV 系列 ===
    # GLA (奔驰GLA: GLA200 28.69万, GLA220 34.69万)
    ('<div class="car-name">GLA</div>', '<div class="car-name">GLA GLA200 / GLA220</div>'),
    # Q2L (奥迪Q2L: 35 TFSI 进取动感型 17.18万, 进取致雅型, 豪华动感型, RS套件燃速型 19.28万)
    ('<div class="car-name">Q2L</div>', '<div class="car-name">Q2L 35 TFSI 进取/豪华/RS套件 17.18万起</div>'),

    # GLB (奔驰GLB: GLB200 时尚型 31.19万, GLB220 时尚型 34.99万, GLB220 4MATIC 36.79万)
    ('<div class="car-name">GLB</div>', '<div class="car-name">GLB GLB200 / GLB220 5/7座 4MATIC</div>'),
    # X1 (宝马X1: sDrive20Li X设计套装 28.89万, sDrive25Li X设计套装 31.69万, sDrive25Li M运动套装 31.69万, xDrive25Li M运动套装 34.99万, xDrive25Li X设计套装 34.99万)
    ('<div class="car-name">X1</div>', '<div class="car-name">X1 sDrive20Li / sDrive25Li / xDrive25Li</div>'),
    # Q3 (奥迪Q3: 35 TFSI 进取动感型 27.98万, 35 TFSI 时尚动感型, 40 TFSI 时尚动感型 30.58万, 45 TFSI quattro 时尚动感型 34.38万)
    ('<div class="car-name">Q3</div>', '<div class="car-name">Q3 35 TFSI / 40 TFSI / 45 TFSI quattro</div>'),

    # GLC (奔驰GLC: GLC260L 经典版 39.98万, GLC260L 动感型 42.78万, GLC300L 动感型 46.38万, GLC300L 豪华型 53.13万)
    ('<div class="car-name">GLC 🏆</div>', '<div class="car-name">GLC GLC260L / GLC300L 4MATIC 🏆</div>'),
    # X3 (宝马X3: xDrive25L 豪华套装 34.99万, xDrive25L M运动套装 34.99万, xDrive30L 领先型 39.99万, xDrive30L 尊享型 44.99万)
    ('<div class="car-name">X3</div>', '<div class="car-name">X3 xDrive25L / xDrive30L 豪华/M运动</div>'),
    # Q5L (奥迪Q5L: 40 TFSI 豪华动感型 39.88万, 40 TFSI 豪华致雅型, 45 TFSI 豪华动感型 45.38万, 45 TFSI 臻选动感型 48.88万)
    ('<div class="car-name">Q5L</div>', '<div class="car-name">Q5L 40 TFSI / 45 TFSI 豪华/臻选</div>'),

    # GLE (奔驰GLE: GLE350 4MATIC 时尚型 69.98万, GLE350 4MATIC 动感型 74.18万, GLE450 4MATIC 时尚型 80.48万, GLE450 4MATIC 豪华型 88.28万)
    ('<div class="car-name">GLE</div>', '<div class="car-name">GLE GLE350 / GLE450 4MATIC 时尚/豪华</div>'),
    # X5 (宝马X5: xDrive30Li M运动套装 60.50万, xDrive40Li M运动套装 72.50万, xDrive40Li 尊享型M运动 80.50万)
    ('<div class="car-name">X5</div>', '<div class="car-name">X5 xDrive30Li / xDrive40Li M运动</div>'),
    # Q7 (奥迪Q7: 45 TFSI quattro S line运动型 58.98万, 45 TFSI quattro S line尊贵型 65.58万, 55 TFSI quattro S line尊贵型 73.68万, 55 TFSI quattro S line运动型 80.58万)
    ('<div class="car-name">Q7</div>', '<div class="car-name">Q7 45 TFSI / 55 TFSI quattro S line</div>'),

    # GLS (奔驰GLS: GLS450 4MATIC 时尚型 109.38万, GLS450 4MATIC 动感型 114.58万, GLS450 4MATIC 豪华型 128.88万)
    ('<div class="car-name">GLS</div>', '<div class="car-name">GLS GLS450 4MATIC 时尚/动感/豪华</div>'),
    # X7 (宝马X7: xDrive40Li 领先型豪华套装 103.90万, xDrive40Li 尊享型M运动套装 118.90万, xDrive40Li 行政型M运动套装 136.90万)
    ('<div class="car-name">X7</div>', '<div class="car-name">X7 xDrive40Li 领先/尊享/行政 M运动</div>'),

    # G级 (奔驰G级: G350 142.48万, G500 186.80万, G580 首发特别版 217.00万)
    ('<div class="car-name">G级（大G）</div>', '<div class="car-name">G级 G350 / G500 / G580 首发特别版</div>'),

    # === 轿跑SUV ===
    # X2 (宝马X2: sDrive25i M运动套装 28.89万, sDrive25i M运动曜夜套装 30.99万)
    ('<div class="car-name">X2</div>', '<div class="car-name">X2 sDrive25i M运动/曜夜</div>'),
    # Q3 Sportback (奥迪: 40 TFSI 时尚型 29.28万, 40 TFSI 豪华型 31.68万, 45 TFSI quattro 时尚型 33.88万)
    ('<div class="car-name">Q3 Sportback</div>', '<div class="car-name">Q3 Sportback 40/45 TFSI quattro</div>'),

    # GLC Coupe (奔驰GLC Coupe: GLC260 4MATIC 轿跑SUV 47.20万, GLC300 4MATIC 轿跑SUV 55.60万)
    ('<div class="car-name">GLC Coupe</div>', '<div class="car-name">GLC Coupe GLC260 / GLC300 4MATIC</div>'),
    # X4 (宝马X4: xDrive25i M运动套装 45.59万, xDrive30i M运动曜夜套装 55.08万)
    ('<div class="car-name">X4</div>', '<div class="car-name">X4 xDrive25i / xDrive30i M运动曜夜</div>'),

    # GLE Coupe (奔驰GLE Coupe: GLE350 4MATIC 轿跑SUV 80.48万, GLE450 4MATIC 轿跑SUV 92.38万)
    ('<div class="car-name">GLE Coupe</div>', '<div class="car-name">GLE Coupe GLE350 / GLE450 4MATIC</div>'),
    # X6 (宝马X6: xDrive30i M运动套装 78.69万, xDrive40i M运动套装 89.69万, xDrive40i 尊享型M运动套装 102.69万)
    ('<div class="car-name">X6</div>', '<div class="car-name">X6 xDrive30i / xDrive40i M运动/尊享</div>'),
    # Q8 (奥迪Q8: 45 TFSI quattro 豪华动感型 76.38万, 45 TFSI quattro 臻选动感型 82.68万, 55 TFSI quattro 尊享动感型 103.68万)
    ('<div class="car-name">Q8</div>', '<div class="car-name">Q8 45 TFSI / 55 TFSI quattro 豪华/臻选</div>'),

    # === 纯电系列 ===
    # EQA (奔驰EQA: EQA 260 32.20万, 续航619km)
    ('<div class="car-name">EQA</div>', '<div class="car-name">EQA 260 续航619km</div>'),
    # iX1 (宝马iX1: eDrive25L X设计套装 29.99万, eDrive25L M运动套装 29.99万, xDrive30L M运动套装 33.99万)
    ('<div class="car-name">iX1</div>', '<div class="car-name">iX1 eDrive25L / xDrive30L M运动</div>'),
    # Q4 e-tron (奥迪Q4 e-tron: 40 e-tron 创境版 28.99万, 40 e-tron 创享版 31.99万, 50 e-tron quattro 创境版 33.99万)
    ('<div class="car-name">Q4 e-tron</div>', '<div class="car-name">Q4 e-tron 40/50 e-tron quattro</div>'),

    # EQB (奔驰EQB: EQB260 35.20万, EQB350 4MATIC 42.80万)
    ('<div class="car-name">EQB</div>', '<div class="car-name">EQB EQB260 / EQB350 4MATIC</div>'),
    # iX3 (宝马iX3: eDrive 35L 27.80万, eDrive 40L 领先型 39.99万, eDrive 40L 卓越型 44.99万, 续航540km)
    ('<div class="car-name">iX3</div>', '<div class="car-name">iX3 eDrive35L / eDrive40L 续航540km</div>'),
    # Q6L e-tron (奥迪Q6L e-tron: 基于PPE平台, 800V, 2025新品)
    ('<div class="car-name">Q6L e-tron</div>', '<div class="car-name">Q6L e-tron PPE平台 800V</div>'),

    # EQE SUV (奔驰EQE SUV: EQE 500 4MATIC 先锋版 48.60万, EQE 500 4MATIC 豪华版 51.60万, EQE 500 4MATIC 旗舰版 63.10万)
    ('<div class="car-name">EQE SUV</div>', '<div class="car-name">EQE SUV 500 4MATIC 先锋/豪华/旗舰</div>'),
    # iX (宝马iX: xDrive40 74.69万, xDrive50 86.89万, M60 100.99万)
    ('<div class="car-name">iX</div>', '<div class="car-name">iX xDrive40 / xDrive50 / M60</div>'),

    # EQS SUV (奔驰EQS SUV: EQS 500 4MATIC 91.05万, 续航777km)
    ('<div class="car-name">EQS SUV</div>', '<div class="car-name">EQS SUV 500 4MATIC 续航777km</div>'),

    # i3 (宝马i3: eDrive35L 17.69-17.70万, eDrive40L 曜夜 19.19-19.80万, eDrive40L 曜夜运动 20.69-21.60万, 续航550km)
    ('<div class="car-name">i3</div>', '<div class="car-name">i3 eDrive35L / 40L 曜夜/运动 续航550km</div>'),

    # EQE (奔驰EQE: EQE 500 4MATIC 先锋版 47.80万, 豪华版 49.60万, 旗舰版 62.70万, 续航681km)
    ('<div class="car-name">EQE</div>', '<div class="car-name">EQE 500 4MATIC 先锋/豪华/旗舰 续航681km</div>'),
    # i4 (宝马i4: eDrive35 44.99万, eDrive40 51.99万, M50 62.99万, 续航570km)
    ('<div class="car-name">i4</div>', '<div class="car-name">i4 eDrive35 / eDrive40 / M50 续航570km</div>'),
    # A6 e-tron (奥迪A6 e-tron: PPE平台 800V, 续航700+km)
    ('<div class="car-name">A6 e-tron</div>', '<div class="car-name">A6 e-tron PPE 800V 续航700+km</div>'),

    # EQS (奔驰EQS: EQS 500 4MATIC 88.10万, 续航840km)
    ('<div class="car-name">EQS</div>', '<div class="car-name">EQS 500 4MATIC 续航840km</div>'),
    # i7 (宝马i7: eDrive50L 领先型 94.90万, xDrive60L 豪华型 145.90万, M70 xDrive 199.90万, 续航625km)
    ('<div class="car-name">i7</div>', '<div class="car-name">i7 eDrive50L / xDrive60L / M70 续航625km</div>'),
    # e-tron GT (奥迪e-tron GT: J1平台 800V, RS e-tron GT 124.78万, 续航495km)
    ('<div class="car-name">e-tron GT</div>', '<div class="car-name">e-tron GT J1平台 RS版 124.78万</div>'),
]

replaced = 0
for old_text, new_text in replacements:
    if old_text in html:
        html = html.replace(old_text, new_text)
        replaced += 1
    else:
        print(f"  WARNING: 未找到 '{old_text}'")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Updated {replaced} car names with configuration details")
