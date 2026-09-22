from __future__ import annotations

import argparse

from _pdf_utils import (
    PdfSkillError,
    handle_cli_error,
    import_required,
    input_path,
    load_json,
    output_path,
    page_info_by_number,
    to_image_rect,
)


def create_validation_image(page_number: int, fields_json_path: str, input_path_arg: str, output_path_arg: str) -> int:
    pillow_image = import_required("PIL.Image", "Pillow")
    pillow_draw = import_required("PIL.ImageDraw", "Pillow")

    data = load_json(fields_json_path)
    pages = page_info_by_number(data)
    if page_number not in pages:
        raise PdfSkillError(f"Page {page_number} is not listed in fields.json.")

    image = pillow_image.open(input_path(input_path_arg))
    draw = pillow_draw.Draw(image)
    num_boxes = 0

    page_info = pages[page_number]
    image_width, image_height = image.size
    for field in data.get("form_fields", []):
        if int(field.get("page_number", -1)) != page_number:
            continue
        if "entry_bounding_box" in field:
            entry_box = to_image_rect(field["entry_bounding_box"], page_info, image_width, image_height)
            draw.rectangle(entry_box, outline="red", width=3)
            num_boxes += 1
        if "label_bounding_box" in field:
            label_box = to_image_rect(field["label_bounding_box"], page_info, image_width, image_height)
            draw.rectangle(label_box, outline="blue", width=2)
            num_boxes += 1

    target = output_path(output_path_arg)
    image.save(target)
    print(f"Created validation image at {target} with {num_boxes} bounding boxes")
    return num_boxes


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw field bounding boxes on a rendered page image.")
    parser.add_argument("page_number", type=int, help="1-based page number")
    parser.add_argument("fields_json", help="fields.json path")
    parser.add_argument("input_image", help="Rendered page image")
    parser.add_argument("output_image", help="Output validation image")
    args = parser.parse_args()

    try:
        create_validation_image(args.page_number, args.fields_json, args.input_image, args.output_image)
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
