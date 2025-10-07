"""
Tests for type-aware extraction pipeline.
"""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from pdf_types.registry import PdfTypeRules, RulesRegistry
from pdf_types.pipeline import extract_and_process


def make_df(cols, rows=3):
    data = {c: list(range(rows)) for c in cols}
    return pd.DataFrame(data)


def test_filter_by_header_and_transform(tmp_path: Path):
    # Prepare fake tables
    tables = [
        make_df(["Product", "Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales", "Total"]),
        make_df(["NoiseA", "NoiseB"])  # should be filtered out
    ]

    rules = PdfTypeRules(
        name="rural_adj",
        selection={"method": "auto", "pages": None},
        extraction={"header_contains": ["Product", "Q1", "Q2", "Q3", "Q4", "Total"], "min_match": 0.4},
        transforms=[
            {"op": "rename_columns", "mapping": {"Q1 Sales": "Q1"}},
            {"op": "cast_columns", "types": {"Q1": "number"}},
        ],
        output={}
    )

    with patch("pdf_types.pipeline.PDFTableExtractor") as MockExt:
        inst = MockExt.return_value
        inst.extract_tables_from_pdf.return_value = tables
        processed, meta = extract_and_process(Path("dummy.pdf"), method="auto", pages=None, rules=rules)

    assert meta["raw"] == 2
    assert meta["selected"] == 1
    assert len(processed) == 1
    assert "Q1" in processed[0].columns


def test_registry_detect_type(tmp_path: Path):
    # Create a temporary rules directory
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    (rules_dir / "foo.yml").write_text(
        """
name: foo
selection:
  filename_patterns: ["*bar*.pdf"]
        """.strip(),
        encoding="utf-8",
    )

    reg = RulesRegistry(rules_dir)
    assert reg.detect_type(Path("great-bar-report.pdf")) == "foo"
    assert reg.detect_type(Path("unmatched.pdf")) is None


