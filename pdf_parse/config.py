"""
Configuration options for PDF parsing.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParseConfig:
    """
    Configuration options for PDF parsing.
    
    Attributes:
        min_table_size: Minimum number of rows/columns for a valid table
        merge_cells: Whether to merge spanned cells
        preserve_formatting: Whether to preserve original formatting
        encoding: Text encoding for output
        page_range: Specific pages to parse (None for all pages)
        table_detection_threshold: Sensitivity for table detection
    """
    
    min_table_size: int = 2
    merge_cells: bool = True
    preserve_formatting: bool = False
    encoding: str = "utf-8"
    page_range: Optional[tuple] = None
    table_detection_threshold: float = 0.5
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if self.min_table_size < 1:
            raise ValueError("min_table_size must be at least 1")
        
        if not 0 <= self.table_detection_threshold <= 1:
            raise ValueError("table_detection_threshold must be between 0 and 1")
        
        if self.page_range is not None:
            if len(self.page_range) != 2 or self.page_range[0] > self.page_range[1]:
                raise ValueError("page_range must be a tuple of (start_page, end_page)")