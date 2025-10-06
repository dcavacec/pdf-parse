# PDF Analysis Tools - Complete Guide

This directory contains comprehensive tools to analyze PDF files and understand their structure before creating extraction rules.

## Tools Overview

### 1. `analyze_pdf_structure.py` - High-Level Analysis
**Purpose**: Quick overview of PDF structure and extraction capabilities
- File information (size, pages)
- PDF metadata (title, author, dates)
- Page-by-page analysis (text length, table likelihood)
- Extraction method testing (pdfplumber, tabula, camelot)
- Table analysis (total tables, column frequency)
- Recommendations for best extraction approach

### 2. `analyze_pdf_literal.py` - Detailed Structure Analysis
**Purpose**: Deep dive into PDF's literal structure and components
- Complete file metadata and PDF version
- Detailed page analysis (dimensions, rotation, boxes)
- Font analysis per page
- Image analysis per page
- Annotation analysis per page
- Form field analysis per page
- Document outline/bookmarks
- Complete table structure with data types
- Null value analysis

### 3. `analyze_pdf_json.py` - Structured JSON Output
**Purpose**: Machine-readable output for programmatic analysis
- Same analysis as `analyze_pdf_structure.py` but in JSON format
- Useful for batch processing and integration

## Usage Examples

### Quick Structure Analysis
```bash
# Display analysis in terminal
python analyze_pdf_structure.py "C:\path\to\file.pdf"

# Save to file
python analyze_pdf_structure.py "C:\path\to\file.pdf" --output analysis.txt
```

### Detailed Literal Structure Analysis
```bash
# Display detailed structure in terminal
python analyze_pdf_literal.py "C:\path\to\file.pdf"

# Save detailed analysis to file
python analyze_pdf_literal.py "C:\path\to\file.pdf" --output detailed_structure.txt
```

### JSON Output for Programming
```bash
# Display JSON in terminal
python analyze_pdf_json.py "C:\path\to\file.pdf"

# Save to JSON file
python analyze_pdf_json.py "C:\path\to\file.pdf" --output structure.json
```

## Sample Outputs

### High-Level Analysis Output
```
================================================================================
PDF STRUCTURE ANALYSIS: sample_tables.pdf
================================================================================

📄 FILE INFORMATION
----------------------------------------
Size: 3,456 bytes
Pages: 1

📋 PDF METADATA
----------------------------------------
Title: Sample PDF with Tabular Data
Creator: ReportLab PDF Library
Producer: ReportLab PDF Library - www.reportlab.com

📖 PAGE ANALYSIS
----------------------------------------
Page 1:
  Text length: 1,234 chars
  Table likelihood: high
  Potential table lines: 8
  Preview: Sample PDF with Tabular Data Sales Data by Quarter Product Q1 Sales...

🔧 EXTRACTION METHODS
----------------------------------------
✅ PDFPLUMBER:
   Tables found: 3
   Shapes: [(5, 6), (5, 6), (4, 5)]
   Sample columns: ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total']

❌ TABULA:
   Tables found: 0
   Error: `java` command is not found

✅ CAMELOT:
   Tables found: 3
   Shapes: [(6, 6), (6, 6), (5, 5)]
   Sample columns: ['0', '1', '2', '3', '4', '5']

💡 RECOMMENDATIONS
----------------------------------------
• Recommended extraction method: pdfplumber
• Common columns for rules: ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total']
• Pages with high table likelihood: [1]
```

