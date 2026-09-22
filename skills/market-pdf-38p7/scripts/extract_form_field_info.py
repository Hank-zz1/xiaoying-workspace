from __future__ import annotations

import argparse

from _pdf_utils import (
    extract_acroform_field_info,
    get_field_info,
    handle_cli_error,
    import_required,
    input_path,
    write_json,
)


def write_field_info(pdf_path: str, json_output_path: str) -> int:
    pypdf = import_required("pypdf")
    reader = pypdf.PdfReader(str(input_path(pdf_path, ".pdf")))
    field_info, warnings = extract_acroform_field_info(reader)
    write_json(json_output_path, field_info)
    for warning in warnings:
        print(f"WARNING: {warning}")
    print(f"Wrote {len(field_info)} fields to {json_output_path}")
    return len(field_info)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract AcroForm field metadata from a PDF.")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("output_json", help="Output JSON path")
    args = parser.parse_args()

    try:
        write_field_info(args.input_pdf, args.output_json)
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
