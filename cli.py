"""
Command Line Interface for PDF Table Extractor
"""

import argparse
import sys
from pathlib import Path
from pdf_table_extractor import PDFTableExtractor
import json
import os

from pdf_types import RulesRegistry
from pdf_types.pipeline import extract_and_process
from java_check import JAVA_AVAILABLE, JAVA_VERSION


def main():
    parser = argparse.ArgumentParser(
        description="Extract tabular data from PDF documents and save to various formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all tables from a PDF
  python cli.py input.pdf
  
  # Extract tables from specific pages
  python cli.py input.pdf --pages 1,3,5
  
  # Use specific extraction method
  python cli.py input.pdf --method tabula
  
  # Save to Excel file
  python cli.py input.pdf --output tables.xlsx
  
  # Save to CSV files in directory
  python cli.py input.pdf --output-dir extracted_tables/
  
  # Get summary information
  python cli.py input.pdf --summary
        """
    )
    
    parser.add_argument(
        'pdf_file',
        help='Path to the PDF file to extract tables from'
    )
    
    parser.add_argument(
        '--method',
        choices=['auto', 'pdfplumber', 'camelot'] + (['tabula'] if JAVA_AVAILABLE else []),
        default='auto',
        help='Extraction method to use (default: auto)'
    )
    
    parser.add_argument(
        '--pages',
        help='Comma-separated list of page numbers to extract from (e.g., 1,3,5)'
    )
    
    parser.add_argument(
        '--output',
        help='Output Excel file path'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for CSV files'
    )
    
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Display summary information about extracted tables'
    )
    parser.add_argument(
        '--pdf-type',
        help='Apply type-specific selection and transforms (name in rules directory)'
    )
    parser.add_argument(
        '--detect-type',
        action='store_true',
        help='Auto-detect PDF type using filename patterns in rules directory'
    )
    parser.add_argument(
        '--rules',
        help='Path to rules directory (default: ./rules or PDF_PARSE_RULES_PATH)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Parse pages
    pages = None
    if args.pages:
        try:
            pages = [int(p.strip()) for p in args.pages.split(',')]
        except ValueError:
            print("Error: Invalid page numbers. Use comma-separated integers (e.g., 1,3,5)")
            sys.exit(1)
    
    # Initialize extractor and registry
    extractor = PDFTableExtractor()
    rules_dir = Path(args.rules) if args.rules else Path(os.environ.get('PDF_PARSE_RULES_PATH') or 'rules')
    registry = RulesRegistry(rules_dir)
    
    try:
        print(f"Extracting tables from {pdf_path.name}...")
        print(f"Method: {args.method}")
        if not JAVA_AVAILABLE and args.method == 'tabula':
            print(f"Warning: Tabula requires Java runtime. Java not detected.")
            print(f"Available methods: pdfplumber, camelot")
            sys.exit(1)
        if pages:
            print(f"Pages: {pages}")
        print()
        
        # Extract tables
        chosen_type = args.pdf_type
        if args.detect_type and not chosen_type:
            chosen_type = registry.detect_type(pdf_path)

        if chosen_type:
            rules = registry.load_type(chosen_type)
            tables, _meta = extract_and_process(
                pdf_path,
                method=args.method,
                pages=pages,
                rules=rules,
            )
        else:
            tables = extractor.extract_tables_from_pdf(
                pdf_path,
                method=args.method,
                pages=pages
            )
        
        if not tables:
            print("No tables found in the PDF.")
            print("\nTroubleshooting tips:")
            print("- Try a different extraction method")
            print("- Check if the PDF contains actual tabular data")
            print("- Ensure the PDF is not password-protected")
            sys.exit(1)
        
        print(f"Successfully extracted {len(tables)} tables!")
        
        # Display summary
        if args.summary or args.verbose:
            summary = extractor.get_table_summary(tables)
            print(f"\nSummary:")
            print(f"Total tables: {summary['total_tables']}")
            
            for table_info in summary['tables_info']:
                print(f"Table {table_info['table_number']}: {table_info['shape'][0]} rows × {table_info['shape'][1]} columns")
                if args.verbose:
                    print(f"  Columns: {table_info['columns']}")
            print()
        
        # Save output
        if args.output:
            output_path = Path(args.output)
            extractor.save_tables_to_excel(tables, output_path)
            print(f"Tables saved to Excel file: {output_path}")
        
        if args.output_dir:
            output_dir = Path(args.output_dir)
            extractor.save_tables_to_csv(tables, output_dir)
            print(f"Tables saved to CSV files in: {output_dir}")
        
        # If no output specified, save to default locations
        if not args.output and not args.output_dir:
            # Save to Excel
            excel_path = pdf_path.stem + "_tables.xlsx"
            extractor.save_tables_to_excel(tables, excel_path)
            print(f"Tables saved to Excel file: {excel_path}")
            
            # Save to CSV directory
            csv_dir = pdf_path.stem + "_tables"
            extractor.save_tables_to_csv(tables, csv_dir)
            print(f"Tables saved to CSV files in: {csv_dir}")
        
        print("\nExtraction completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()