### Detailed Literal Structure Output
```
====================================================================================================
PDF LITERAL STRUCTURE ANALYSIS: sample_tables.pdf
====================================================================================================

📄 FILE INFORMATION
--------------------------------------------------
Path: C:\path\to\sample_tables.pdf
Size: 3,456 bytes
PDF Version: b'%PDF-1.4'
Pages: 1
Encrypted: False

📋 PDF METADATA
--------------------------------------------------
Title: Sample PDF with Tabular Data
Creator: ReportLab PDF Library
Producer: ReportLab PDF Library - www.reportlab.com

📖 PAGE-BY-PAGE ANALYSIS
--------------------------------------------------

Page 1:
  Rotation: 0°
  Media Box: 612.0 x 792.0
  Text Length: 1,234 characters
  Has Text: True
  Text Preview: Sample PDF with Tabular Data Sales Data by Quarter Product Q1 Sales Q2 Sales Q3 Sales Q4 Sales Total Widget A $1,200 $1,500 $1,800 $2,100 $6,600 Widget B $800 $950 $1,200 $1,400 $4,350 Widget C $2,100 $2,300 $2,500 $2,800 $9,700 Widget D $1,500 $1,600 $1,700 $1,900 $6,700 Total $5,600 $6,350 $7,200 $8,200 $27,350 Employee Information Employee ID Name Department Position Salary Start Date EMP001 John Smith Engineering Senior Developer $85,000 2020-01-15 EMP002 Jane Doe Marketing Marketing Manager $75,000 2019-03-22 EMP003 Bob Johnson Sales Sales Representative $60,000 2021-06-10 EMP004 Alice Brown HR HR Specialist $65,000 2020-09-05 EMP005 Charlie Wilson Engineering Junior Developer $55,000 2022-02-14 Financial Summary Metric 2021 2022 2023 Change (%) Revenue $2.5M $3.2M $4.1M +28.1% Expenses $1.8M $2.1M $2.6M +23.8% Net Profit $700K $1.1M $1.5M +36.4% ROI 28.0% 34.4% 36.6% +6.4%...
  Fonts (2):
    - Helvetica-Bold (Type1)
    - Helvetica (Type1)

📊 TABLE STRUCTURE ANALYSIS
--------------------------------------------------
Total Tables: 6
Unique Columns: 12
Column Frequency:
  Product: 2 tables
  Q1 Sales: 2 tables
  Q2 Sales: 2 tables
  Q3 Sales: 2 tables
  Q4 Sales: 2 tables
  Total: 2 tables
  Employee ID: 2 tables
  Name: 2 tables
  Department: 2 tables
  Position: 2 tables
  Salary: 2 tables
  Start Date: 2 tables

Tables on Page 1:
  Table 1:
    Shape: (5, 6)
    Columns: ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total']
    Data Types: {'Product': 'object', 'Q1 Sales': 'object', 'Q2 Sales': 'object', 'Q3 Sales': 'object', 'Q4 Sales': 'object', 'Total': 'object'}
    Has Nulls: False

🏗️ STRUCTURE SUMMARY
--------------------------------------------------
Total Pages: 1
Total Fonts: 2
Total Images: 0
Total Annotations: 0
Total Form Fields: 0
Total Tables: 6
```

## Integration with Rules Creation

### 1. Column Selection Rules
Use `column_frequency` data to create targeted field selection:
```yaml
transforms:
  - op: select_fields
    fields: ["Product", "Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales", "Total"]
    allow_missing: false
```

### 2. Method Selection
Use `extraction_methods` results to set optimal extraction:
```yaml
selection:
  method: pdfplumber  # Based on analysis showing best results
```

### 3. Page Targeting
Use `page_analysis` to target specific pages:
```yaml
selection:
  pages: [1]  # Pages with high table likelihood
```

### 4. Header Matching
Use `sample_columns` for header-based selection:
```yaml
extraction:
  header_contains: ["Product", "Q1", "Q2", "Q3", "Q4", "Total"]
  min_match: 0.6
```

### 5. Data Type Casting
Use `data_types` information for proper type conversion:
```yaml
transforms:
  - op: cast_columns
    types:
      "Q1 Sales": number
      "Q2 Sales": number
      "Q3 Sales": number
      "Q4 Sales": number
      "Total": number
```

## Error Handling

The tools include robust error handling for common issues:

- **Permission Errors**: Fixed camelot temp file issues by using `flavor='lattice'`
- **Missing Dependencies**: Graceful handling of missing Java (tabula) or Ghostscript (camelot)
- **Corrupted PDFs**: Safe extraction with fallback methods
- **Large Files**: Memory-efficient processing for large PDFs

## Use Cases

1. **Pre-Analysis**: Understand PDF structure before creating extraction rules
2. **Rule Optimization**: Use analysis data to create more targeted rules
3. **Debugging**: Identify why certain extraction methods fail
4. **Batch Processing**: Analyze multiple PDFs to find common patterns
5. **Documentation**: Generate structure documentation for PDF collections
6. **Quality Assurance**: Verify PDF structure meets expectations

## Performance Notes

- **High-Level Analysis**: Fast, suitable for quick overviews
- **Literal Structure Analysis**: More detailed but slower, use for deep analysis
- **JSON Output**: Fastest for programmatic processing
- **Memory Usage**: Efficient processing even for large PDFs
- **Error Recovery**: Continues processing even if some methods fail