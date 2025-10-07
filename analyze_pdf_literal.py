"""
PDF Literal Structure Analyzer
Analyzes a PDF file and outputs its literal structure with proper syntax.

Usage:
    python analyze_pdf_literal.py "C:\\path\\to\\file.pdf"
    python analyze_pdf_literal.py "C:\\path\\to\\file.pdf" --output structure.txt
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict, List, Any
import json

from pypdf import PdfReader
from pdf_table_extractor import PDFTableExtractor
from java_check import JAVA_AVAILABLE, JAVA_VERSION


def analyze_pdf_literal_structure(pdf_path: Path) -> Dict[str, Any]:
    """Analyze PDF literal structure and return detailed metadata."""
    reader = PdfReader(str(pdf_path))
    
    structure = {
        "file_path": str(pdf_path),
        "file_name": pdf_path.name,
        "file_size_bytes": pdf_path.stat().st_size,
        "pdf_version": reader.pdf_header,
        "pages_count": len(reader.pages),
        "is_encrypted": reader.is_encrypted,
        "metadata": {},
        "pages": [],
        "outline": [],
        "forms": [],
        "annotations": [],
        "fonts": [],
        "images": [],
        "structure_elements": {}
    }
    
    # Extract PDF metadata
    if reader.metadata:
        structure["metadata"] = {
            "title": str(reader.metadata.get("/Title", "")),
            "author": str(reader.metadata.get("/Author", "")),
            "subject": str(reader.metadata.get("/Subject", "")),
            "creator": str(reader.metadata.get("/Creator", "")),
            "producer": str(reader.metadata.get("/Producer", "")),
            "creation_date": str(reader.metadata.get("/CreationDate", "")),
            "modification_date": str(reader.metadata.get("/ModDate", "")),
            "keywords": str(reader.metadata.get("/Keywords", "")),
            "trapped": str(reader.metadata.get("/Trapped", ""))
        }
    
    # Analyze each page in detail
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Safely extract mediabox information
        mediabox_info = {}
        try:
            if hasattr(page, 'mediabox') and page.mediabox:
                # mediabox is an array [x0, y0, x1, y1]
                coords = [float(x) for x in page.mediabox]
                mediabox_info = {
                    "x0": coords[0],
                    "y0": coords[1], 
                    "x1": coords[2],
                    "y1": coords[3],
                    "width": coords[2] - coords[0],
                    "height": coords[3] - coords[1]
                }
        except Exception:
            mediabox_info = {"error": "Could not extract mediabox"}
        
        # Safely extract cropbox information
        cropbox_info = None
        try:
            if hasattr(page, 'cropbox') and page.cropbox:
                # cropbox is an array [x0, y0, x1, y1]
                coords = [float(x) for x in page.cropbox]
                cropbox_info = {
                    "x0": coords[0],
                    "y0": coords[1],
                    "x1": coords[2], 
                    "y1": coords[3],
                    "width": coords[2] - coords[0],
                    "height": coords[3] - coords[1]
                }
        except Exception:
            cropbox_info = {"error": "Could not extract cropbox"}
        
        page_info = {
            "page_number": page_num + 1,
            "rotation": page.rotation,
            "mediabox": mediabox_info,
            "cropbox": cropbox_info,
            "text_content": {
                "raw_text": page.extract_text(),
                "text_length": len(page.extract_text()),
                "has_text": len(page.extract_text().strip()) > 0
            },
            "fonts": [],
            "images": [],
            "annotations": [],
            "form_fields": []
        }
        
        # Extract fonts used on this page
        try:
            if hasattr(page, 'get_fonts'):
                fonts = page.get_fonts()
                for font in fonts:
                    page_info["fonts"].append({
                        "name": font[0] if len(font) > 0 else "unknown",
                        "type": font[1] if len(font) > 1 else "unknown",
                        "encoding": font[2] if len(font) > 2 else "unknown"
                    })
        except Exception:
            pass
        
        # Extract images on this page
        try:
            if hasattr(page, 'images'):
                for img in page.images:
                    # Handle image properties safely
                    img_info = {
                        "name": "unknown",
                        "width": 0,
                        "height": 0,
                        "colorspace": "unknown"
                    }
                    
                    try:
                        if hasattr(img, 'name'):
                            img_info["name"] = str(img.name)
                    except Exception:
                        pass
                    
                    try:
                        if hasattr(img, 'width'):
                            img_info["width"] = int(img.width) if img.width else 0
                    except Exception:
                        pass
                    
                    try:
                        if hasattr(img, 'height'):
                            img_info["height"] = int(img.height) if img.height else 0
                    except Exception:
                        pass
                    
                    try:
                        if hasattr(img, 'colorspace'):
                            img_info["colorspace"] = str(img.colorspace)
                    except Exception:
                        pass
                    
                    page_info["images"].append(img_info)
        except Exception:
            pass
        
        # Extract annotations
        try:
            if hasattr(page, 'annotations'):
                for ann in page.annotations:
                    # Handle rectangle coordinates properly
                    rect_info = "unknown"
                    try:
                        rect = ann.get("/Rect")
                        if rect:
                            # Rect is also an array [x0, y0, x1, y1]
                            if hasattr(rect, '__iter__') and len(rect) >= 4:
                                rect_info = f"[{rect[0]:.1f}, {rect[1]:.1f}, {rect[2]:.1f}, {rect[3]:.1f}]"
                            else:
                                rect_info = str(rect)
                    except Exception:
                        rect_info = str(ann.get("/Rect", "unknown"))
                    
                    page_info["annotations"].append({
                        "type": ann.get("/Type", "unknown"),
                        "subtype": ann.get("/Subtype", "unknown"),
                        "rect": rect_info
                    })
        except Exception:
            pass
        
        # Extract form fields
        try:
            if hasattr(page, 'get_form_text_fields'):
                form_fields = page.get_form_text_fields()
                for field_name, field_value in form_fields.items():
                    page_info["form_fields"].append({
                        "name": field_name,
                        "value": str(field_value)
                    })
        except Exception:
            pass
        
        structure["pages"].append(page_info)
    
    # Extract outline/bookmarks
    try:
        if hasattr(reader, 'outline') and reader.outline:
            for item in reader.outline:
                structure["outline"].append({
                    "title": item.title if hasattr(item, 'title') else str(item),
                    "page_number": item.page_number if hasattr(item, 'page_number') else None
                })
    except Exception:
        pass
    
    # Extract forms
    try:
        if hasattr(reader, 'get_form_text_fields'):
            form_fields = reader.get_form_text_fields()
            for field_name, field_value in form_fields.items():
                structure["forms"].append({
                    "name": field_name,
                    "value": str(field_value)
                })
    except Exception:
        pass
    
    # Analyze table structure using our extractor
    try:
        extractor = PDFTableExtractor()
        tables = extractor.extract_tables_from_pdf(pdf_path, method="auto")
        
        structure["tables"] = {
            "total_count": len(tables),
            "tables_by_page": {},
            "column_analysis": {
                "unique_columns": [],
                "column_frequency": {}
            },
            "data_types": {}
        }
        
        # Analyze each table
        for i, table in enumerate(tables):
            table_info = {
                "table_index": i + 1,
                "shape": table.shape,
                "columns": list(table.columns),
                "dtypes": {col: str(dtype) for col, dtype in table.dtypes.items()},
                "sample_data": table.head(3).to_dict('records'),
                "has_nulls": table.isnull().any().any(),
                "null_counts": table.isnull().sum().to_dict()
            }
            
            # Try to determine which page this table came from
            # This is approximate since we can't easily map back to pages
            page_num = min(i // 3, len(structure["pages"]) - 1)  # Rough estimate
            if page_num not in structure["tables"]["tables_by_page"]:
                structure["tables"]["tables_by_page"][page_num] = []
            structure["tables"]["tables_by_page"][page_num].append(table_info)
        
        # Column frequency analysis (only if we have tables)
        if tables:
            all_columns = set()
            for table in tables:
                all_columns.update(table.columns)
            
            column_frequency = {}
            for col in all_columns:
                count = sum(1 for table in tables if col in table.columns)
                column_frequency[col] = count
            
            structure["tables"]["column_analysis"] = {
                "unique_columns": list(all_columns),
                "column_frequency": column_frequency
            }
            
    except Exception as e:
        structure["tables"] = {"error": str(e)}
    
    return structure


def generate_literal_structure_diagram(structure: Dict[str, Any]) -> str:
    """Generate a detailed text-based diagram of the PDF literal structure."""
    lines = []
    
    # Header
    lines.append("=" * 100)
    lines.append(f"PDF LITERAL STRUCTURE ANALYSIS: {structure['file_name']}")
    lines.append("=" * 100)
    
    # File information
    lines.append("\n📄 FILE INFORMATION")
    lines.append("-" * 50)
    lines.append(f"Path: {structure['file_path']}")
    lines.append(f"Size: {structure['file_size_bytes']:,} bytes")
    lines.append(f"PDF Version: {structure['pdf_version']}")
    lines.append(f"Pages: {structure['pages_count']}")
    lines.append(f"Encrypted: {structure['is_encrypted']}")
    if JAVA_AVAILABLE:
        lines.append(f"Java Runtime: {JAVA_VERSION}")
    else:
        lines.append("Java Runtime: Not available (Tabula disabled)")
    
    # PDF metadata
    if structure["metadata"]:
        lines.append("\n📋 PDF METADATA")
        lines.append("-" * 50)
        for key, value in structure["metadata"].items():
            if value and value != "None":
                lines.append(f"{key.replace('_', ' ').title()}: {value}")
    
    # Page-by-page analysis
    lines.append("\n📖 PAGE-BY-PAGE ANALYSIS")
    lines.append("-" * 50)
    for page in structure["pages"]:
        lines.append(f"\nPage {page['page_number']}:")
        lines.append(f"  Rotation: {page['rotation']}°")
        if 'error' not in page['mediabox']:
            lines.append(f"  Media Box: {page['mediabox']['width']:.1f} x {page['mediabox']['height']:.1f}")
        else:
            lines.append(f"  Media Box: {page['mediabox']['error']}")
        if page['cropbox'] and 'error' not in page['cropbox']:
            lines.append(f"  Crop Box: {page['cropbox']['width']:.1f} x {page['cropbox']['height']:.1f}")
        elif page['cropbox'] and 'error' in page['cropbox']:
            lines.append(f"  Crop Box: {page['cropbox']['error']}")
        
        # Text content
        text_info = page['text_content']
        lines.append(f"  Text Length: {text_info['text_length']} characters")
        lines.append(f"  Has Text: {text_info['has_text']}")
        if text_info['has_text']:
            preview = text_info['raw_text'][:150].replace('\n', ' ')
            lines.append(f"  Text Preview: {preview}...")
        
        # Fonts
        if page['fonts']:
            lines.append(f"  Fonts ({len(page['fonts'])}):")
            for font in page['fonts'][:5]:  # Show first 5 fonts
                lines.append(f"    - {font['name']} ({font['type']})")
        
        # Images
        if page['images']:
            lines.append(f"  Images ({len(page['images'])}):")
            for img in page['images'][:3]:  # Show first 3 images
                lines.append(f"    - {img['name']}: {img['width']}x{img['height']} ({img['colorspace']})")
        
        # Annotations
        if page['annotations']:
            lines.append(f"  Annotations ({len(page['annotations'])}):")
            for ann in page['annotations'][:3]:  # Show first 3 annotations
                lines.append(f"    - {ann['type']}/{ann['subtype']}")
        
        # Form fields
        if page['form_fields']:
            lines.append(f"  Form Fields ({len(page['form_fields'])}):")
            for field in page['form_fields'][:3]:  # Show first 3 fields
                lines.append(f"    - {field['name']}: {field['value']}")
    
    # Outline/bookmarks
    if structure["outline"]:
        lines.append("\n📑 DOCUMENT OUTLINE")
        lines.append("-" * 50)
        for item in structure["outline"][:10]:  # Show first 10 items
            lines.append(f"  - {item['title']} (Page {item['page_number']})")
    
    # Forms
    if structure["forms"]:
        lines.append("\n📝 FORM FIELDS")
        lines.append("-" * 50)
        for field in structure["forms"][:10]:  # Show first 10 fields
            lines.append(f"  - {field['name']}: {field['value']}")
    
    # Table analysis
    if "error" not in structure["tables"]:
        lines.append("\n📊 TABLE STRUCTURE ANALYSIS")
        lines.append("-" * 50)
        lines.append(f"Total Tables: {structure['tables']['total_count']}")
        
        if structure["tables"]["column_analysis"]["unique_columns"]:
            lines.append(f"Unique Columns: {len(structure['tables']['column_analysis']['unique_columns'])}")
            lines.append("Column Frequency:")
            for col, freq in sorted(structure["tables"]["column_analysis"]["column_frequency"].items(), 
                                  key=lambda x: x[1], reverse=True):
                lines.append(f"  {col}: {freq} tables")
        
        # Show table details
        for page_num, tables in structure["tables"]["tables_by_page"].items():
            lines.append(f"\nTables on Page {page_num + 1}:")
            for table in tables:
                lines.append(f"  Table {table['table_index']}:")
                lines.append(f"    Shape: {table['shape']}")
                lines.append(f"    Columns: {table['columns']}")
                lines.append(f"    Data Types: {table['dtypes']}")
                if table['has_nulls']:
                    lines.append(f"    Null Counts: {table['null_counts']}")
    else:
        lines.append(f"\n❌ TABLE ANALYSIS ERROR: {structure['tables']['error']}")
    
    # Structure summary
    lines.append("\n🏗️ STRUCTURE SUMMARY")
    lines.append("-" * 50)
    lines.append(f"Total Pages: {structure['pages_count']}")
    lines.append(f"Total Fonts: {sum(len(page['fonts']) for page in structure['pages'])}")
    lines.append(f"Total Images: {sum(len(page['images']) for page in structure['pages'])}")
    lines.append(f"Total Annotations: {sum(len(page['annotations']) for page in structure['pages'])}")
    lines.append(f"Total Form Fields: {sum(len(page['form_fields']) for page in structure['pages'])}")
    if "error" not in structure["tables"]:
        lines.append(f"Total Tables: {structure['tables']['total_count']}")
    
    lines.append("\n" + "=" * 100)
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf_literal.py <pdf_file> [--output <output_file>]")
        return 2
    
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return 2
    
    # Parse output option
    output_file = None
    if len(sys.argv) > 2 and sys.argv[2] == "--output" and len(sys.argv) > 3:
        output_file = Path(sys.argv[3])
    
    try:
        print("Analyzing PDF literal structure...")
        structure = analyze_pdf_literal_structure(pdf_path)
        diagram = generate_literal_structure_diagram(structure)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Literal structure analysis saved to: {output_file}")
        else:
            print(diagram)
        
        return 0
        
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
