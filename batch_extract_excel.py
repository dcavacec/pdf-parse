"""
Batch extract: for each PDF in a directory, save its tables to an individual Excel workbook.

Usage:
    # Save one <pdf_stem>_tables.xlsx per PDF into the same directory
    python batch_extract_excel.py "C:\\Users\\david\\Downloads\\ruralAdj\\expt\\Zone 17"

    # Or specify an output directory for the generated workbooks
    python batch_extract_excel.py "C:\\path\\to\\in_dir" "C:\\path\\to\\out_dir"
"""

from pathlib import Path
import sys
import os
import pandas as pd

from pdf_table_extractor import PDFTableExtractor
from pdf_types import RulesRegistry
from pdf_types.pipeline import extract_and_process


def sanitize_sheet_name(name: str) -> str:
    # Excel sheet name constraints: <= 31 chars, no []:*?/\\ and not empty
    invalid = set('[]:*?/\\')
    clean = ''.join(c for c in name if c not in invalid).strip()
    if not clean:
        clean = "Sheet"
    return clean[:31]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python batch_extract_excel.py <input_directory> [output_dir] [--pdf-type TYPE] [--detect-type] [--rules RULES_DIR]")
        return 2

    in_dir = Path(sys.argv[1])
    if not in_dir.exists() or not in_dir.is_dir():
        print(f"Error: directory not found: {in_dir}")
        return 2

    # Determine output directory (default: same as input directory)
    # Parse optional args (simple positional + flags parsing to avoid argparse here)
    out_dir = in_dir
    pdf_type: str | None = None
    detect_type = False
    rules_dir: Path | None = None

    if len(sys.argv) > 2 and not sys.argv[2].startswith("--"):
        out_dir = Path(sys.argv[2])
        arg_start = 3
    else:
        arg_start = 2

    args = sys.argv[arg_start:]
    i = 0
    while i < len(args):
        tok = args[i]
        if tok == "--pdf-type" and i + 1 < len(args):
            pdf_type = args[i + 1]
            i += 2
        elif tok == "--detect-type":
            detect_type = True
            i += 1
        elif tok == "--rules" and i + 1 < len(args):
            rules_dir = Path(args[i + 1])
            i += 2
        else:
            i += 1
    if out_dir.suffix.lower() == ".xlsx":
        # If a file path was mistakenly provided, use its parent directory
        print(f"Note: output path '{out_dir}' looks like a file. Using its parent directory.")
        out_dir = out_dir.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    extractor = PDFTableExtractor()
    # Initialize registry
    if rules_dir is None:
        # Allow env var override; default to ./rules
        env_rules = os.environ.get("PDF_PARSE_RULES_PATH")
        rules_dir = Path(env_rules) if env_rules else Path("rules")
    registry = RulesRegistry(rules_dir)

    pdf_files = sorted(in_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in: {in_dir}")
        return 1

    total_tables = 0

    for pdf_path in pdf_files:
        try:
            chosen_type = pdf_type
            if detect_type and not chosen_type:
                chosen_type = registry.detect_type(pdf_path)

            if chosen_type:
                rules = registry.load_type(chosen_type)
                tables, meta = extract_and_process(pdf_path, method="auto", pages=None, rules=rules)
            else:
                tables = extractor.extract_tables_from_pdf(pdf_path, method="auto")
        except Exception as e:
            print(f"Warning: failed to extract from {pdf_path.name}: {e}")
            continue

        if not tables:
            print(f"No tables found in {pdf_path.name}; skipping workbook.")
            continue

        # One workbook per source PDF
        out_xlsx = out_dir / f"{pdf_path.stem}_tables.xlsx"
        with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:
            for i, df in enumerate(tables, 1):
                sheet_name = sanitize_sheet_name(f"Table_{i}")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        total_tables += len(tables)
        print(f"Saved {len(tables)} table(s) from {pdf_path.name} to: {out_xlsx}")

    print(f"Done. Processed {len(pdf_files)} PDF(s); wrote {total_tables} table(s) across per-file workbooks in: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


