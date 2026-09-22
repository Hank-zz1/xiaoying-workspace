---
name: office-pdf-tool
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, rendering pages to images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
author: 刘博
---

# PDF 技能

用于可靠地读取、分析、转换、编辑和生成 PDF。优先使用可验证、可复现的脚本或成熟库；涉及表单填写时必须阅读 [forms.md](forms.md)。

## 工作原则

1. 先确认 PDF 类型：文本型、扫描图像型、可填写 AcroForm、非可填写表单、加密/损坏文件。
2. 尽量保留原 PDF 结构：拆分、合并、旋转、加密等优先用 `pypdf` 或 `qpdf`；需要视觉落字时再用覆盖层。
3. 对用户可见的输出必须验证：至少检查页数/文件存在；表单和视觉改动要渲染成图片抽查位置；复杂操作建议再跑 `qpdf --check`。
4. 不要把扫描件当成文本 PDF。若抽取文本为空或乱码，先渲染页面并考虑 OCR。
5. 写脚本时使用结构化库处理 PDF，不要用字符串直接改 PDF 二进制内容。

## 常用任务选择

| 任务 | 首选工具 | 说明 |
| --- | --- | --- |
| 查看页数/元数据 | `pypdf.PdfReader` | 快速、依赖少 |
| 合并/拆分/旋转页面 | `pypdf` 或 `qpdf` | 大文件优先 `qpdf` |
| 抽取普通文本 | `pdftotext -layout` 或 `pdfplumber` | 表格/坐标需要 `pdfplumber` |
| 抽取表格 | `pdfplumber` | 必须人工检查表头和跨页结果 |
| 渲染页面图片 | `scripts/convert_pdf_to_images.py` | 自动创建输出目录，可限制页码 |
| 创建新 PDF | `reportlab` | 正文/表格用 Platypus，简单标注用 canvas |
| 填写可填写表单 | `scripts/fill_fillable_fields.py` | 先抽字段并校验枚举值 |
| 填写非可填写表单 | `scripts/fill_pdf_form_with_annotations.py` | 实际绘制文字覆盖层，比 FreeText 注释更稳定 |
| 加密/解密/修复 | `qpdf` | 命令行工具更稳 |
| OCR 扫描件 | `ocrmypdf` 或 `pytesseract` | 先确认语言包和分辨率 |

## 随附脚本

从本技能目录运行：

```bash
python scripts/convert_pdf_to_images.py input.pdf pages --dpi 200 --max-dim 2000
python scripts/check_fillable_fields.py input.pdf
python scripts/extract_form_field_info.py input.pdf field_info.json
python scripts/fill_fillable_fields.py input.pdf field_values.json output.pdf
python scripts/extract_form_structure.py input.pdf form_structure.json
python scripts/check_bounding_boxes.py fields.json
python scripts/create_validation_image.py 1 fields.json pages/page_1.png validation_page_1.png
python scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

脚本会对路径、JSON、页码、表单枚举值和坐标盒做基本校验；缺依赖时会给出安装提示。

## 表单填写

只要任务涉及“填写 PDF 表格/申请表/表单”，先读 [forms.md](forms.md)。核心流程：

1. `python scripts/check_fillable_fields.py input.pdf`
2. 如果有 AcroForm 字段：抽取字段 JSON，按字段 ID 准备值，再用 `fill_fillable_fields.py` 写入。
3. 如果没有 AcroForm 字段：抽取结构或渲染页面，准备 `fields.json`，先跑 `check_bounding_boxes.py`，再用覆盖层脚本写入。
4. 最后把输出 PDF 渲染为图片，检查文字是否落在正确位置。

## 可靠性检查

输出 PDF 后至少做其中几项；`qpdf` 未安装时跳过对应检查，改用 `pypdf` 页数/可读性检查和渲染抽查：

```bash
python scripts/convert_pdf_to_images.py output.pdf verify_pages --first-page 1 --last-page 1
qpdf --check output.pdf
python - < None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def handle_cli_error(exc: Exception) -> None:
    if isinstance(exc, PdfSkillError):
        exit_with_error(str(exc))
    raise exc


