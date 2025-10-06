from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd

from pdf_table_extractor import PDFTableExtractor
from .registry import PdfTypeRules
from .selectors import filter_tables
from .transforms import apply_transforms


def extract_and_process(
    pdf_path: Path,
    method: str = "auto",
    pages: Optional[List[int]] = None,
    rules: Optional[PdfTypeRules] = None,
) -> Tuple[List[pd.DataFrame], dict]:
    """Run extraction then apply selection and transforms based on rules."""
    extractor = PDFTableExtractor()
    raw_tables = extractor.extract_tables_from_pdf(pdf_path, method=method, pages=pages)

    if not rules:
        return raw_tables, {"selected": len(raw_tables), "raw": len(raw_tables)}

    # Selection overrides from rules.selection/extraction
    sel_method = (rules.selection or {}).get("method", method)
    sel_pages = (rules.selection or {}).get("pages", pages)
    if sel_method != method or sel_pages != pages:
        raw_tables = extractor.extract_tables_from_pdf(pdf_path, method=sel_method, pages=sel_pages)

    selected = filter_tables(raw_tables, rules.extraction or {})
    processed: List[pd.DataFrame] = []
    for df in selected:
        out = apply_transforms(df, rules.transforms or [])
        processed.append(out)

    meta = {
        "raw": len(raw_tables),
        "selected": len(selected),
        "processed": len(processed),
        "type": rules.name,
    }
    return processed, meta


