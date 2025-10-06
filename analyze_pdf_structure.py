"""
PDF Structure Analyzer
Analyzes a PDF file and outputs a diagram of its metadata structure.

Usage:
    python analyze_pdf_structure.py "C:\\path\\to\\file.pdf"
    python analyze_pdf_structure.py "C:\\path\\to\\file.pdf" --output structure.txt
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict, List, Any
import json

from pypdf import PdfReader
from pdf_table_extractor import PDFTableExtractor
from java_check import JAVA_AVAILABLE, JAVA_VERSION


def analyze_pdf_structure(pdf_path: Path) -> Dict[str, Any]:
    """Analyze PDF structure and return metadata."""
    reader = PdfReader(str(pdf_path))
    extractor = PDFTableExtractor()
    
    structure = {
        "file_info": {
            "name": pdf_path.name,
            "size_bytes": pdf_path.stat().st_size,
            "pages": len(reader.pages)
        },
        "pdf_metadata": {},
        "page_analysis": [],
        "table_analysis": {},
        "extraction_methods": {}
    }
    
    # Extract PDF metadata
    if reader.metadata:
        structure["pdf_metadata"] = {
            "title": reader.metadata.get("/Title", ""),
            "author": reader.metadata.get("/Author", ""),
            "subject": reader.metadata.get("/Subject", ""),
            "creator": reader.metadata.get("/Creator", ""),
            "producer": reader.metadata.get("/Producer", ""),
            "creation_date": str(reader.metadata.get("/CreationDate", "")),
            "modification_date": str(reader.metadata.get("/ModDate", ""))
        }
    
    # Analyze each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        
        page_info = {
            "page_number": page_num + 1,
            "text_length": len(text),
            "has_text": len(text.strip()) > 0,
            "text_preview": text[:200] + "..." if len(text) > 200 else text,
            "rotation": page.rotation,
            "mediabox": str(page.mediabox) if hasattr(page, 'mediabox') else "unknown"
        }
        
        # Try to detect potential tables by looking for tabular patterns
        lines = text.split('\n')
        potential_table_lines = 0
        for line in lines:
            if '\t' in line or line.count('  ') >= 3:
                potential_table_lines += 1
        
        page_info["potential_table_lines"] = potential_table_lines
        page_info["table_likelihood"] = "high" if potential_table_lines > 5 else "medium" if potential_table_lines > 2 else "low"
        
        structure["page_analysis"].append(page_info)
    
    # Test different extraction methods
    methods = ["pdfplumber", "camelot"]
    if JAVA_AVAILABLE:
        methods.append("tabula")
    
    for method in methods:
        try:
            tables = extractor.extract_tables_from_pdf(pdf_path, method=method)
            structure["extraction_methods"][method] = {
                "success": True,
                "tables_found": len(tables),
                "table_shapes": [table.shape for table in tables],
                "sample_columns": [list(table.columns) for table in tables[:3]]  # First 3 tables
            }
        except Exception as e:
            structure["extraction_methods"][method] = {
                "success": False,
                "error": str(e)
            }
    
    # Overall table analysis
    try:
        all_tables = extractor.extract_tables_from_pdf(pdf_path, method="auto")
        structure["table_analysis"] = {
            "total_tables": len(all_tables),
            "tables_by_page": {},
            "column_analysis": {},
            "data_types": {}
        }
        
        # Analyze columns across all tables
        all_columns = set()
        for table in all_tables:
            all_columns.update(table.columns)
        
        structure["table_analysis"]["unique_columns"] = list(all_columns)
        structure["table_analysis"]["column_frequency"] = {}
        
        for col in all_columns:
            count = sum(1 for table in all_tables if col in table.columns)
            structure["table_analysis"]["column_frequency"][col] = count
        
    except Exception as e:
        structure["table_analysis"]["error"] = str(e)
    
    return structure


def generate_diagram(structure: Dict[str, Any]) -> str:
    """Generate a text-based diagram of the PDF structure."""
    lines = []
    
    # Header
    lines.append("=" * 80)
    lines.append(f"PDF STRUCTURE ANALYSIS: {structure['file_info']['name']}")
    lines.append("=" * 80)
    
    # File info
    lines.append("\n📄 FILE INFORMATION")
    lines.append("-" * 40)
    lines.append(f"Size: {structure['file_info']['size_bytes']:,} bytes")
    lines.append(f"Pages: {structure['file_info']['pages']}")
    if JAVA_AVAILABLE:
        lines.append(f"Java Runtime: {JAVA_VERSION}")
    else:
        lines.append("Java Runtime: Not available (Tabula disabled)")
    
    # PDF metadata
    if structure["pdf_metadata"]:
        lines.append("\n📋 PDF METADATA")
        lines.append("-" * 40)
        for key, value in structure["pdf_metadata"].items():
            if value and value != "None":
                lines.append(f"{key.replace('_', ' ').title()}: {value}")
    
    # Page analysis
    lines.append("\n📖 PAGE ANALYSIS")
    lines.append("-" * 40)
    for page in structure["page_analysis"]:
        lines.append(f"Page {page['page_number']}:")
        lines.append(f"  Text length: {page['text_length']} chars")
        lines.append(f"  Table likelihood: {page['table_likelihood']}")
        lines.append(f"  Potential table lines: {page['potential_table_lines']}")
        if page["text_preview"]:
            lines.append(f"  Preview: {page['text_preview'][:100]}...")
        lines.append("")
    
    # Extraction methods
    lines.append("\n🔧 EXTRACTION METHODS")
    lines.append("-" * 40)
    for method, result in structure["extraction_methods"].items():
        if result["success"]:
            lines.append(f"✅ {method.upper()}:")
            lines.append(f"   Tables found: {result['tables_found']}")
            lines.append(f"   Shapes: {result['table_shapes']}")
            if result["sample_columns"]:
                lines.append(f"   Sample columns: {result['sample_columns'][0]}")
        else:
            lines.append(f"❌ {method.upper()}: {result['error']}")
        lines.append("")
    
    # Table analysis
    if "error" not in structure["table_analysis"]:
        lines.append("\n📊 TABLE ANALYSIS")
        lines.append("-" * 40)
        lines.append(f"Total tables found: {structure['table_analysis']['total_tables']}")
        
        if structure["table_analysis"]["unique_columns"]:
            lines.append(f"Unique columns: {len(structure['table_analysis']['unique_columns'])}")
            lines.append("Column frequency:")
            for col, freq in sorted(structure["table_analysis"]["column_frequency"].items(), 
                                  key=lambda x: x[1], reverse=True):
                lines.append(f"  {col}: {freq} tables")
    else:
        lines.append(f"\n❌ TABLE ANALYSIS ERROR: {structure['table_analysis']['error']}")
    
    # Recommendations
    lines.append("\n💡 RECOMMENDATIONS")
    lines.append("-" * 40)
    
    # Find best extraction method
    best_method = None
    best_count = 0
    for method, result in structure["extraction_methods"].items():
        if result["success"] and result["tables_found"] > best_count:
            best_method = method
            best_count = result["tables_found"]
    
    if best_method:
        lines.append(f"• Recommended extraction method: {best_method}")
    
    # Suggest rules based on common columns
    if structure["table_analysis"].get("column_frequency"):
        common_cols = [col for col, freq in structure["table_analysis"]["column_frequency"].items() 
                      if freq >= 2]
        if common_cols:
            lines.append(f"• Common columns for rules: {common_cols[:5]}")
    
    # Page recommendations
    high_table_pages = [p["page_number"] for p in structure["page_analysis"] 
                       if p["table_likelihood"] == "high"]
    if high_table_pages:
        lines.append(f"• Pages with high table likelihood: {high_table_pages}")
    
    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf_structure.py <pdf_file> [--output <output_file>]")
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
        print("Analyzing PDF structure...")
        structure = analyze_pdf_structure(pdf_path)
        diagram = generate_diagram(structure)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Structure analysis saved to: {output_file}")
        else:
            print(diagram)
        
        return 0
        
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
