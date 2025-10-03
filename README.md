# PDF Table Extractor 📊

A comprehensive tool for extracting tabular data from PDF documents and loading into pandas DataFrames. This application provides multiple extraction methods, a user-friendly web interface, and command-line tools for processing PDF files containing tables.

## Features ✨

- **Multiple Extraction Methods**: Supports pdfplumber, tabula-py, and camelot-py
- **Auto Mode**: Automatically tries multiple methods for best results
- **Web Interface**: User-friendly Streamlit application
- **Command Line Interface**: CLI tool for batch processing
- **Flexible Output**: Save to Excel, CSV, or work directly with DataFrames
- **Page Selection**: Extract from specific pages or all pages
- **Error Handling**: Robust error handling and validation
- **Table Cleaning**: Automatic cleaning and standardization of extracted data

## Installation 🚀

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **For camelot-py (optional but recommended)**:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install python3-tk ghostscript
   
   # On macOS
   brew install ghostscript
   
   # On Windows
   # Download and install Ghostscript from https://www.ghostscript.com/
   ```

## Quick Start 🏃‍♂️

### 1. Web Interface (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` and upload a PDF file.

### 2. Command Line Interface

```bash
# Extract all tables from a PDF
python cli.py input.pdf

# Extract from specific pages
python cli.py input.pdf --pages 1,3,5

# Use specific extraction method
python cli.py input.pdf --method tabula

# Save to Excel file
python cli.py input.pdf --output tables.xlsx
```

### 3. Python API

```python
from pdf_table_extractor import PDFTableExtractor

# Initialize extractor
extractor = PDFTableExtractor()

# Extract tables
tables = extractor.extract_tables_from_pdf('input.pdf', method='auto')

# Work with DataFrames
for i, table in enumerate(tables):
    print(f"Table {i+1}: {table.shape}")
    print(table.head())
```

## Usage Examples 📚

### Basic Usage

```python
from pdf_table_extractor import PDFTableExtractor

extractor = PDFTableExtractor()
tables = extractor.extract_tables_from_pdf('document.pdf')

# Save to Excel
extractor.save_tables_to_excel(tables, 'output.xlsx')

# Save to CSV files
extractor.save_tables_to_csv(tables, 'output_directory/')
```

### Advanced Usage

```python
# Extract from specific pages
tables = extractor.extract_tables_from_pdf(
    'document.pdf', 
    method='tabula',
    pages=[1, 3, 5]
)

# Get summary information
summary = extractor.get_table_summary(tables)
print(f"Total tables: {summary['total_tables']}")
```

### Command Line Examples

```bash
# Basic extraction
python cli.py document.pdf

# Extract from specific pages with verbose output
python cli.py document.pdf --pages 1,2,3 --verbose

# Use specific method and save to Excel
python cli.py document.pdf --method pdfplumber --output results.xlsx

# Get summary information
python cli.py document.pdf --summary
```

## Extraction Methods 🔧

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Auto** | General use | Tries multiple methods | Slower |
| **PDFPlumber** | Simple tables | Fast, good for basic tables | Limited complex table support |
| **Tabula** | Complex tables | Excellent table detection | Requires Java |
| **Camelot** | High-quality PDFs | Very accurate | Slower, requires Ghostscript |

## File Formats 📁

### Input
- PDF files (`.pdf`)

### Output
- Excel files (`.xlsx`) - Multiple sheets
- CSV files (`.csv`) - Individual files
- ZIP archives - Multiple CSV files
- Pandas DataFrames - Direct Python objects

## Testing 🧪

Create a sample PDF for testing:

```bash
python create_sample_pdf.py
```

Run example usage:

```bash
python example_usage.py
```

## Troubleshooting 🔧

### Common Issues

1. **No tables found**
   - Try different extraction methods
   - Check if PDF contains actual tabular data
   - Ensure PDF is not password-protected

2. **Installation issues**
   - Install Java for tabula-py
   - Install Ghostscript for camelot-py
   - Check Python version compatibility

3. **Memory issues with large PDFs**
   - Extract from specific pages
   - Use pdfplumber method for large files

### Error Messages

- `FileNotFoundError`: Check PDF file path
- `No tables found`: Try different extraction method
- `Java not found`: Install Java for tabula-py
- `Ghostscript not found`: Install Ghostscript for camelot-py

## API Reference 📖

### PDFTableExtractor Class

#### Methods

- `extract_tables_from_pdf(pdf_path, method='auto', pages=None)`: Extract tables from PDF
- `save_tables_to_excel(tables, output_path)`: Save tables to Excel file
- `save_tables_to_csv(tables, output_dir)`: Save tables to CSV files
- `get_table_summary(tables)`: Get summary information about tables

#### Parameters

- `pdf_path`: Path to PDF file (str or Path)
- `method`: Extraction method ('auto', 'pdfplumber', 'tabula', 'camelot')
- `pages`: Page numbers to extract from (int, list, or None for all)

## Contributing 🤝

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Dependencies 📦

- pandas >= 1.5.0
- PyPDF2 >= 3.0.0
- pdfplumber >= 0.9.0
- tabula-py >= 2.5.0
- camelot-py[cv] >= 0.10.1
- openpyxl >= 3.0.0
- streamlit >= 1.25.0
- numpy >= 1.24.0

## Support 💬

If you encounter any issues or have questions, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Happy table extracting! 🎉**
