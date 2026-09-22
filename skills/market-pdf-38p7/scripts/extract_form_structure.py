from __future__ import annotations

import argparse
from typing import Any

from _pdf_utils import handle_cli_error, import_required, input_path, write_json


def _empty_structure() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "coordinate_system": "top-left PDF points",
        "pages": [],
        "labels": [],
        "lines": [],
        "checkboxes": [],
        "row_boundaries": [],
        "warnings": [],
    }


def _extract_with_pdfplumber(pdf_path: str, x_tolerance: float, y_tolerance: float) -> dict[str, Any]:
    pdfplumber = import_required("pdfplumber")
    structure = _empty_structure()
    structure["engine"] = "pdfplumber"

    with pdfplumber.open(str(input_path(pdf_path, ".pdf"))) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            structure["pages"].append(
                {
                    "page_number": page_num,
                    "pdf_width": round(float(page.width), 3),
                    "pdf_height": round(float(page.height), 3),
                }
            )

            words = page.extract_words(x_tolerance=x_tolerance, y_tolerance=y_tolerance) or []
            for word in words:
                structure["labels"].append(
                    {
                        "page": page_num,
                        "text": word["text"],
                        "x0": round(float(word["x0"]), 1),
                        "top": round(float(word["top"]), 1),
                        "x1": round(float(word["x1"]), 1),
                        "bottom": round(float(word["bottom"]), 1),
                    }
                )

            for line in page.lines:
                width = abs(float(line["x1"]) - float(line["x0"]))
                if width > page.width * 0.35:
                    structure["lines"].append(
                        {
                            "page": page_num,
                            "y": round(float(line["top"]), 1),
                            "x0": round(float(line["x0"]), 1),
                            "x1": round(float(line["x1"]), 1),
                        }
                    )

            for rect in page.rects:
                width = float(rect["x1"]) - float(rect["x0"])
                height = float(rect["bottom"]) - float(rect["top"])
                if 4 <= width <= 22 and 4 <= height  None:
    lines_by_page: dict[int, list[float]] = {}
    for line in structure["lines"]:
        lines_by_page.setdefault(int(line["page"]), []).append(float(line["y"]))

    for page, y_coords in lines_by_page.items():
        unique_y = sorted(set(y_coords))
        for index in range(len(unique_y) - 1):
            row_top = unique_y[index]
            row_bottom = unique_y[index + 1]
            if row_bottom  dict[str, Any]:
    try:
        return _extract_with_pdfplumber(pdf_path, x_tolerance, y_tolerance)
    except Exception as exc:
        if exc.__class__.__name__ != "PdfSkillError" or "pdfplumber" not in str(exc):
            raise
        return _extract_with_pypdf(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract visible structure from a non-fillable PDF.")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("output_json", help="Output JSON path")
    parser.add_argument("--x-tolerance", type=float, default=2.0, help="Word grouping x tolerance")
    parser.add_argument("--y-tolerance", type=float, default=3.0, help="Word grouping y tolerance")
    args = parser.parse_args()

    try:
        print(f"Extracting structure from {args.input_pdf}...")
        structure = extract_form_structure(args.input_pdf, args.x_tolerance, args.y_tolerance)
        write_json(args.output_json, structure)
        print("Found:")
        print(f"  - {len(structure['pages'])} pages")
        print(f"  - {len(structure['labels'])} text labels")
        print(f"  - {len(structure['lines'])} horizontal lines")
        print(f"  - {len(structure['checkboxes'])} checkboxes")
        print(f"  - {len(structure['row_boundaries'])} row boundaries")
        for warning in structure.get("warnings", []):
            print(f"WARNING: {warning}")
        print(f"Saved to {args.output_json}")
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
