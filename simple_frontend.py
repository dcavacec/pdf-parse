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
import logging
from typing import List, Dict, Any

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

@app.route('/upload_multiple', methods=['POST'])
def upload_multiple_files():
    """Handle multiple file uploads and batch table extraction"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        # Filter for PDF files
        pdf_files = [file for file in files if file.filename.lower().endswith('.pdf')]
        if not pdf_files:
            return jsonify({'error': 'No PDF files found in upload'}), 400
        
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
        
        # Initialize extractor
        extractor = PDFTableExtractor()
        
        all_tables = []
        processed_files = []
        temp_files = []
        
        try:
            # Process each PDF file
            for file in pdf_files:
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        file.save(tmp_file.name)
                        temp_files.append(tmp_file.name)
                    
                    # Extract tables from this file
                    file_tables = extractor.extract_tables_from_pdf(
                        tmp_file.name, 
                        method=method,
                        pages=page_list
                    )
                    
                    # Add file information to each table
                    for i, table in enumerate(file_tables):
                        table_data = {
                            'index': len(all_tables) + 1,
                            'file_name': file.filename,
                            'rows': table.shape[0],
                            'columns': table.shape[1],
                            'data': table.to_dict('records'),
                            'columns_list': list(table.columns)
                        }
                        all_tables.append(table_data)
                    
                    processed_files.append({
                        'name': file.filename,
                        'tables_found': len(file_tables)
                    })
                    
                except Exception as e:
                    logging.warning(f"Failed to process file {file.filename}: {str(e)}")
                    processed_files.append({
                        'name': file.filename,
                        'tables_found': 0,
                        'error': str(e)
                    })
                    continue
            
            if not all_tables:
                return jsonify({'error': 'No tables found in any of the PDF files'}), 400
            
            # Prepare response data
            result = {
                'success': True,
                'files_processed': len(processed_files),
                'total_tables': len(all_tables),
                'tables': all_tables,
                'files': processed_files
            }
            
            # Get summary
            summary = extractor.get_table_summary([pd.DataFrame(table['data']) for table in all_tables])
            result['summary'] = {
                'total_tables': summary['total_tables'],
                'total_rows': sum(table_info['shape'][0] for table_info in summary['tables_info']),
                'total_columns': sum(table_info['shape'][1] for table_info in summary['tables_info'])
            }
            
            return jsonify(result)
            
        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
            
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

@app.route('/download_selected', methods=['POST'])
def download_selected_tables():
    """Download selected tables in specified format"""
    try:
        data = request.get_json()
        if not data or 'tables' not in data or 'format' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        tables_data = data['tables']
        format_type = data['format']
        
        if not tables_data:
            return jsonify({'error': 'No tables selected'}), 400
        
        # Convert table data back to DataFrames
        tables = []
        for table_data in tables_data:
            df = pd.DataFrame(table_data['data'])
            tables.append(df)
        
        if format_type == 'excel':
            # Create Excel file in memory
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                for i, table in enumerate(tables):
                    sheet_name = f'Table_{i+1}'
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
            
            excel_buffer.seek(0)
            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='selected_tables.xlsx'
            )
        
        elif format_type == 'csv':
            # Create ZIP file with CSV files
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for i, table in enumerate(tables):
                    csv_data = table.to_csv(index=False)
                    zip_file.writestr(f"table_{i+1}.csv", csv_data)
            
            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name='selected_tables.zip'
            )
        
        else:
            return jsonify({'error': 'Invalid format specified'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error creating download: {str(e)}'}), 500

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