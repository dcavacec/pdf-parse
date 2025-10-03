"""
Main PDF parser class for extracting tabular data from PDF documents.
"""

import io
from typing import List, Optional, Union
from pathlib import Path

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

from .table import Table
from .config import ParseConfig


class PDFParseError(Exception):
    """Custom exception for PDF parsing errors."""
    pass


class PDFParser:
    """
    Main class for parsing PDF documents and extracting tabular data.
    
    This class provides methods to parse PDF files and extract structured
    table data with configurable options.
    """
    
    def __init__(self, config: Optional[ParseConfig] = None):
        """
        Initialize the PDF parser.
        
        Args:
            config: Optional configuration object for parsing options
        """
        if PyPDF2 is None:
            raise ImportError(
                "PyPDF2 is required but not installed. "
                "Install it with: pip install PyPDF2"
            )
        
        self.config = config or ParseConfig()
    
    def parse_pdf(self, file_path: Union[str, Path]) -> List[Table]:
        """
        Parse a PDF file and extract tables.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Table objects extracted from the PDF
            
        Raises:
            PDFParseError: If parsing fails
            FileNotFoundError: If PDF file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                return self.parse_pdf_from_bytes(file.read())
        except Exception as e:
            raise PDFParseError(f"Failed to parse PDF file {file_path}: {str(e)}")
    
    def parse_pdf_from_bytes(self, pdf_bytes: bytes) -> List[Table]:
        """
        Parse PDF from byte data and extract tables.
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            List of Table objects extracted from the PDF
            
        Raises:
            PDFParseError: If parsing fails
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            return self._extract_tables_from_pdf(pdf_reader)
        except Exception as e:
            raise PDFParseError(f"Failed to parse PDF from bytes: {str(e)}")
    
    def _extract_tables_from_pdf(self, pdf_reader) -> List[Table]:
        """
        Extract tables from a PyPDF2 PdfReader object.
        
        Args:
            pdf_reader: PyPDF2 PdfReader object
            
        Returns:
            List of Table objects
        """
        tables = []
        
        # Determine which pages to process
        if self.config.page_range:
            start_page, end_page = self.config.page_range
            pages_to_process = range(start_page - 1, min(end_page, len(pdf_reader.pages)))
        else:
            pages_to_process = range(len(pdf_reader.pages))
        
        for page_num in pages_to_process:
            try:
                page = pdf_reader.pages[page_num]
                page_tables = self._extract_tables_from_page(page, page_num + 1)
                tables.extend(page_tables)
            except Exception as e:
                # Log error but continue with other pages
                print(f"Warning: Failed to process page {page_num + 1}: {str(e)}")
                continue
        
        return tables
    
    def _extract_tables_from_page(self, page, page_num: int) -> List[Table]:
        """
        Extract tables from a single PDF page.
        
        Args:
            page: PyPDF2 page object
            page_num: Page number (1-based)
            
        Returns:
            List of Table objects found on the page
        """
        tables = []
        
        try:
            # Extract text from page
            text = page.extract_text()
            
            if not text.strip():
                return tables
            
            # Simple table detection based on text patterns
            potential_tables = self._detect_tables_in_text(text)
            
            for table_data in potential_tables:
                if self._is_valid_table(table_data):
                    table = Table(table_data)
                    tables.append(table)
        
        except Exception as e:
            print(f"Warning: Failed to extract tables from page {page_num}: {str(e)}")
        
        return tables
    
    def _detect_tables_in_text(self, text: str) -> List[List[List[str]]]:
        """
        Detect potential tables in extracted text.
        
        This is a simplified table detection algorithm. In a real implementation,
        you would use more sophisticated methods like:
        - Analyzing text positioning and alignment
        - Using machine learning models
        - Integrating with specialized PDF table extraction libraries
        
        Args:
            text: Extracted text from PDF page
            
        Returns:
            List of potential table data (list of rows, each row is list of cells)
        """
        lines = text.strip().split('\n')
        potential_tables = []
        current_table = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple heuristic: lines with multiple spaces or tabs might be table rows
            if '\t' in line or line.count('  ') >= 2:
                # Split by tabs or multiple spaces
                if '\t' in line:
                    cells = [cell.strip() for cell in line.split('\t')]
                else:
                    # Split by multiple spaces
                    cells = [cell.strip() for cell in line.split('  ') if cell.strip()]
                
                if len(cells) >= self.config.min_table_size:
                    current_table.append(cells)
                else:
                    # End current table if it exists
                    if current_table:
                        potential_tables.append(current_table)
                        current_table = []
            else:
                # End current table if it exists
                if current_table:
                    potential_tables.append(current_table)
                    current_table = []
        
        # Add final table if it exists
        if current_table:
            potential_tables.append(current_table)
        
        return potential_tables
    
    def _is_valid_table(self, table_data: List[List[str]]) -> bool:
        """
        Check if detected table data is valid according to configuration.
        
        Args:
            table_data: List of table rows
            
        Returns:
            True if table is valid, False otherwise
        """
        if not table_data:
            return False
        
        # Check minimum size requirements
        if len(table_data) < self.config.min_table_size:
            return False
        
        # Check if all rows have consistent column count
        if len(table_data) > 1:
            first_row_cols = len(table_data[0])
            for row in table_data[1:]:
                if len(row) != first_row_cols:
                    return False
        
        return True