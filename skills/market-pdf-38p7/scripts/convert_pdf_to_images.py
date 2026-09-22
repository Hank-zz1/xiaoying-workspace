from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from _pdf_utils import PdfSkillError, ensure_output_dir, handle_cli_error, import_required, input_path


def _resize_if_needed(image, max_dim: int):
    if max_dim <= 0:
        return image
    width, height = image.size
    if width  int:
    source = input_path(pdf_path, ".pdf")
    target_dir = ensure_output_dir(output_dir)

    pypdf = import_required("pypdf")
    reader = pypdf.PdfReader(str(source))
    total_pages = len(reader.pages)
    if total_pages == 0:
        raise PdfSkillError("PDF contains no pages.")

    last = last_page or total_pages
    if first_page  None:
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG images.")
    parser.add_argument("input_pdf", help="Input PDF path")
    parser.add_argument("output_directory", help="Directory for page_*.png")
    parser.add_argument("--dpi", type=int, default=200, help="Render DPI (default: 200)")
    parser.add_argument(
        "--max-dim",
        type=int,
        default=2000,
        help="Resize output so the longest side is at most this many pixels; use 0 to disable",
    )
    parser.add_argument("--first-page", type=int, default=1, help="First 1-based page to render")
    parser.add_argument("--last-page", type=int, help="Last 1-based page to render")
    args = parser.parse_args()

    try:
        convert(
            args.input_pdf,
            args.output_directory,
            dpi=args.dpi,
            max_dim=args.max_dim,
            first_page=args.first_page,
            last_page=args.last_page,
        )
    except Exception as exc:
        handle_cli_error(exc)


if __name__ == "__main__":
    main()
