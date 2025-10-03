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
    print(f"Found table with {len(first_table.rows)} rows and {len(first_table.columns)} columns")
    
    # Convert to CSV
    first_table.to_csv('output.csv')
    
    # Convert to JSON
    import json
    print(json.dumps(first_table.to_dict(), indent=2))
```

## Usage Examples

### Basic Table Extraction

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

```python
from pdf_parse import PDFParser, ParseConfig

# Configure parsing options
config = ParseConfig(
    min_table_size=3,  # Minimum rows/columns for a valid table
    merge_cells=True,  # Merge spanned cells
    preserve_formatting=True  # Keep original formatting
)

parser = PDFParser(config=config)
tables = parser.parse_pdf('complex_document.pdf')
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

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=pdf_parse

# Run specific test file
python -m pytest tests/test_parser.py
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyPDF2](https://github.com/py-pdf/PyPDF2) for PDF processing
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
