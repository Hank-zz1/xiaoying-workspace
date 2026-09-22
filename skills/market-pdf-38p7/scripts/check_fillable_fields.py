from __future__ import annotations

import argparse

from _pdf_utils import handle_cli_error, import_required, input_path


def has_fillable_fields(pdf_path: str) -> bool:
    pypdf = import_required("pypdf")
    reader = pypdf.PdfReader(str(input_path(pdf_path, ".pdf")))
    return bool(reader.get_fields())


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether a PDF contains AcroForm fields.")
    parser.add_argument("pdf", help="Input PDF path")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    try:
        result = has_fillable_fields(args.pdf)
    except Exception as exc:
        handle_cli_error(exc)
        return

    if args.json:
        print('{"fillable": %s}' % ("true" if result else "false"))
    elif result:
        print("This PDF has fillable form fields")
    else:
        print("This PDF does not have fillable form fields; use annotation/overlay filling")


if __name__ == "__main__":
    main()
