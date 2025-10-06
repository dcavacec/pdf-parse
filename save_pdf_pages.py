"""
Save specified pages from a PDF, either overwriting the original or writing a copy.

Usage:
    # Save pages 1,3,5 into a new file next to the original
    python save_pdf_pages.py "C:\\path\\to\\file.pdf" --pages 1,3,5

    # Overwrite the original with pages 1-3 only
    python save_pdf_pages.py "C:\\path\\to\\file.pdf" --pages 1-3 --overwrite

Notes:
    - Pages are 1-based. Ranges like 1-3 are supported; combine with commas.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import List

from pypdf import PdfReader, PdfWriter


def parse_pages(pages_arg: str) -> List[int]:
    pages: List[int] = []
    for part in pages_arg.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = int(a)
            end = int(b)
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(part))
    # Deduplicate and sort
    return sorted(set(p for p in pages if p > 0))


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python save_pdf_pages.py <pdf_file> --pages <list> [--overwrite] [--out <output_file>]")
        return 2

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: file not found: {pdf_path}")
        return 2

    # Simple flag parsing
    overwrite = False
    out_file: Path | None = None
    pages_spec: str | None = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        tok = args[i]
        if tok == "--pages" and i + 1 < len(args):
            pages_spec = args[i + 1]
            i += 2
        elif tok == "--overwrite":
            overwrite = True
            i += 1
        elif tok == "--out" and i + 1 < len(args):
            out_file = Path(args[i + 1])
            i += 2
        else:
            i += 1

    if not pages_spec:
        print("Error: --pages is required (e.g., 1,3,5 or 1-3)")
        return 2

    page_numbers = parse_pages(pages_spec)
    if not page_numbers:
        print("Error: no valid pages parsed")
        return 2

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()

    max_page = len(reader.pages)
    zero_based = [p - 1 for p in page_numbers if 1 <= p <= max_page]
    if not zero_based:
        print("Error: no pages in range of the document")
        return 2

    for p in zero_based:
        writer.add_page(reader.pages[p])

    if overwrite:
        # Write to a temp file then replace atomically
        tmp = pdf_path.with_suffix(".tmp.pdf")
        with open(tmp, "wb") as f:
            writer.write(f)
        tmp.replace(pdf_path)
        print(f"Overwrote {pdf_path} with pages {page_numbers}")
    else:
        if not out_file:
            out_file = pdf_path.with_name(f"{pdf_path.stem}_pages.pdf")
        with open(out_file, "wb") as f:
            writer.write(f)
        print(f"Saved pages {page_numbers} to: {out_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


