from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def rename_columns(df: pd.DataFrame, mapping: Dict[str, str], strict: bool = False) -> pd.DataFrame:
    new_cols = {c: mapping.get(str(c), c) for c in df.columns}
    if strict:
        missing = set(mapping.keys()) - {str(c) for c in df.columns}
        if missing:
            raise KeyError(f"Missing columns to rename: {sorted(missing)}")
    return df.rename(columns=new_cols)


def select_columns(df: pd.DataFrame, columns: List[str], allow_missing: bool = False) -> pd.DataFrame:
    cols = []
    for c in columns:
        if c in df.columns:
            cols.append(c)
        elif not allow_missing:
            raise KeyError(f"Column not found: {c}")
    return df[cols]


def cast_columns(df: pd.DataFrame, types: Dict[str, str], errors: str = "ignore") -> pd.DataFrame:
    out = df.copy()
    for col, t in types.items():
        if col not in out.columns:
            continue
        if t == "number":
            out[col] = pd.to_numeric(out[col].astype(str).str.replace(r"[^0-9\.-]", "", regex=True), errors=errors)
        elif t in ("int", "float", "string"):
            out[col] = out[col].astype(t, errors=errors) if t != "string" else out[col].astype(str)
        elif t == "date":
            out[col] = pd.to_datetime(out[col], errors=errors)
    return out


def filter_rows(df: pd.DataFrame, expr: str) -> pd.DataFrame:
    return df.query(expr, engine="python")


def derive_column(df: pd.DataFrame, name: str, expr: str) -> pd.DataFrame:
    out = df.copy()
    out[name] = pd.eval(expr, engine="python", target=out)  # simple expressions
    return out


def normalize_values(df: pd.DataFrame, strip: bool = True) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        out[col] = out[col].astype(str)
        if strip:
            out[col] = out[col].str.strip()
    return out


def apply_transforms(df: pd.DataFrame, steps: List[Dict[str, Any]]) -> pd.DataFrame:
    out = df
    for step in steps or []:
        op = (step.get("op") or "").lower()
        if op == "rename_columns":
            out = rename_columns(out, step.get("mapping") or {}, bool(step.get("strict", False)))
        elif op == "select_columns":
            out = select_columns(out, step.get("columns") or [], bool(step.get("allow_missing", False)))
        elif op == "cast_columns":
            out = cast_columns(out, step.get("types") or {}, errors=str(step.get("errors", "ignore")))
        elif op == "filter_rows":
            out = filter_rows(out, step.get("expr") or "True")
        elif op == "derive_column":
            out = derive_column(out, step.get("name") or "derived", step.get("expr") or "None")
        elif op == "normalize_values":
            out = normalize_values(out, strip=bool(step.get("strip", True)))
        else:
            # Unknown op: skip
            continue
    return out


