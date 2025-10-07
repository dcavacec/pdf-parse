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
        # Apply deduplication by default even without rules
        deduplicated = _remove_duplicate_tables(raw_tables)
        return deduplicated, {"selected": len(deduplicated), "raw": len(raw_tables)}

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

    # Apply deduplication to processed tables
    deduplicated = _remove_duplicate_tables(processed)

    meta = {
        "raw": len(raw_tables),
        "selected": len(selected),
        "processed": len(processed),
        "deduplicated": len(deduplicated),
        "type": rules.name,
    }
    return deduplicated, meta


def _remove_duplicate_tables(tables: List[pd.DataFrame]) -> List[pd.DataFrame]:
    """Remove duplicate tables based on shape and content."""
    unique_tables = []
    
    for table in tables:
        is_duplicate = False
        for existing_table in unique_tables:
            if (table.shape == existing_table.shape and 
                table.equals(existing_table)):
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_tables.append(table)
    
    return unique_tables


