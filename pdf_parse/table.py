"""
Table class for representing extracted tables from PDF documents.
"""

import csv
import json
from typing import List, Dict, Any, Optional


class Table:
    """
    Represents an extracted table from a PDF document.
    
    This class provides methods for accessing table data and exporting
    to various formats like CSV, JSON, and dictionaries.
    """
    
    def __init__(self, data: List[List[str]], columns: Optional[List[str]] = None):
        """
        Initialize a Table object.
        
        Args:
            data: 2D list of table data (rows x columns)
            columns: Optional list of column names
        """
        self.data = data
        self.columns = columns or [f"Column_{i+1}" for i in range(len(data[0]) if data else 0)]
        self.rows = data
    
    @property
    def row_count(self) -> int:
        """Return the number of rows in the table."""
        return len(self.data)
    
    @property
    def column_count(self) -> int:
        """Return the number of columns in the table."""
        return len(self.columns)
    
    def get_cell(self, row: int, col: int) -> str:
        """
        Get the value of a specific cell.
        
        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            
        Returns:
            Cell value as string
            
        Raises:
            IndexError: If row or column index is out of range
        """
        if not (0 <= row < self.row_count and 0 <= col < self.column_count):
            raise IndexError(f"Cell ({row}, {col}) is out of range")
        return self.data[row][col]
    
    def get_row(self, row: int) -> List[str]:
        """
        Get a specific row.
        
        Args:
            row: Row index (0-based)
            
        Returns:
            List of cell values in the row
        """
        if not (0 <= row < self.row_count):
            raise IndexError(f"Row {row} is out of range")
        return self.data[row]
    
    def get_column(self, col: int) -> List[str]:
        """
        Get a specific column.
        
        Args:
            col: Column index (0-based)
            
        Returns:
            List of cell values in the column
        """
        if not (0 <= col < self.column_count):
            raise IndexError(f"Column {col} is out of range")
        return [row[col] for row in self.data]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert table to dictionary format.
        
        Returns:
            Dictionary with table data and metadata
        """
        return {
            "columns": self.columns,
            "rows": self.data,
            "row_count": self.row_count,
            "column_count": self.column_count
        }
    
    def to_csv(self, file_path: str, delimiter: str = ",") -> None:
        """
        Export table to CSV file.
        
        Args:
            file_path: Path to output CSV file
            delimiter: CSV delimiter character
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter)
            
            # Write header row
            writer.writerow(self.columns)
            
            # Write data rows
            writer.writerows(self.data)
    
    def to_json(self, file_path: str, indent: int = 2) -> None:
        """
        Export table to JSON file.
        
        Args:
            file_path: Path to output JSON file
            indent: JSON indentation level
        """
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.to_dict(), jsonfile, indent=indent, ensure_ascii=False)
    
    def to_string(self, max_width: int = 80) -> str:
        """
        Convert table to formatted string representation.
        
        Args:
            max_width: Maximum width for table display
            
        Returns:
            Formatted string representation of the table
        """
        if not self.data:
            return "Empty table"
        
        # Calculate column widths
        col_widths = []
        for i in range(self.column_count):
            max_width_col = len(self.columns[i])
            for row in self.data:
                max_width_col = max(max_width_col, len(str(row[i])))
            col_widths.append(min(max_width_col, max_width // self.column_count))
        
        # Build table string
        lines = []
        
        # Header
        header_parts = []
        for i, col in enumerate(self.columns):
            header_parts.append(col.ljust(col_widths[i]))
        lines.append(" | ".join(header_parts))
        lines.append("-" * len(lines[0]))
        
        # Data rows
        for row in self.data:
            row_parts = []
            for i, cell in enumerate(row):
                row_parts.append(str(cell).ljust(col_widths[i]))
            lines.append(" | ".join(row_parts))
        
        return "\n".join(lines)
    
    def __str__(self) -> str:
        """String representation of the table."""
        return self.to_string()
    
    def __repr__(self) -> str:
        """Detailed string representation of the table."""
        return f"Table(rows={self.row_count}, columns={self.column_count})"