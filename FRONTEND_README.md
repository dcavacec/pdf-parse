# PDF Table Extractor - Frontend Options

This project now includes **two front-end options** for extracting tables from PDF documents:

## 🚀 Option 1: Streamlit Web App (Advanced)

**File:** `app.py`  
**Features:**
- Full-featured web interface with modern UI
- Multiple extraction methods (auto, pdfplumber, tabula, camelot)
- Page selection options
- Table preview and download capabilities
- Excel and CSV export options
- Error handling and troubleshooting tips
- Custom CSS styling

**To run:**
```bash
python3 -m streamlit run app.py --server.headless true --server.port 8501
```

**Access:** http://localhost:8501

## 🌐 Option 2: Simple HTML Frontend (Lightweight)

**File:** `simple_frontend.py`  
**Features:**
- Clean, responsive HTML interface
- Flask-based backend
- File upload with drag-and-drop
- Real-time table extraction
- Modern CSS styling with gradients
- Mobile-friendly design
- JSON API for table data

**To run:**
```bash
python3 simple_frontend.py
```

**Access:** http://localhost:5000

## 📋 Comparison

| Feature | Streamlit App | Simple HTML |
|---------|---------------|-------------|
| **Complexity** | Advanced | Simple |
| **Dependencies** | Streamlit + all PDF libs | Flask + all PDF libs |
| **UI Framework** | Streamlit components | Custom HTML/CSS/JS |
| **File Downloads** | ✅ Full support | ⚠️ Placeholder |
| **Mobile Support** | ✅ Good | ✅ Excellent |
| **Customization** | Limited | Full control |
| **Performance** | Good | Excellent |
| **Setup** | Easy | Easy |

## 🎯 Which Should You Use?

### Use Streamlit App (`app.py`) if you want:
- Full-featured interface with all bells and whistles
- Built-in download functionality
- Minimal customization needed
- Quick setup and deployment

### Use Simple HTML Frontend (`simple_frontend.py`) if you want:
- Lightweight, fast interface
- Full control over styling and behavior
- Custom JavaScript functionality
- Better mobile experience
- Minimal dependencies

## 🛠️ Command Line Interface

Both front-ends are backed by the same powerful CLI tool:

```bash
# Basic extraction
python3 cli.py sample_tables.pdf

# Extract from specific pages
python3 cli.py sample_tables.pdf --pages 1,3,5

# Use specific method
python3 cli.py sample_tables.pdf --method tabula

# Save to Excel
python3 cli.py sample_tables.pdf --output tables.xlsx

# Get summary
python3 cli.py sample_tables.pdf --summary --verbose
```

## 📁 Project Structure

```
/workspace/
├── app.py                 # Streamlit frontend
├── simple_frontend.py     # Flask frontend
├── templates/
│   └── index.html        # HTML template for Flask app
├── cli.py                # Command line interface
├── pdf_table_extractor.py # Core extraction logic
├── sample_tables.pdf     # Sample PDF for testing
└── requirements.txt      # Dependencies
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Choose your frontend:**
   
   **For Streamlit:**
   ```bash
   python3 -m streamlit run app.py
   ```
   
   **For Simple HTML:**
   ```bash
   python3 simple_frontend.py
   ```

3. **Upload a PDF** and extract tables!

## 🧪 Testing

Test with the included sample PDF:
```bash
python3 cli.py sample_tables.pdf --summary --verbose
```

This will extract 6 tables from the sample PDF and show detailed information about each table.

## 📝 Notes

- Both front-ends use the same underlying `PDFTableExtractor` class
- The Streamlit app has more features but is heavier
- The simple HTML frontend is more customizable and lightweight
- Both support all extraction methods (auto, pdfplumber, tabula, camelot)
- The CLI tool provides the most direct access to functionality

Choose the frontend that best fits your needs! 🎉