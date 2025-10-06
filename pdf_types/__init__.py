"""
Typed extraction scaffolding for pdf-parse.

This package provides:
- A registry to load/detect PDF type rules
- Selectors to pick target tables
- Transforms to normalize/reshape DataFrames
- A pipeline to orchestrate extraction + processing
"""

from .registry import PdfTypeRules, RulesRegistry
from .pipeline import extract_and_process

__all__ = [
    "PdfTypeRules",
    "RulesRegistry",
    "extract_and_process",
]


