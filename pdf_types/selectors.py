from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple
import re

import pandas as pd


def by_table_index(tables: List[pd.DataFrame], indices: Iterable[int]) -> List[Tuple[int, pd.DataFrame]]:
    wanted = set(int(i) for i in indices)
    return [(i, df) for i, df in enumerate(tables, 1) if i in wanted]


def by_header_contains(tables: List[pd.DataFrame], required_headers: List[str], min_match: float = 1.0) -> List[Tuple[int, pd.DataFrame]]:
    required = [h.strip().lower() for h in required_headers if str(h).strip()]
    results: List[Tuple[int, pd.DataFrame]] = []
    for i, df in enumerate(tables, 1):
        headers = [str(c).strip().lower() for c in df.columns]
        hits = sum(1 for r in required if any(r in h for h in headers))
        ratio = hits / max(1, len(required))
        if ratio >= min_match:
            results.append((i, df))
    return results


def by_shape(tables: List[pd.DataFrame], min_rows: int = 1, min_cols: int = 1) -> List[Tuple[int, pd.DataFrame]]:
    return [(i, df) for i, df in enumerate(tables, 1) if df.shape[0] >= min_rows and df.shape[1] >= min_cols]


def by_regex_in_row(tables: List[pd.DataFrame], pattern: str) -> List[Tuple[int, pd.DataFrame]]:
    rx = re.compile(pattern)
    matched: List[Tuple[int, pd.DataFrame]] = []
    for i, df in enumerate(tables, 1):
        if df.astype(str).apply(lambda col: col.str.contains(rx)).any(axis=None):
            matched.append((i, df))
    return matched


def filter_tables(tables: List[pd.DataFrame], selectors: Dict[str, Any]) -> List[pd.DataFrame]:
    if not selectors:
        return tables

    # Start with all tables, narrow via AND semantics
    candidate_indices = set(range(1, len(tables) + 1))

    if "indices" in selectors:
        candidate_indices &= set(int(x) for x in selectors["indices"])

    if "header_contains" in selectors:
        req = selectors["header_contains"] or []
        min_match = float(selectors.get("min_match", 1.0))
        idxs = {i for i, _ in by_header_contains(tables, req, min_match=min_match)}
        candidate_indices &= idxs

    if "min_shape" in selectors:
        ms = selectors["min_shape"] or {}
        idxs = {i for i, _ in by_shape(tables, ms.get("rows", 1), ms.get("cols", 1))}
        candidate_indices &= idxs

    if "regex" in selectors:
        idxs = {i for i, _ in by_regex_in_row(tables, selectors["regex"]) }
        candidate_indices &= idxs

    if not candidate_indices:
        return []

    return [tables[i - 1] for i in sorted(candidate_indices)]


