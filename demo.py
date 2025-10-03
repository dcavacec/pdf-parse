"""
Quick demo of the PDF Table Extractor
"""

from pdf_table_extractor import PDFTableExtractor
import pandas as pd

def main():
    print("🚀 PDF Table Extractor Demo")
    print("=" * 50)
    
    # Initialize extractor
    extractor = PDFTableExtractor()
    
    # Extract tables from sample PDF
    print("📄 Extracting tables from sample_tables.pdf...")
    tables = extractor.extract_tables_from_pdf("sample_tables.pdf", method='pdfplumber')
    
    if tables:
        print(f"✅ Successfully extracted {len(tables)} tables!")
        
        # Show first table
        print("\n📊 First table preview:")
        print(tables[0].head())
        
        # Show summary
        summary = extractor.get_table_summary(tables)
        print(f"\n📈 Summary:")
        print(f"Total tables: {summary['total_tables']}")
        
        for i, table_info in enumerate(summary['tables_info'][:3]):  # Show first 3
            print(f"Table {i+1}: {table_info['shape'][0]} rows × {table_info['shape'][1]} columns")
        
        print(f"\n💾 Files created:")
        print("- sample_tables_tables.xlsx (Excel file)")
        print("- sample_tables_tables/ (CSV files)")
        
        print(f"\n🌐 To run the web interface:")
        print("streamlit run app.py")
        
        print(f"\n💻 To use command line:")
        print("python3 cli.py --help")
        
    else:
        print("❌ No tables found!")

if __name__ == "__main__":
    main()