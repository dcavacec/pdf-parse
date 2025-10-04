"""
Simple Flask Web Interface for PDF Table Extractor
A lightweight alternative to the Streamlit app for extracting tabular data from PDF documents.
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from pdf_table_extractor import PDFTableExtractor
import tempfile
import os
from pathlib import Path
import zipfile
import io
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and table extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Please upload a PDF file'}), 400
        
        # Get extraction parameters
        method = request.form.get('method', 'auto')
        pages = request.form.get('pages', '')
        
        # Parse pages if provided
        page_list = None
        if pages.strip():
            try:
                page_list = [int(p.strip()) for p in pages.split(',')]
            except ValueError:
                return jsonify({'error': 'Invalid page numbers format'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Initialize extractor
            extractor = PDFTableExtractor()
            
            # Extract tables
            tables = extractor.extract_tables_from_pdf(
                tmp_path, 
                method=method,
                pages=page_list
            )
            
            if not tables:
                return jsonify({'error': 'No tables found in the PDF'}), 400
            
            # Prepare response data
            result = {
                'success': True,
                'total_tables': len(tables),
                'tables': []
            }
            
            # Convert tables to JSON-serializable format
            for i, table in enumerate(tables):
                table_data = {
                    'index': i + 1,
                    'rows': table.shape[0],
                    'columns': table.shape[1],
                    'data': table.to_dict('records'),
                    'columns_list': list(table.columns)
                }
                result['tables'].append(table_data)
            
            # Get summary
            summary = extractor.get_table_summary(tables)
            result['summary'] = {
                'total_tables': summary['total_tables'],
                'total_rows': sum(table_info['shape'][0] for table_info in summary['tables_info']),
                'total_columns': sum(table_info['shape'][1] for table_info in summary['tables_info'])
            }
            
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
            
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/download/<int:table_index>')
def download_table(table_index):
    """Download individual table as CSV"""
    try:
        # This would need to be implemented with session storage or similar
        # For now, return a placeholder response
        return jsonify({'error': 'Table download not implemented in this simple version'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_all')
def download_all():
    """Download all tables as Excel"""
    try:
        # This would need to be implemented with session storage or similar
        # For now, return a placeholder response
        return jsonify({'error': 'Bulk download not implemented in this simple version'}), 501
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5001)