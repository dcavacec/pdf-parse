"""
PDF Structure Analyzer - JSON Output
Analyzes a PDF file and outputs structured metadata as JSON.

Usage:
    python analyze_pdf_json.py "C:\\path\\to\\file.pdf"
    python analyze_pdf_json.py "C:\\path\\to\\file.pdf" --output structure.json
"""

from __future__ import annotations

from pathlib import Path
import sys
import json
from typing import Dict, Any

from analyze_pdf_structure import analyze_pdf_structure


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python analyze_pdf_json.py <pdf_file> [--output <output_file>]")
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
        
        # Convert to JSON-serializable format
        json_structure = json.loads(json.dumps(structure, default=str))
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_structure, f, indent=2, ensure_ascii=False)
            print(f"JSON structure analysis saved to: {output_file}")
        else:
            print(json.dumps(json_structure, indent=2, ensure_ascii=False))
        
        return 0
        
    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
