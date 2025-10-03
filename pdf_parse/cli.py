"""
Command-line interface for PDF Parse.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .parser import PDFParser
from .config import ParseConfig


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract tabular data from PDF documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-parse document.pdf                    # Extract tables from document.pdf
  pdf-parse document.pdf -o output.csv       # Save first table to CSV
  pdf-parse document.pdf -f json            # Export as JSON
  pdf-parse document.pdf -p 1-3              # Parse only pages 1-3
        """
    )
    
    parser.add_argument(
        "pdf_file",
        type=str,
        help="Path to the PDF file to parse"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output file path (default: print to stdout)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["csv", "json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "-p", "--pages",
        type=str,
        help="Page range to parse (e.g., '1-3' or '5')"
    )
    
    parser.add_argument(
        "-t", "--table",
        type=int,
        default=1,
        help="Table number to export (default: 1)"
    )
    
    parser.add_argument(
        "--min-size",
        type=int,
        default=2,
        help="Minimum table size (rows/columns) (default: 2)"
    )
    
    parser.add_argument(
        "--no-merge-cells",
        action="store_true",
        help="Don't merge spanned cells"
    )
    
    parser.add_argument(
        "--preserve-formatting",
        action="store_true",
        help="Preserve original formatting"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: PDF file '{args.pdf_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Parse page range
    page_range = None
    if args.pages:
        try:
            if '-' in args.pages:
                start, end = map(int, args.pages.split('-'))
                page_range = (start, end)
            else:
                page_num = int(args.pages)
                page_range = (page_num, page_num)
        except ValueError:
            print(f"Error: Invalid page range '{args.pages}'", file=sys.stderr)
            sys.exit(1)
    
    # Create configuration
    config = ParseConfig(
        min_table_size=args.min_size,
        merge_cells=not args.no_merge_cells,
        preserve_formatting=args.preserve_formatting,
        page_range=page_range
    )
    
    try:
        # Parse PDF
        pdf_parser = PDFParser(config=config)
        tables = pdf_parser.parse_pdf(pdf_path)
        
        if not tables:
            print("No tables found in the PDF document", file=sys.stderr)
            sys.exit(1)
        
        if args.verbose:
            print(f"Found {len(tables)} table(s) in the PDF", file=sys.stderr)
        
        # Select table to export
        table_index = args.table - 1
        if table_index < 0 or table_index >= len(tables):
            print(f"Error: Table {args.table} not found. Available tables: 1-{len(tables)}", file=sys.stderr)
            sys.exit(1)
        
        selected_table = tables[table_index]
        
        # Export table
        if args.format == "csv":
            if args.output:
                selected_table.to_csv(args.output)
                if args.verbose:
                    print(f"Table exported to {args.output}", file=sys.stderr)
            else:
                # Print CSV to stdout
                import csv
                import io
                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(selected_table.columns)
                writer.writerows(selected_table.data)
                print(output.getvalue())
        
        elif args.format == "json":
            if args.output:
                selected_table.to_json(args.output)
                if args.verbose:
                    print(f"Table exported to {args.output}", file=sys.stderr)
            else:
                import json
                print(json.dumps(selected_table.to_dict(), indent=2))
        
        else:  # text format
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(selected_table.to_string())
                if args.verbose:
                    print(f"Table exported to {args.output}", file=sys.stderr)
            else:
                print(selected_table.to_string())
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()