---
name: "CAD 文件读取"
description: "读取 AutoCAD DWG 文件，提取图层、几何图形、标注、文字等信息，支持转换为 DXF/PDF 格式"
icon: "cad.svg"
globs: ["*.dwg"]
---

# CAD 文件读取技能

## 功能说明

本技能用于读取 AutoCAD 原生 DWG 格式文件，提取其中的图形和文字信息。

### 核心功能

- **读取 DWG 文件** - 直接读取 AutoCAD 原生格式文件
- **提取图层信息** - 获取所有图层名称、颜色、线型等属性
- **提取几何图形** - 获取直线、圆、圆弧、多段线等图形数据
- **提取文字标注** - 获取图纸中的文字、尺寸标注、公差等信息
- **导出转换** - 支持导出为 DXF、PDF、SVG 等格式

## 使用方法

### 1. 读取 DWG 文件基本信息

```bash
python cad_reader.py --info 
```

输出包括：
- 文件大小、版本
- 图层数量
- 实体数量统计
- 图纸单位

### 2. 提取图层列表

```bash
python cad_reader.py --layers 
```

输出所有图层的详细信息（名称、颜色、线型、线宽等）。

### 3. 提取几何图形

```bash
python cad_reader.py --entities  [--layer ]
```

提取指定图层或全部图层的几何图形信息。

### 4. 提取文字和标注

```bash
python cad_reader.py --text 
```

提取图纸中的所有文字内容和尺寸标注。

### 5. 导出为其他格式

```bash
# 导出为 DXF
python cad_reader.py --export-dxf  --output 

# 导出为 PDF
python cad_reader.py --export-pdf  --output 

# 导出为 SVG
python cad_reader.py --export-svg  --output 
```

## 依赖安装

```bash
# 主要依赖
pip install pyautocad
pip install ezdxf

# 可选依赖（用于 PDF 导出）
pip install reportlab
```

### 系统要求

- **Windows**: 需要安装 AutoCAD（任何版本），因为 pyautocad 通过 COM 接口工作
- **Linux/Mac**: 使用 OdaFileConvert 将 DWG 转为 DXF 后用 ezdxf 读取

## 输出格式

所有提取的信息默认以 JSON 格式输出，便于其他程序处理：

```json
{
  "file_info": {
    "path": "xxx.dwg",
    "version": "AC1032",
    "size_bytes": 123456
  },
  "layers": [
    {"name": "0", "color": 7, "linetype": "Continuous"}
  ],
  "entities": [
    {"type": "LINE", "layer": "0", "start": [0, 0], "end": [100, 100]}
  ],
  "texts": [
    {"content": "尺寸标注", "position": [50, 50], "height": 2.5}
  ]
}
```

## 注意事项

1. **AutoCAD 依赖**: pyautocad 需要系统安装 AutoCAD 才能工作
2. **文件锁定**: 读取时确保 DWG 文件未被其他程序独占打开
3. **大文件处理**: 对于大型图纸，建议使用 --layer 参数指定特定图层
4. **编码问题**: 中文标注使用 UTF-8 编码输出

## 常见问题

**Q: 没有安装 AutoCAD 怎么办？**

A: 可以使用以下替代方案：
1. 安装 ODA File Converter 进行格式转换
2. 使用在线 DWG 查看器导出为 DXF
3. 请求图纸提供方直接提供 DXF 格式

**Q: 读取速度慢怎么办？**

A: 使用 `--layer` 参数限制只读取特定图层，或添加 `--limit N` 限制实体数量。
