"""
Basic usage example for PDF Parse library.
"""

from pdf_parse import PDFParser, ParseConfig


def main():
    """Demonstrate basic PDF parsing functionality."""
    
    # Initialize parser with default configuration
    parser = PDFParser()
    
    # Example: Parse a PDF file
    try:
        tables = parser.parse_pdf('sample_document.pdf')
        
        print(f"Found {len(tables)} table(s) in the PDF")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(f"  Rows: {table.row_count}")
            print(f"  Columns: {table.column_count}")
            print(f"  Columns: {table.columns}")
            
            # Display first few rows
            print("\nFirst 3 rows:")
            for j, row in enumerate(table.data[:3]):
                print(f"  Row {j+1}: {row}")
            
            # Export to CSV
            csv_filename = f"table_{i+1}.csv"
            table.to_csv(csv_filename)
            print(f"  Exported to {csv_filename}")
    
    except FileNotFoundError:
        print("Error: sample_document.pdf not found")
        print("Please provide a PDF file to parse")
    except Exception as e:
        print(f"Error parsing PDF: {e}")


if __name__ == "__main__":
    main()