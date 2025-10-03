"""
Advanced usage example for PDF Parse library.
"""

import json
from pdf_parse import PDFParser, ParseConfig


def main():
    """Demonstrate advanced PDF parsing functionality."""
    
    # Create custom configuration
    config = ParseConfig(
        min_table_size=3,  # Require at least 3 rows/columns
        merge_cells=True,  # Merge spanned cells
        preserve_formatting=False,  # Don't preserve formatting
        page_range=(1, 5),  # Only parse pages 1-5
        table_detection_threshold=0.7  # Higher sensitivity
    )
    
    parser = PDFParser(config=config)
    
    try:
        # Parse PDF with custom configuration
        tables = parser.parse_pdf('complex_document.pdf')
        
        print(f"Found {len(tables)} table(s) in pages 1-5")
        
        # Process each table
        for i, table in enumerate(tables):
            print(f"\n=== Table {i+1} ===")
            
            # Basic information
            print(f"Dimensions: {table.row_count} rows × {table.column_count} columns")
            print(f"Columns: {', '.join(table.columns)}")
            
            # Access specific data
            if table.row_count > 0:
                print(f"First row: {table.get_row(0)}")
                print(f"Last row: {table.get_row(table.row_count - 1)}")
            
            # Export in multiple formats
            base_filename = f"advanced_table_{i+1}"
            
            # CSV export
            table.to_csv(f"{base_filename}.csv")
            print(f"Exported CSV: {base_filename}.csv")
            
            # JSON export
            table.to_json(f"{base_filename}.json")
            print(f"Exported JSON: {base_filename}.json")
            
            # Dictionary access
            table_dict = table.to_dict()
            print(f"Table metadata: {json.dumps(table_dict, indent=2)}")
            
            # Access individual cells
            if table.row_count > 0 and table.column_count > 0:
                first_cell = table.get_cell(0, 0)
                print(f"First cell (0,0): '{first_cell}'")
            
            # Column access
            if table.column_count > 0:
                first_column = table.get_column(0)
                print(f"First column: {first_column[:3]}...")  # Show first 3 values
    
    except FileNotFoundError:
        print("Error: complex_document.pdf not found")
        print("Please provide a PDF file to parse")
    except Exception as e:
        print(f"Error parsing PDF: {e}")


if __name__ == "__main__":
    main()