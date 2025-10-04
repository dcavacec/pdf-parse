# Multi-PDF Parsing and Selective Saving Features

## Overview

This branch implements comprehensive multi-PDF parsing capabilities with selective table saving functionality. Users can now process multiple PDF files at once and choose which tables to save, significantly improving workflow efficiency.

## 🚀 New Features

### 1. Multiple File Upload Options
- **Single PDF File**: Traditional single file upload
- **Multiple PDF Files**: Select multiple PDF files at once
- **Directory Selection**: Choose an entire directory containing PDF files

### 2. Batch Processing
- Process multiple PDFs simultaneously
- Individual file processing status tracking
- Error handling for problematic files
- Comprehensive processing summary

### 3. Selective Table Saving
- **Interactive Table Selection**: Checkbox interface to choose which tables to download
- **Select All/Deselect All**: Quick selection controls
- **Table Preview**: See table dimensions and column information
- **File Attribution**: Know which file each table came from

### 4. Enhanced Download Options
- **Excel Format**: Download selected tables as Excel workbook with multiple sheets
- **CSV Format**: Download selected tables as ZIP archive containing individual CSV files
- **Individual Downloads**: Download single tables as CSV files

## 🛠️ Technical Implementation

### Frontend Changes

#### Flask Application (`simple_frontend.py`)
- New `/upload_multiple` endpoint for handling multiple file uploads
- New `/download_selected` endpoint for selective table downloads
- Enhanced error handling and file processing status
- Support for directory uploads via webkitdirectory API

#### Streamlit Application (`app.py`)
- Radio button selection for upload type (single vs multiple)
- Multiple file uploader with `accept_multiple_files=True`
- Session state management for table selection
- Interactive checkbox interface for table selection
- Enhanced download buttons for selected tables

#### HTML Template (`templates/index.html`)
- Radio button interface for upload type selection
- Dynamic form switching based on upload type
- Enhanced CSS for table selection interface
- JavaScript functions for table selection and download management
- File input handlers for different upload types

### Backend Changes

#### Multi-File Processing
```python
# Process multiple PDF files
for file in pdf_files:
    file_tables = extractor.extract_tables_from_pdf(file_path, method, pages)
    # Add file attribution to each table
    for table in file_tables:
        table.file_name = file.filename
```

#### Selective Download
```python
# Download selected tables in specified format
selected_tables = [tables[i] for i in selected_indices]
if format_type == 'excel':
    # Create Excel workbook
elif format_type == 'csv':
    # Create ZIP archive
```

## 📋 User Interface Enhancements

### Upload Interface
- **Upload Type Selection**: Radio buttons for single/multiple/directory
- **Dynamic File Inputs**: Different input types based on selection
- **File Count Display**: Shows number of files selected
- **Directory Support**: Webkitdirectory API for folder selection

### Results Interface
- **Processing Summary**: Files processed, tables found, total rows/columns
- **File Status**: Individual file processing results
- **Table Selection Panel**: Checkbox interface with select all/none
- **Download Controls**: Excel and CSV download buttons
- **Table Preview**: Limited preview of each table with file attribution

## 🎯 Usage Examples

### Single PDF Processing
1. Select "Single PDF File" option
2. Choose a PDF file
3. Configure extraction settings
4. Click "Extract Tables"
5. Select desired tables using checkboxes
6. Download selected tables

### Multiple PDF Processing
1. Select "Multiple PDF Files" option
2. Choose multiple PDF files
3. Configure extraction settings
4. Click "Extract Tables"
5. Review processing summary
6. Select tables from all files
7. Download selected tables

### Directory Processing
1. Select "Directory of PDFs" option
2. Choose a directory containing PDF files
3. Configure extraction settings
4. Click "Extract Tables"
5. Review processing summary for all files
6. Select tables from all processed files
7. Download selected tables

## 🔧 Configuration Options

### Extraction Settings
- **Method**: Auto, PDFPlumber, Tabula, Camelot
- **Pages**: All pages or specific page numbers
- **File Processing**: Individual error handling

### Download Settings
- **Format**: Excel (.xlsx) or CSV (ZIP)
- **Selection**: Individual table selection
- **Naming**: Automatic file naming with table numbers

## 🧪 Testing

Both applications have been tested and are running successfully:

- **Flask App**: http://localhost:5000
- **Streamlit App**: http://localhost:8501

### Test Results
✅ Multiple file upload functionality
✅ Directory selection capability
✅ Batch processing with error handling
✅ Selective table saving interface
✅ Excel and CSV download formats
✅ File attribution and processing summary
✅ Enhanced UI with responsive design

## 📁 File Structure

```
/workspace/
├── simple_frontend.py          # Flask application with multi-PDF support
├── app.py                      # Streamlit application with multi-PDF support
├── templates/
│   └── index.html             # Enhanced HTML template with selection UI
├── pdf_table_extractor.py     # Core PDF extraction functionality
├── test_multi_pdf.py         # Test script for new features
└── MULTI_PDF_FEATURES.md     # This documentation
```

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Flask Application**:
   ```bash
   python3 simple_frontend.py
   ```
   Access at: http://localhost:5000

3. **Run Streamlit Application**:
   ```bash
   python3 -m streamlit run app.py --server.port 8501
   ```
   Access at: http://localhost:8501

4. **Test Functionality**:
   ```bash
   python3 test_multi_pdf.py
   ```

## 🎉 Benefits

- **Efficiency**: Process multiple PDFs in one operation
- **Flexibility**: Choose which tables to save
- **User Experience**: Intuitive interface with clear feedback
- **Scalability**: Handle large batches of PDF files
- **Error Resilience**: Continue processing even if some files fail
- **Format Options**: Multiple download formats for different use cases

The implementation provides a comprehensive solution for batch PDF table extraction with selective saving capabilities, significantly improving the user experience and workflow efficiency.