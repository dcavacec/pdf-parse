"""
PDF Table Extractor
A comprehensive tool for extracting tabular data from PDF documents and loading into pandas DataFrames.
"""

import pandas as pd
import pypdf
import pdfplumber
import tabula
import camelot
import numpy as np
from typing import List, Dict, Optional, Union
import logging
import warnings
from pathlib import Path

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFTableExtractor:
    """
    A comprehensive PDF table extraction tool that uses multiple methods
    to extract tabular data from PDF documents.
    """
    
    def __init__(self):
        self.extracted_tables = []
        self.extraction_methods = ['pdfplumber', 'tabula', 'camelot']
    
    def extract_tables_from_pdf(self, pdf_path: Union[str, Path], 
                               method: str = 'auto',
                               pages: Optional[Union[int, List[int]]] = None) -> List[pd.DataFrame]:
        """
        Extract tables from a PDF document using specified method.
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method ('pdfplumber', 'tabula', 'camelot', or 'auto')
            pages: Specific pages to extract from (None for all pages)
            
        Returns:
            List of pandas DataFrames containing extracted tables
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Extracting tables from {pdf_path.name}")
        
        if method == 'auto':
            # Try multiple methods and return the best results
            return self._extract_with_multiple_methods(pdf_path, pages)
        elif method == 'pdfplumber':
            return self._extract_with_pdfplumber(pdf_path, pages)
        elif method == 'tabula':
            return self._extract_with_tabula(pdf_path, pages)
        elif method == 'camelot':
            return self._extract_with_camelot(pdf_path, pages)
        else:
            raise ValueError(f"Unknown extraction method: {method}")
    
    def _extract_with_multiple_methods(self, pdf_path: Path, pages: Optional[Union[int, List[int]]]) -> List[pd.DataFrame]:
        """Try multiple extraction methods and return the best results."""
        all_tables = []
        
        for method in self.extraction_methods:
            try:
                logger.info(f"Trying extraction with {method}")
                if method == 'pdfplumber':
                    tables = self._extract_with_pdfplumber(pdf_path, pages)
                elif method == 'tabula':
                    tables = self._extract_with_tabula(pdf_path, pages)
                elif method == 'camelot':
                    tables = self._extract_with_camelot(pdf_path, pages)
                
                if tables:
                    all_tables.extend(tables)
                    logger.info(f"Successfully extracted {len(tables)} tables with {method}")
                    
            except Exception as e:
                logger.warning(f"Failed to extract with {method}: {str(e)}")
                continue
        
        # Remove duplicates and return unique tables
        deduplicated = self._remove_duplicate_tables(all_tables)
        logger.info(f"Removed {len(all_tables) - len(deduplicated)} duplicate tables")
        return deduplicated
    
    def _extract_with_pdfplumber(self, pdf_path: Path, pages: Optional[Union[int, List[int]]]) -> List[pd.DataFrame]:
        """Extract tables using pdfplumber."""
        tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            if pages is None:
                pages_to_process = range(len(pdf.pages))
            elif isinstance(pages, int):
                pages_to_process = [pages - 1]  # Convert to 0-based indexing
            else:
                pages_to_process = [p - 1 for p in pages]  # Convert to 0-based indexing
            
            for page_num in pages_to_process:
                if page_num >= len(pdf.pages):
                    continue
                    
                page = pdf.pages[page_num]
                page_tables = page.extract_tables()
                
                for table in page_tables:
                    if table and len(table) > 1:  # Ensure table has data
                        df = pd.DataFrame(table[1:], columns=table[0])
                        df = self._clean_dataframe(df)
                        if not df.empty:
                            tables.append(df)
        
        return tables
    
    def _extract_with_tabula(self, pdf_path: Path, pages: Optional[Union[int, List[int]]]) -> List[pd.DataFrame]:
        """Extract tables using tabula-py."""
        try:
            if pages is None:
                tables = tabula.read_pdf(str(pdf_path), pages='all', multiple_tables=True)
            elif isinstance(pages, int):
                tables = tabula.read_pdf(str(pdf_path), pages=pages, multiple_tables=True)
            else:
                tables = tabula.read_pdf(str(pdf_path), pages=pages, multiple_tables=True)
            
            cleaned_tables = []
            for table in tables:
                if isinstance(table, pd.DataFrame):
                    df = self._clean_dataframe(table)
                    if not df.empty:
                        cleaned_tables.append(df)
            
            return cleaned_tables
        except Exception as e:
            logger.warning(f"Tabula extraction failed: {str(e)}")
            return []
    
    def _extract_with_camelot(self, pdf_path: Path, pages: Optional[Union[int, List[int]]]) -> List[pd.DataFrame]:
        """Extract tables using camelot."""
        try:
            if pages is None:
                tables = camelot.read_pdf(str(pdf_path), pages='all')
            elif isinstance(pages, int):
                tables = camelot.read_pdf(str(pdf_path), pages=str(pages))
            else:
                pages_str = ','.join(map(str, pages))
                tables = camelot.read_pdf(str(pdf_path), pages=pages_str)
            
            cleaned_tables = []
            for table in tables:
                df = table.df
                df = self._clean_dataframe(df)
                if not df.empty:
                    cleaned_tables.append(df)
            
            return cleaned_tables
        except Exception as e:
            logger.warning(f"Camelot extraction failed: {str(e)}")
            return []
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize extracted DataFrame."""
        if df.empty:
            return df
        
        # Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Remove rows where all values are NaN or empty strings
        df = df.dropna(how='all')
        
        # Convert all columns to string and strip whitespace
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', '')
        
        return df
    
    def _remove_duplicate_tables(self, tables: List[pd.DataFrame]) -> List[pd.DataFrame]:
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
    
    def save_tables_to_excel(self, tables: List[pd.DataFrame], output_path: Union[str, Path]):
        """Save extracted tables to an Excel file."""
        output_path = Path(output_path)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                sheet_name = f'Table_{i+1}'
                table.to_excel(writer, sheet_name=sheet_name, index=False)
        
        logger.info(f"Saved {len(tables)} tables to {output_path}")
    
    def save_tables_to_csv(self, tables: List[pd.DataFrame], output_dir: Union[str, Path]):
        """Save extracted tables to CSV files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        for i, table in enumerate(tables):
            csv_path = output_dir / f'table_{i+1}.csv'
            table.to_csv(csv_path, index=False)
        
        logger.info(f"Saved {len(tables)} tables to {output_dir}")
    
    def get_table_summary(self, tables: List[pd.DataFrame]) -> Dict:
        """Get summary information about extracted tables."""
        summary = {
            'total_tables': len(tables),
            'tables_info': []
        }
        
        for i, table in enumerate(tables):
            table_info = {
                'table_number': i + 1,
                'shape': table.shape,
                'columns': list(table.columns),
                'sample_data': table.head(3).to_dict('records') if not table.empty else []
            }
            summary['tables_info'].append(table_info)
        
        return summary


def main():
    """Example usage of the PDFTableExtractor."""
    extractor = PDFTableExtractor()
    
    # Example usage
    pdf_path = "sample.pdf"  # Replace with actual PDF path
    
    try:
        # Extract tables from PDF
        tables = extractor.extract_tables_from_pdf(pdf_path, method='auto')
        
        if tables:
            print(f"Successfully extracted {len(tables)} tables")
            
            # Display summary
            summary = extractor.get_table_summary(tables)
            print("\nTable Summary:")
            for table_info in summary['tables_info']:
                print(f"Table {table_info['table_number']}: {table_info['shape']}")
                print(f"Columns: {table_info['columns']}")
                print()
            
            # Save to Excel
            extractor.save_tables_to_excel(tables, "extracted_tables.xlsx")
            
            # Save to CSV files
            extractor.save_tables_to_csv(tables, "extracted_tables")
            
        else:
            print("No tables found in the PDF")
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()