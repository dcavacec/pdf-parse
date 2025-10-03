"""
Example usage of the PDF Table Extractor
"""

from pdf_table_extractor import PDFTableExtractor
import pandas as pd


def example_basic_usage():
    """Basic example of extracting tables from a PDF."""
    print("=== Basic Usage Example ===")
    
    # Initialize the extractor
    extractor = PDFTableExtractor()
    
    # Extract tables from PDF (replace with your PDF path)
    pdf_path = "sample_tables.pdf"  # Use the sample PDF we created
    
    try:
        # Extract tables using auto method (tries multiple extraction methods)
        tables = extractor.extract_tables_from_pdf(pdf_path, method='auto')
        
        if tables:
            print(f"Successfully extracted {len(tables)} tables")
            
            # Display each table
            for i, table in enumerate(tables):
                print(f"\nTable {i+1}:")
                print(f"Shape: {table.shape}")
                print(f"Columns: {list(table.columns)}")
                print("First few rows:")
                print(table.head())
                print("-" * 50)
        else:
            print("No tables found in the PDF")
            
    except FileNotFoundError:
        print("Sample PDF not found. Run 'python create_sample_pdf.py' first to create a test PDF.")
    except Exception as e:
        print(f"Error: {str(e)}")


def example_specific_method():
    """Example using a specific extraction method."""
    print("\n=== Specific Method Example ===")
    
    extractor = PDFTableExtractor()
    pdf_path = "sample_tables.pdf"
    
    # Try different extraction methods
    methods = ['pdfplumber', 'tabula', 'camelot']
    
    for method in methods:
        try:
            print(f"\nTrying {method} method:")
            tables = extractor.extract_tables_from_pdf(pdf_path, method=method)
            
            if tables:
                print(f"  Found {len(tables)} tables")
                for i, table in enumerate(tables):
                    print(f"  Table {i+1}: {table.shape}")
            else:
                print("  No tables found")
                
        except Exception as e:
            print(f"  Error with {method}: {str(e)}")


def example_specific_pages():
    """Example extracting from specific pages."""
    print("\n=== Specific Pages Example ===")
    
    extractor = PDFTableExtractor()
    pdf_path = "sample_tables.pdf"
    
    try:
        # Extract from first page only
        tables_page_1 = extractor.extract_tables_from_pdf(pdf_path, pages=1)
        print(f"Tables from page 1: {len(tables_page_1)}")
        
        # Extract from multiple specific pages
        tables_multiple = extractor.extract_tables_from_pdf(pdf_path, pages=[1, 2])
        print(f"Tables from pages 1 and 2: {len(tables_multiple)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


def example_save_outputs():
    """Example of saving extracted tables to different formats."""
    print("\n=== Save Outputs Example ===")
    
    extractor = PDFTableExtractor()
    pdf_path = "sample_tables.pdf"
    
    try:
        tables = extractor.extract_tables_from_pdf(pdf_path)
        
        if tables:
            # Save to Excel file
            extractor.save_tables_to_excel(tables, "example_output.xlsx")
            print("Saved tables to Excel file: example_output.xlsx")
            
            # Save to CSV files
            extractor.save_tables_to_csv(tables, "example_csv_output")
            print("Saved tables to CSV files in: example_csv_output/")
            
            # Get summary information
            summary = extractor.get_table_summary(tables)
            print(f"\nSummary:")
            print(f"Total tables: {summary['total_tables']}")
            
            for table_info in summary['tables_info']:
                print(f"Table {table_info['table_number']}: {table_info['shape']}")
                
    except Exception as e:
        print(f"Error: {str(e)}")


def example_dataframe_operations():
    """Example of working with extracted DataFrames."""
    print("\n=== DataFrame Operations Example ===")
    
    extractor = PDFTableExtractor()
    pdf_path = "sample_tables.pdf"
    
    try:
        tables = extractor.extract_tables_from_pdf(pdf_path)
        
        if tables:
            # Work with the first table
            first_table = tables[0]
            print(f"Working with first table: {first_table.shape}")
            
            # Basic DataFrame operations
            print(f"Column names: {list(first_table.columns)}")
            print(f"Data types:\n{first_table.dtypes}")
            
            # Filter data (example: find rows with specific values)
            if 'Product' in first_table.columns:
                widget_a_rows = first_table[first_table['Product'].str.contains('Widget A', na=False)]
                print(f"\nRows containing 'Widget A': {len(widget_a_rows)}")
                print(widget_a_rows)
            
            # Calculate statistics if numeric columns exist
            numeric_cols = first_table.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                print(f"\nNumeric columns: {list(numeric_cols)}")
                print("Summary statistics:")
                print(first_table[numeric_cols].describe())
            
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    """Run all examples."""
    print("PDF Table Extractor - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_specific_method()
    example_specific_pages()
    example_save_outputs()
    example_dataframe_operations()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo run the web interface: streamlit run app.py")
    print("To use command line: python cli.py --help")


if __name__ == "__main__":
    main()