def input_path(path: str | Path, suffix: Optional[str] = None) -> Path:
    resolved = Path(path).expanduser()
    if not resolved.exists():
        raise PdfSkillError(f"Input file does not exist: {resolved}")
    if not resolved.is_file():
        raise PdfSkillError(f"Input path is not a file: {resolved}")
    if suffix and resolved.suffix.lower() != suffix.lower():
        raise PdfSkillError(f"Expected a {suffix} file, got: {resolved}")
    return resolved


def output_path(path: str | Path) -> Path:
    resolved = Path(path).expanduser()
    if resolved.parent and not resolved.parent.exists():
        resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def ensure_output_dir(path: str | Path) -> Path:
    resolved = Path(path).expanduser()
    resolved.mkdir(parents=True, exist_ok=True)
    if not resolved.is_dir():
        raise PdfSkillError(f"Output path is not a directory: {resolved}")
    return resolved


def load_json(path: str | Path) -> Any:
    resolved = input_path(path)
    try:
        with resolved.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except json.JSONDecodeError as exc:
        raise PdfSkillError(f"Invalid JSON in {resolved}: {exc}") from exc


def write_json(path: str | Path, data: Any) -> None:
    resolved = output_path(path)
    with resolved.open("w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def dereference(obj: Any) -> Any:
    if hasattr(obj, "get_object"):
        try:
            return obj.get_object()
        except Exception:
            return obj
    return obj


def pdf_name(value: Any) -> Optional[str]:
    value = dereference(value)
    if value is None:
        return None
    return str(value)


def json_safe(value: Any) -> Any:
    value = dereference(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if hasattr(value, "as_numeric"):
        try:
            return float(value)
        except Exception:
            return str(value)
    return str(value)


def rect_to_floats(rect: Any) -> list[float]:
    rect = dereference(rect)
    if rect is None or len(rect) != 4:
        raise PdfSkillError(f"Invalid rectangle: {rect}")
    try:
        return [round(float(dereference(item)), 3) for item in rect]
    except (TypeError, ValueError) as exc:
        raise PdfSkillError(f"Rectangle contains non-numeric values: {rect}") from exc


def normalize_rect(rect: Iterable[Any]) -> list[float]:
    values = [float(item) for item in rect]
    if len(values) != 4:
        raise PdfSkillError(f"Expected 4 rectangle values, got {len(values)}")
    left, top_or_bottom, right, bottom_or_top = values
    x0 = min(left, right)
    x1 = max(left, right)
    y0 = min(top_or_bottom, bottom_or_top)
    y1 = max(top_or_bottom, bottom_or_top)
    return [x0, y0, x1, y1]


def rect_area(rect: Iterable[Any]) -> float:
    x0, y0, x1, y1 = normalize_rect(rect)
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)


def rects_intersect(r1: Iterable[Any], r2: Iterable[Any]) -> bool:
    a = normalize_rect(r1)
    b = normalize_rect(r2)
    disjoint_horizontal = a[0] >= b[2] or a[2] = b[3] or a[3]  Optional[str]:
    components: list[str] = []
    seen: set[str] = set()
    current = annotation
    while current is not None:
        current = dereference(current)
        marker = repr(current)
        if marker in seen:
            break
        seen.add(marker)
        field_name = current.get("/T") if hasattr(current, "get") else None
        if field_name:
            components.append(str(field_name))
        current = current.get("/Parent") if hasattr(current, "get") else None
    return ".".join(reversed(components)) if components else None


def appearance_on_values(annotation: Any) -> list[str]:
    annotation = dereference(annotation)
    ap = dereference(annotation.get("/AP")) if hasattr(annotation, "get") else None
    normal = dereference(ap.get("/N")) if hasattr(ap, "get") else None
    if not hasattr(normal, "keys"):
        return []
    values = [str(key) for key in normal.keys()]
    return [value for value in values if value != "/Off"]


def field_states(field: Any) -> list[str]:
    field = dereference(field)
    states = field.get("/_States_", []) if hasattr(field, "get") else []
    result: list[str] = []
    for state in states:
        if isinstance(state, (list, tuple)) and state:
            result.append(str(json_safe(state[0])))
        else:
            result.append(str(json_safe(state)))
    return result


def choice_options(field: Any) -> list[dict[str, str]]:
    field = dereference(field)
    if hasattr(field, "get"):
        raw_options = field.get("/Opt") or field.get("/_States_", [])
    else:
        raw_options = []
    options: list[dict[str, str]] = []
    for option in raw_options:
        option = json_safe(option)
        if isinstance(option, list) and len(option) >= 2:
            options.append({"value": str(option[0]), "text": str(option[1])})
        else:
            options.append({"value": str(option), "text": str(option)})
    return options


def make_field_dict(field: Any, field_id: str) -> dict[str, Any]:
    field = dereference(field)
    field_dict: dict[str, Any] = {"field_id": field_id}
    field_type = pdf_name(field.get("/FT")) if hasattr(field, "get") else None

    if field_type == "/Tx":
        field_dict["type"] = "text"
        max_length = field.get("/MaxLen")
        if max_length is not None:
            field_dict["max_length"] = int(max_length)
    elif field_type == "/Btn":
        field_dict["type"] = "checkbox"
        states = field_states(field)
        checked_values = [state for state in states if state != "/Off"]
        if checked_values:
            field_dict["checked_value"] = checked_values[0]
            field_dict["unchecked_value"] = "/Off" if "/Off" in states else states[-1]
        else:
            field_dict["checked_value"] = "/Yes"
            field_dict["unchecked_value"] = "/Off"
    elif field_type == "/Ch":
        field_dict["type"] = "choice"
        field_dict["choice_options"] = choice_options(field)
    elif field_type == "/Sig":
        field_dict["type"] = "signature"
    else:
        field_dict["type"] = f"unknown ({field_type})"

    existing_value = field.get("/V") if hasattr(field, "get") else None
    if existing_value is not None:
        field_dict["current_value"] = json_safe(existing_value)
    return field_dict


def extract_acroform_field_info(reader: Any) -> tuple[list[dict[str, Any]], list[str]]:
    fields = reader.get_fields() or {}
    warnings: list[str] = []
    field_info_by_id: dict[str, dict[str, Any]] = {}
    possible_radio_names: set[str] = set()

    for field_id, field in fields.items():
        field = dereference(field)
        if field.get("/Kids") and pdf_name(field.get("/FT")) == "/Btn":
            possible_radio_names.add(field_id)
            continue
        field_info_by_id[field_id] = make_field_dict(field, field_id)

    radio_fields_by_id: dict[str, dict[str, Any]] = {}

    for page_index, page in enumerate(reader.pages):
        annotations = page.get("/Annots", []) or []
        for raw_annotation in annotations:
            annotation = dereference(raw_annotation)
            field_id = get_full_annotation_field_id(annotation)
            if not field_id:
                continue
            rect = annotation.get("/Rect") if hasattr(annotation, "get") else None

            if field_id in field_info_by_id:
                field = field_info_by_id[field_id]
                field["page"] = page_index + 1
                if rect is not None:
                    field["rect"] = rect_to_floats(rect)
                if field["type"] == "checkbox":
                    on_values = appearance_on_values(annotation)
                    if on_values:
                        field["checked_value"] = on_values[0]
                        field["unchecked_value"] = "/Off"
                continue

            if field_id in possible_radio_names:
                on_values = appearance_on_values(annotation)
                if not on_values:
                    continue
                if field_id not in radio_fields_by_id:
                    radio_fields_by_id[field_id] = {
                        "field_id": field_id,
                        "type": "radio_group",
                        "page": page_index + 1,
                        "radio_options": [],
                    }
                option: dict[str, Any] = {"value": on_values[0]}
                if rect is not None:
                    option["rect"] = rect_to_floats(rect)
                radio_fields_by_id[field_id]["radio_options"].append(option)

    fields_with_location: list[dict[str, Any]] = []
    for field in field_info_by_id.values():
        if "page" in field:
            fields_with_location.append(field)
        else:
            warnings.append(f"Unable to determine location for field id '{field.get('field_id')}', ignored.")

    def sort_key(field: dict[str, Any]) -> tuple[int, float, float]:
        if field.get("radio_options"):
            rect = field["radio_options"][0].get("rect", [0, 0, 0, 0])
        else:
            rect = field.get("rect", [0, 0, 0, 0])
        return (int(field.get("page") or 0), -float(rect[1]), float(rect[0]))

    result = fields_with_location + list(radio_fields_by_id.values())
    result.sort(key=sort_key)
    return result, warnings


def get_field_info(reader: Any) -> list[dict[str, Any]]:
    return extract_acroform_field_info(reader)[0]


def validate_fillable_value(field_info: dict[str, Any], field_value: Any) -> Optional[str]:
    field_type = field_info.get("type")
    field_id = field_info.get("field_id")
    value = str(field_value)

    if field_type == "checkbox":
        checked_val = str(field_info.get("checked_value", "/Yes"))
        unchecked_val = str(field_info.get("unchecked_value", "/Off"))
        if value not in {checked_val, unchecked_val}:
            return (
                f"Invalid value '{value}' for checkbox field '{field_id}'. "
                f"Use '{checked_val}' to check it or '{unchecked_val}' to uncheck it."
            )
    elif field_type == "radio_group":
        option_values = [str(opt["value"]) for opt in field_info.get("radio_options", [])]
        if value not in option_values:
            return f"Invalid value '{value}' for radio group field '{field_id}'. Valid values: {option_values}"
    elif field_type == "choice":
        option_values = [str(opt["value"]) for opt in field_info.get("choice_options", [])]
        if option_values and value not in option_values:
            return f"Invalid value '{value}' for choice field '{field_id}'. Valid values: {option_values}"
    elif field_type == "signature":
        return f"Signature field '{field_id}' cannot be filled by this script."
    return None


def page_info_by_number(fields_data: dict[str, Any]) -> dict[int, dict[str, Any]]:
    pages = fields_data.get("pages")
    if not isinstance(pages, list):
        raise PdfSkillError("fields.json must contain a 'pages' list.")
    result: dict[int, dict[str, Any]] = {}
    for page in pages:
        if not isinstance(page, dict) or "page_number" not in page:
            raise PdfSkillError("Each page entry must be an object with 'page_number'.")
        result[int(page["page_number"])] = page
    return result


def coordinate_mode(page_info: dict[str, Any]) -> str:
    if "pdf_width" in page_info and "pdf_height" in page_info:
        return "pdf_top_left"
    if "image_width" in page_info and "image_height" in page_info:
        return "image_top_left"
    raise PdfSkillError(
        "Each page must define either pdf_width/pdf_height or image_width/image_height."
    )


def to_pdf_rect(
    bbox: Iterable[Any],
    page_info: dict[str, Any],
    actual_pdf_width: float,
    actual_pdf_height: float,
) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = normalize_rect(bbox)
    mode = coordinate_mode(page_info)
    if mode == "pdf_top_left":
        declared_width = float(page_info["pdf_width"])
        declared_height = float(page_info["pdf_height"])
        x_scale = actual_pdf_width / declared_width if declared_width else 1.0
        y_scale = actual_pdf_height / declared_height if declared_height else 1.0
    else:
        declared_width = float(page_info["image_width"])
        declared_height = float(page_info["image_height"])
        x_scale = actual_pdf_width / declared_width
        y_scale = actual_pdf_height / declared_height

    left = x0 * x_scale
    right = x1 * x_scale
    top = actual_pdf_height - (y0 * y_scale)
    bottom = actual_pdf_height - (y1 * y_scale)
    return left, bottom, right, top


def to_image_rect(
    bbox: Iterable[Any],
    page_info: dict[str, Any],
    actual_image_width: float,
    actual_image_height: float,
) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = normalize_rect(bbox)
    mode = coordinate_mode(page_info)
    if mode == "image_top_left":
        declared_width = float(page_info["image_width"])
        declared_height = float(page_info["image_height"])
        x_scale = actual_image_width / declared_width
        y_scale = actual_image_height / declared_height
        return x0 * x_scale, y0 * y_scale, x1 * x_scale, y1 * y_scale

    declared_width = float(page_info["pdf_width"])
    declared_height = float(page_info["pdf_height"])
    x_scale = actual_image_width / declared_width
    y_scale = actual_image_height / declared_height
    return x0 * x_scale, y0 * y_scale, x1 * x_scale, y1 * y_scale


def parse_hex_color(value: str) -> tuple[float, float, float]:
    color = value.strip().lstrip("#")
    if len(color) == 3:
        color = "".join(ch * 2 for ch in color)
    if len(color) != 6:
        raise PdfSkillError(f"Invalid hex color: {value}")
    try:
        r = int(color[0:2], 16) / 255.0
        g = int(color[2:4], 16) / 255.0
        b = int(color[4:6], 16) / 255.0
    except ValueError as exc:
        raise PdfSkillError(f"Invalid hex color: {value}") from exc
    return r, g, b


def string_width(text: str, font_name: str, font_size: float) -> float:
    pdfmetrics = import_required("reportlab.pdfbase.pdfmetrics", "reportlab")
    try:
        return float(pdfmetrics.stringWidth(text, font_name, font_size))
    except Exception:
        return float(len(text) * font_size * 0.55)


def split_long_token(token: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    pieces: list[str] = []
    current = ""
    for char in token:
        candidate = current + char
        if current and string_width(candidate, font_name, font_size) > max_width:
            pieces.append(current)
            current = char
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces or [token]


def wrap_text(text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    if max_width = min_size:
        lines = wrap_text(text, font_name, size, max_width)
        line_height = size * 1.2
        if lines and len(lines) * line_height  dict[str, Any]:
    import json

    try:
        data = json.load(fields_json_stream)
    except json.JSONDecodeError as exc:
        raise PdfSkillError(f"Invalid JSON: {exc}") from exc
    return _validate_schema(data)


def _validate_schema(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise PdfSkillError("fields.json must be a JSON object.")
    if not isinstance(data.get("form_fields"), list):
        raise PdfSkillError("fields.json must contain a 'form_fields' list.")
    if not isinstance(data.get("pages"), list):
        raise PdfSkillError("fields.json must contain a 'pages' list.")
    return data


def _field_rects(field: dict[str, Any]) -> list[RectAndField]:
    rects: list[RectAndField] = []
    if "label_bounding_box" in field:
        rects.append(RectAndField(normalize_rect(field["label_bounding_box"]), "label", field))
    if "entry_bounding_box" in field:
        rects.append(RectAndField(normalize_rect(field["entry_bounding_box"]), "entry", field))
    else:
        raise PdfSkillError(f"Field '{field.get('description', '')}' is missing entry_bounding_box.")
    return rects


def _text_fit_messages(field: dict[str, Any], entry_rect: list[float]) -> list[str]:
    entry_text = field.get("entry_text")
    if not isinstance(entry_text, dict) or "text" not in entry_text:
        return []

    messages: list[str] = []
    text = str(entry_text.get("text", ""))
    font_name = str(entry_text.get("font", "Helvetica"))
    font_size = float(entry_text.get("font_size", 12))
    padding = float(entry_text.get("padding", 1.5))
    width = max(0.0, entry_rect[2] - entry_rect[0] - padding * 2)
    height = max(0.0, entry_rect[3] - entry_rect[1] - padding * 2)

    if height  height:
        messages.append(
            "WARNING: text for '%s' may not fit after wrapping (%d lines, %.1fpt height available)."
            % (field.get("description", ""), len(lines), height)
        )
    elif any(string_width(line, font_name, font_size) > width + 0.5 for line in lines):
        messages.append(
            "WARNING: text for '%s' may be wider than the entry box."
            % field.get("description", "")
        )
    return messages


def get_bounding_box_messages(fields_json_stream: TextIO) -> list[str]:
    data = _load_fields_from_stream(fields_json_stream)
    fields = data["form_fields"]
    messages = [f"Read {len(fields)} fields"]

    rects_and_fields: list[RectAndField] = []
    has_failure = False
    for field_index, field in enumerate(fields):
        if not isinstance(field, dict):
            raise PdfSkillError(f"form_fields[{field_index}] must be an object.")
        if "page_number" not in field:
            raise PdfSkillError(f"form_fields[{field_index}] is missing page_number.")
        for rect_info in _field_rects(field):
            if any(not finite_number(value) for value in rect_info.rect):
                raise PdfSkillError(f"Invalid non-finite coordinate in {rect_info.rect}.")
            if rect_area(rect_info.rect) = 30:
                messages.append("Aborting further checks; fix bounding boxes and try again.")
                return messages

    if not has_failure:
        messages.append("SUCCESS: All bounding boxes are structurally valid")
    return messages


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate non-fillable PDF field bounding boxes.")
    parser.add_argument("fields_json", help="fields.json path")
    args = parser.parse_args()

    try:
        data = load_json(args.fields_json)
        _validate_schema(data)
        with open(args.fields_json, "r", encoding="utf-8") as stream:
            messages = get_bounding_box_messages(stream)
        for message in messages:
            print(message)
        if any(message.startswith("FAILURE") for message in messages):
            raise SystemExit(1)
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
