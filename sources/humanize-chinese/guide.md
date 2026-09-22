# Humanize Chinese

中文 AI 文本检测与去痕工具。纯 Python 标准库实现，零依赖，本地运行。支持 20+ 维度检测、智能改写、学术论文 AIGC 降重、7 种风格转换。

## Scope

- 检测中文文本的 AI 生成痕迹（0-100 评分）
- 改写文本去除 AI 味道（句式重组、词汇替换、段落结构调整）
- 学术论文 AIGC 降重（适配知网/维普/万方）
- 风格转换（口语化/知乎/小红书/公众号/学术/文艺/微博）
- 所有操作本地完成，无需联网

## Guidelines

- 所有脚本在 `scripts/` 目录下，纯 Python 标准库，无需安装依赖
- 使用 `python` 运行脚本（Windows 上可能是 `python` 或 `python3`）
- 检测和改写支持中文文本，文件需为 UTF-8 编码
- 评分标准：0-24 LOW / 25-49 MEDIUM / 50-74 HIGH / 75-100 VERY HIGH
- 改写后建议通读确认专业术语未被误改

## CLI 工具

### 检测 AI 痕迹
```bash
python scripts/detect_cn.py text.txt        # 基础检测
python scripts/detect_cn.py text.txt -v     # 详细模式 + 最可疑句子
python scripts/detect_cn.py text.txt -s     # 仅评分
python scripts/detect_cn.py text.txt -j     # JSON 输出
```

### 通用改写
```bash
python scripts/humanize_cn.py text.txt -o clean.txt
python scripts/humanize_cn.py text.txt --scene social -a   # 社交场景 + 激进
python scripts/humanize_cn.py text.txt --style xiaohongshu # 改写 + 风格转换
```

### 学术论文降 AIGC
```bash
python scripts/academic_cn.py paper.txt -o clean.txt --compare
python scripts/academic_cn.py paper.txt -o clean.txt -a --compare  # 激进模式
```

### 风格转换
```bash
python scripts/style_cn.py text.txt --style zhihu -o out.txt
# 支持: casual / zhihu / xiaohongshu / wechat / academic / literary / weibo
```

### 前后对比
```bash
python scripts/compare_cn.py text.txt --scene tech -a
```

### 参数速查
| 参数 | 说明 |
|------|------|
| `-v` | 详细模式，显示可疑句子 |
| `-s` | 仅评分 |
| `-j` | JSON 输出 |
| `-o` | 输出文件 |
| `-a` | 激进模式 |
| `--seed N` | 固定随机种子 |
| `--scene` | general / social / tech / formal / chat |
| `--style` | casual / zhihu / xiaohongshu / wechat / academic / literary / weibo |
| `--compare` | 前后对比 |