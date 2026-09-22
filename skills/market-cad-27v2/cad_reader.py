#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CAD 文件读取工具 - DWG 文件读取和导出
支持 AutoCAD 原生 DWG 格式文件的读取、信息提取和格式转换
"""

import sys
import json
import os
from pathlib import Path


def check_dependencies():
    """检查并安装所需依赖"""
    missing = []
    try:
        import pyautocad
    except ImportError:
        missing.append('pyautocad')
    try:
        import ezdxf
    except ImportError:
        missing.append('ezdxf')

    if missing:
        print(f"缺少依赖库：{', '.join(missing)}")
        print(f"请运行：pip install {' '.join(missing)}")
        return False
    return True


def get_file_info(dwg_path):
    """获取 DWG 文件基本信息"""
    from pyautocad import Autocad

    acad = Autocad(create_if_not_exists=False)
    if not acad:
        return {"error": "无法连接到 AutoCAD，请确保已安装并运行"}

    try:
        doc = acad.app.Documents.Open(dwg_path, False, True)  # 只读打开
        info = {
            "path": dwg_path,
            "name": doc.Name,
            "size_bytes": os.path.getsize(dwg_path),
            "layers_count": len(doc.Layers),
            "entities_count": doc.ModelSpace.Count,
            "units": str(doc.ActiveSpace),
        }
        doc.Close(False)
        return info
    except Exception as e:
        return {"error": str(e)}


def extract_layers(dwg_path):
    """提取所有图层信息"""
    from pyautocad import Autocad

    acad = Autocad(create_if_not_exists=False)
    if not acad:
        return {"error": "无法连接到 AutoCAD"}

    try:
        doc = acad.app.Documents.Open(dwg_path, False, True)
        layers = []
        for layer in doc.Layers:
            layers.append({
                "name": layer.Name,
                "color": layer.Color,
                "linetype": layer.Linetype,
                "linewidth": layer.Lineweight,
                "frozen": layer.Freeze,
                "locked": layer.Lock,
                "visible": layer.On,
            })
        doc.Close(False)
        return {"layers": layers, "count": len(layers)}
    except Exception as e:
        return {"error": str(e)}


def extract_entities(dwg_path, layer_filter=None, limit=1000):
    """提取几何图形实体"""
    from pyautocad import Autocad

    acad = Autocad(create_if_not_exists=False)
    if not acad:
        return {"error": "无法连接到 AutoCAD"}

    try:
        doc = acad.app.Documents.Open(dwg_path, False, True)
        entities = []
        count = 0

        for entity in doc.ModelSpace:
            if limit and count >= limit:
                break

            if layer_filter and entity.Layer != layer_filter:
                continue

            entity_data = {
                "type": entity.ObjectName.replace('AcDb', ''),
                "layer": entity.Layer,
                "handle": entity.Handle,
            }

            # 根据类型提取特定属性
            try:
                if entity.ObjectName == 'AcDbLine':
                    entity_data.update({
                        "start": [entity.StartPoint.x, entity.StartPoint.y, entity.StartPoint.z],
                        "end": [entity.EndPoint.x, entity.EndPoint.y, entity.EndPoint.z],
                        "length": entity.Length,
                    })
                elif entity.ObjectName == 'AcDbCircle':
                    entity_data.update({
                        "center": [entity.Center.x, entity.Center.y, entity.Center.z],
                        "radius": entity.Radius,
                    })
                elif entity.ObjectName == 'AcDbArc':
                    entity_data.update({
                        "center": [entity.Center.x, entity.Center.y, entity.Center.z],
                        "radius": entity.Radius,
                        "start_angle": entity.StartAngle,
                        "end_angle": entity.EndAngle,
                    })
                elif entity.ObjectName == 'AcDbPolyline':
                    points = []
                    for i in range(entity.Coordinates.Count):
                        points.append(entity.Coordinates.Item(i))
                    entity_data["coordinates"] = points
                elif entity.ObjectName == 'AcDbBlockReference':
                    entity_data.update({
                        "block_name": entity.EffectiveName,
                        "position": [entity.InsertionPoint.x, entity.InsertionPoint.y, entity.InsertionPoint.z],
                    })
            except Exception:
                entity_data["note"] = "部分属性读取失败"

            entities.append(entity_data)
            count += 1

        doc.Close(False)
        return {"entities": entities, "count": len(entities), "limit_reached": count >= limit}
    except Exception as e:
        return {"error": str(e)}


def extract_texts(dwg_path):
    """提取文字和标注信息"""
    from pyautocad import Autocad

    acad = Autocad(create_if_not_exists=False)
    if not acad:
        return {"error": "无法连接到 AutoCAD"}

    try:
        doc = acad.app.Documents.Open(dwg_path, False, True)
        texts = []
        dimensions = []

        for entity in doc.ModelSpace:
            try:
                if entity.ObjectName == 'AcDbText' or entity.ObjectName == 'AcDbMText':
                    texts.append({
                        "type": "MText" if entity.ObjectName == 'AcDbMText' else "Text",
                        "content": entity.TextString,
                        "position": [entity.InsertionPoint.x, entity.InsertionPoint.y, entity.InsertionPoint.z],
                        "height": entity.Height if hasattr(entity, 'Height') else 0,
                        "layer": entity.Layer,
                        "rotation": entity.Rotation if hasattr(entity, 'Rotation') else 0,
                    })
                elif entity.ObjectName == 'AcDbDimension':
                    dimensions.append({
                        "type": entity.DimensionType,
                        "text": entity.TextOverride if entity.TextOverride else "(自动标注)",
                        "layer": entity.Layer,
                    })
            except Exception:
                continue

        doc.Close(False)
        return {
            "texts": texts,
            "dimensions": dimensions,
            "text_count": len(texts),
            "dimension_count": len(dimensions),
        }
    except Exception as e:
        return {"error": str(e)}


def export_to_dxf(dwg_path, output_path):
    """导出为 DXF 格式"""
    from pyautocad import Autocad

    acad = Autocad(create_if_not_exists=False)
    if not acad:
        return {"error": "无法连接到 AutoCAD"}

    try:
        doc = acad.app.Documents.Open(dwg_path, False, True)
        doc.SaveAs(output_path, 16)  # 16 = DXF 格式
        doc.Close(False)
        return {"success": True, "output": output_path}
    except Exception as e:
        return {"error": str(e)}


def main():
    import argparse

    parser = argparse.ArgumentParser(description='CAD 文件读取工具')
    parser.add_argument('file', help='DWG 文件路径')
    parser.add_argument('--info', action='store_true', help='显示文件基本信息')
    parser.add_argument('--layers', action='store_true', help='提取图层列表')
    parser.add_argument('--entities', action='store_true', help='提取几何图形')
    parser.add_argument('--text', action='store_true', help='提取文字和标注')
    parser.add_argument('--layer', type=str, help='指定图层名称过滤')
    parser.add_argument('--limit', type=int, default=1000, help='实体数量限制')
    parser.add_argument('--export-dxf', type=str, help='导出为 DXF 格式')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')

    args = parser.parse_args()

    if not check_dependencies():
        sys.exit(1)

    if not os.path.exists(args.file):
        print(json.dumps({"error": f"文件不存在：{args.file}"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = {}

    if args.info:
        result = get_file_info(args.file)
    elif args.layers:
        result = extract_layers(args.file)
    elif args.entities:
        result = extract_entities(args.file, args.layer, args.limit)
    elif args.text:
        result = extract_texts(args.file)
    elif args.export_dxf:
        output = args.output or args.export_dxf
        result = export_to_dxf(args.file, output)
    else:
        # 默认显示基本信息
        result = get_file_info(args.file)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
