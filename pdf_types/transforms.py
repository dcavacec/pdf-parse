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


def select_fields(df: pd.DataFrame, fields: List[str], allow_missing: bool = False) -> pd.DataFrame:
    """
    Select only specific fields/columns from the DataFrame.
    
    Args:
        df: Input DataFrame
        fields: List of field names to keep
        allow_missing: If True, missing fields are ignored; if False, raises error
        
    Returns:
        DataFrame with only the specified fields
    """
    return select_columns(df, fields, allow_missing)


def filter_by_field_values(df: pd.DataFrame, field: str, values: List[str], keep: bool = True) -> pd.DataFrame:
    """
    Filter rows based on specific field values.
    
    Args:
        df: Input DataFrame
        field: Field name to filter on
        values: List of values to match
        keep: If True, keep rows matching values; if False, exclude them
        
    Returns:
        Filtered DataFrame
    """
    if field not in df.columns:
        return df
    
    if keep:
        return df[df[field].isin(values)]
    else:
        return df[~df[field].isin(values)]


def extract_field_subset(df: pd.DataFrame, field_config: Dict[str, Any]) -> pd.DataFrame:
    """
    Extract a subset of data based on field configuration.
    
    Args:
        df: Input DataFrame
        field_config: Configuration dict with:
            - fields: List of fields to keep
            - filter_field: Field to filter on
            - filter_values: Values to keep/exclude
            - filter_keep: Whether to keep (True) or exclude (False) filter_values
            
    Returns:
        Filtered and field-selected DataFrame
    """
    result = df.copy()
    
    # Apply field filtering if specified
    if "filter_field" in field_config and "filter_values" in field_config:
        filter_field = field_config["filter_field"]
        filter_values = field_config["filter_values"]
        filter_keep = field_config.get("filter_keep", True)
        result = filter_by_field_values(result, filter_field, filter_values, filter_keep)
    
    # Select specific fields
    if "fields" in field_config:
        fields = field_config["fields"]
        allow_missing = field_config.get("allow_missing_fields", False)
        result = select_fields(result, fields, allow_missing)
    
    return result


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
        elif op == "select_fields":
            out = select_fields(out, step.get("fields") or [], bool(step.get("allow_missing", False)))
        elif op == "filter_by_field_values":
            out = filter_by_field_values(out, step.get("field") or "", step.get("values") or [], bool(step.get("keep", True)))
        elif op == "extract_field_subset":
            out = extract_field_subset(out, step.get("config") or {})
        else:
            # Unknown op: skip
            continue
    return out


