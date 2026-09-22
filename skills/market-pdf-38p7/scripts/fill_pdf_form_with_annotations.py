from __future__ import annotations

import argparse
import io
from typing import Any

from _pdf_utils import (
    PdfSkillError,
    fit_font_size,
    handle_cli_error,
    import_required,
    input_path,
    load_json,
    output_path,
    page_info_by_number,
    parse_hex_color,
    string_width,
    to_pdf_rect,
    wrap_text,
)


def _fields_by_page(fields_data: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
    if not isinstance(fields_data.get("form_fields"), list):
        raise PdfSkillError("fields.json must contain a 'form_fields' list.")
    result: dict[int, list[dict[str, Any]]] = {}
    for index, field in enumerate(fields_data["form_fields"]):
        if not isinstance(field, dict):
            raise PdfSkillError(f"form_fields[{index}] must be an object.")
        if "page_number" not in field:
            raise PdfSkillError(f"form_fields[{index}] is missing page_number.")
        if "entry_bounding_box" not in field:
            raise PdfSkillError(f"form_fields[{index}] is missing entry_bounding_box.")
        result.setdefault(int(field["page_number"]), []).append(field)
    return result


def _set_font(canvas, font_name: str, font_size: float) -> str:
    try:
        canvas.setFont(font_name, font_size)
        return font_name
    except Exception:
        canvas.setFont("Helvetica", font_size)
        return "Helvetica"


def _draw_text(canvas, rect: tuple[float, float, float, float], entry_text: dict[str, Any]) -> None:
    left, bottom, right, top = rect
    width = max(0.0, right - left)
    height = max(0.0, top - bottom)
    text = str(entry_text.get("text", ""))
    if not text:
        return

    requested_font = str(entry_text.get("font", "Helvetica"))
    requested_size = float(entry_text.get("font_size", 12))
    padding = float(entry_text.get("padding", 1.5))
    align = str(entry_text.get("align", "left")).lower()
    color = parse_hex_color(str(entry_text.get("font_color", "000000")))
    max_width = max(1.0, width - padding * 2)
    max_height = max(1.0, height - padding * 2)

    font_name = _set_font(canvas, requested_font, requested_size)
    if entry_text.get("auto_fit", True):
        font_size, lines = fit_font_size(text, font_name, requested_size, max_width, max_height)
    else:
        font_size = requested_size
        lines = wrap_text(text, font_name, font_size, max_width)
    font_name = _set_font(canvas, font_name, font_size)
    line_height = float(entry_text.get("line_height", font_size * 1.2))

    canvas.setFillColorRGB(*color)
    y = top - padding - font_size
    for line in lines:
        if y  None:
    left, bottom, right, top = rect
    canvas.saveState()
    canvas.setStrokeColorRGB(1, 0, 0)
    canvas.setLineWidth(0.5)
    canvas.rect(left, bottom, right - left, top - bottom, stroke=1, fill=0)
    canvas.restoreState()


def _make_overlay_page(
    page_width: float,
    page_height: float,
    fields: list[dict[str, Any]],
    page_info: dict[str, Any],
    draw_boxes: bool,
) -> Any:
    reportlab_canvas = import_required("reportlab.pdfgen.canvas", "reportlab")
    packet = io.BytesIO()
    canvas = reportlab_canvas.Canvas(packet, pagesize=(page_width, page_height))

    for field in fields:
        rect = to_pdf_rect(field["entry_bounding_box"], page_info, page_width, page_height)
        if draw_boxes:
            _draw_debug_boxes(canvas, field, rect)
        entry_text = field.get("entry_text")
        if isinstance(entry_text, dict):
            _draw_text(canvas, rect, entry_text)

    canvas.save()
    packet.seek(0)
    return packet


def fill_pdf_form(input_pdf_path: str, fields_json_path: str, output_pdf_path: str, draw_boxes: bool = False) -> int:
    pypdf = import_required("pypdf")
    fields_data = load_json(fields_json_path)
    pages = page_info_by_number(fields_data)
    fields_for_page = _fields_by_page(fields_data)

    reader = pypdf.PdfReader(str(input_path(input_pdf_path, ".pdf")))
    writer = pypdf.PdfWriter()
    total_drawn = 0

    for page_index, page in enumerate(reader.pages, 1):
        if page_index not in fields_for_page:
            writer.add_page(page)
            continue
        if page_index not in pages:
            raise PdfSkillError(f"Page {page_index} has fields but no page metadata in fields.json.")

        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        overlay_stream = _make_overlay_page(
            page_width,
            page_height,
            fields_for_page[page_index],
            pages[page_index],
            draw_boxes,
        )
        overlay_reader = pypdf.PdfReader(overlay_stream)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)
        total_drawn += sum(
            1
            for field in fields_for_page[page_index]
            if isinstance(field.get("entry_text"), dict) and field["entry_text"].get("text")
        )

    target = output_path(output_pdf_path)
    with target.open("wb") as output:
        writer.write(output)

    print(f"Successfully filled PDF form and saved to {target}")
    print(f"Drew {total_drawn} text overlays")
    return total_drawn


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill a non-fillable PDF by drawing text overlays.")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("fields_json", help="Field coordinate JSON path")
    parser.add_argument("output_pdf", help="Output PDF path")
    parser.add_argument("--draw-boxes", action="store_true", help="Draw red boxes around entry areas")
    args = parser.parse_args()

    try:
        fill_pdf_form(args.input_pdf, args.fields_json, args.output_pdf, draw_boxes=args.draw_boxes)
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
