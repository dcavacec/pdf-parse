# PDF Parse

A Python library for extracting and parsing tabular data from PDF documents.

## Description

PDF Parse is a powerful tool designed to extract structured tabular data from PDF files. Whether you're working with financial reports, data tables, or any document containing tabular information, this library provides an easy-to-use interface for parsing and extracting the data you need.

## Features

- **Tabular Data Extraction**: Extract tables from PDF documents with high accuracy
- **Multiple Output Formats**: Export parsed data to CSV, JSON, or Python data structures
- **Flexible Parsing**: Handle various table formats and layouts
- **Easy Integration**: Simple API for quick integration into your projects
- **Robust Error Handling**: Graceful handling of malformed or complex PDF structures

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pdf-parse.git
cd pdf-parse

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install .
```

### Install with pip (when available on PyPI)

```bash
pip install pdf-parse
```

## Quick Start

```python
from pdf_parse import PDFParser

# Initialize the parser
parser = PDFParser()

# Parse a PDF file
tables = parser.parse_pdf('document.pdf')

# Access the first table
if tables:
    first_table = tables[0]
    print(f"Found table with {first_table.row_count} rows and {first_table.column_count} columns")
    
    # Convert to CSV
    first_table.to_csv('output.csv')
    
    # Convert to JSON
    import json
    print(json.dumps(first_table.to_dict(), indent=2))
```

## Usage Examples

### Basic Table Extraction

See `examples/basic_usage.py` for a complete example:

```python
from pdf_parse import PDFParser

parser = PDFParser()
tables = parser.parse_pdf('financial_report.pdf')

for i, table in enumerate(tables):
    print(f"Table {i+1}:")
    print(table.to_string())
    print("-" * 50)
```

### Advanced Configuration

See `examples/advanced_usage.py` for advanced usage:

```python
from pdf_parse import PDFParser, ParseConfig

# Configure parsing options
config = ParseConfig(
    min_table_size=3,  # Minimum rows/columns for a valid table
    merge_cells=True,  # Merge spanned cells
    preserve_formatting=True,  # Keep original formatting
    page_range=(1, 5)  # Parse only pages 1-5
)

parser = PDFParser(config=config)
tables = parser.parse_pdf('complex_document.pdf')
```

### Command Line Interface

PDF Parse also includes a command-line interface:

```bash
# Extract tables from a PDF
pdf-parse document.pdf

# Export to CSV
pdf-parse document.pdf -o output.csv -f csv

# Parse specific pages
pdf-parse document.pdf -p 1-3

# Export specific table
pdf-parse document.pdf -t 2 -f json -o table2.json
```

### Batch Processing

```python
import os
from pdf_parse import PDFParser

parser = PDFParser()
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

for pdf_file in pdf_files:
    print(f"Processing {pdf_file}...")
    tables = parser.parse_pdf(pdf_file)
    
    # Save each table to a separate CSV file
    for i, table in enumerate(tables):
        output_file = f"{pdf_file}_table_{i+1}.csv"
        table.to_csv(output_file)
        print(f"  Saved table {i+1} to {output_file}")
```

## API Reference

### PDFParser

Main class for parsing PDF documents.

#### Methods

- `parse_pdf(file_path: str) -> List[Table]`: Parse a PDF file and return a list of extracted tables
- `parse_pdf_from_bytes(pdf_bytes: bytes) -> List[Table]`: Parse PDF from byte data

### Table

Represents an extracted table from a PDF.

#### Properties

- `rows`: List of table rows
- `columns`: List of column names
- `data`: 2D list of table data

#### Methods

- `to_csv(file_path: str)`: Export table to CSV file
- `to_json(file_path: str)`: Export table to JSON file
- `to_dict() -> dict`: Convert table to dictionary
- `to_string() -> str`: Convert table to formatted string

### ParseConfig

Configuration options for PDF parsing.

#### Parameters

- `min_table_size`: Minimum number of rows/columns for a valid table
- `merge_cells`: Whether to merge spanned cells
- `preserve_formatting`: Whether to preserve original formatting
- `encoding`: Text encoding for output

## Contributing

We welcome contributions to PDF Parse! Here's how you can help:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/pdf-parse.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install in development mode: `pip install -e .`

### Running Examples

```bash
# Run basic usage example
python examples/basic_usage.py

# Run advanced usage example  
python examples/advanced_usage.py
```

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Run tests: `python -m pytest`
5. Run linting: `python -m flake8`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

### Reporting Issues

If you find a bug or have a feature request, please:

1. Check existing issues first
2. Create a new issue with a clear description
3. Include sample PDF files if reporting parsing issues
4. Provide Python version and operating system information

## Project Structure

```
pdf-parse/
├── pdf_parse/           # Main package
│   ├── __init__.py      # Package initialization
│   ├── parser.py         # Main PDFParser class
│   ├── table.py          # Table class for data representation
│   ├── config.py         # ParseConfig class for options
│   └── cli.py            # Command-line interface
├── tests/               # Test suite
│   ├── test_parser.py    # Tests for PDFParser
│   └── test_table.py     # Tests for Table class
├── examples/            # Usage examples
│   ├── basic_usage.py    # Basic usage example
│   └── advanced_usage.py  # Advanced usage example
├── requirements.txt      # Python dependencies
├── setup.py             # Package installation script
├── README.md            # This file
└── LICENSE              # GPL v3.0 license
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=pdf_parse

# Run specific test file
python -m pytest tests/test_parser.py

# Run tests with verbose output
python -m pytest -v
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [pypdf](https://github.com/py-pdf/pypdf) for PDF processing
- Inspired by the need for reliable PDF table extraction
- Thanks to all contributors who help improve this project

## Support

- 📖 [Documentation](https://github.com/yourusername/pdf-parse/wiki)
- 🐛 [Issue Tracker](https://github.com/yourusername/pdf-parse/issues)
- 💬 [Discussions](https://github.com/yourusername/pdf-parse/discussions)

## Changelog

### Version 1.0.0 (Planned)
- Initial release
- Basic table extraction functionality
- CSV and JSON export
- Configurable parsing options
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
