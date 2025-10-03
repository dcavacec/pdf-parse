"""
PDF Parse - A Python library for extracting tabular data from PDF documents.

This package provides tools for parsing PDF files and extracting structured
tabular data with high accuracy and flexible output formats.
"""

from .parser import PDFParser
from .table import Table
from .config import ParseConfig

__version__ = "1.0.0"
__author__ = "PDF Parse Contributors"
__email__ = "contact@pdf-parse.dev"

__all__ = ["PDFParser", "Table", "ParseConfig"]