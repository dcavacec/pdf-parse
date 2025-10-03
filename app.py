"""
Streamlit Web Interface for PDF Table Extractor
A user-friendly web application for extracting tabular data from PDF documents.
"""

import streamlit as st
import pandas as pd
from pdf_table_extractor import PDFTableExtractor
import tempfile
import os
from pathlib import Path
import zipfile
import io

# Page configuration
st.set_page_config(
    page_title="PDF Table Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 PDF Table Extractor</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Settings")
    
    # Extraction method selection
    extraction_method = st.sidebar.selectbox(
        "Extraction Method",
        ["auto", "pdfplumber", "tabula", "camelot"],
        help="Choose the extraction method. 'auto' tries multiple methods for best results."
    )
    
    # Page selection
    page_option = st.sidebar.radio(
        "Pages to Extract",
        ["All pages", "Specific pages"],
        help="Choose whether to extract from all pages or specific pages"
    )
    
    pages = None
    if page_option == "Specific pages":
        pages_input = st.sidebar.text_input(
            "Page numbers (comma-separated)",
            placeholder="e.g., 1,3,5",
            help="Enter page numbers separated by commas"
        )
        if pages_input:
            try:
                pages = [int(p.strip()) for p in pages_input.split(',')]
            except ValueError:
                st.sidebar.error("Please enter valid page numbers separated by commas")
                pages = None
    
    # File upload
    st.subheader("📁 Upload PDF File")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF file containing tabular data"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.info(f"📄 **File:** {uploaded_file.name} | **Size:** {uploaded_file.size:,} bytes")
        
        # Extract button
        if st.button("🔍 Extract Tables", type="primary"):
            with st.spinner("Extracting tables from PDF..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Initialize extractor
                    extractor = PDFTableExtractor()
                    
                    # Extract tables
                    tables = extractor.extract_tables_from_pdf(
                        tmp_path, 
                        method=extraction_method,
                        pages=pages
                    )
                    
                    # Clean up temporary file
                    os.unlink(tmp_path)
                    
                    if tables:
                        st.success(f"✅ Successfully extracted {len(tables)} tables!")
                        
                        # Display summary
                        st.subheader("📋 Extraction Summary")
                        summary = extractor.get_table_summary(tables)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Tables", summary['total_tables'])
                        with col2:
                            total_rows = sum(table_info['shape'][0] for table_info in summary['tables_info'])
                            st.metric("Total Rows", total_rows)
                        with col3:
                            total_cols = sum(table_info['shape'][1] for table_info in summary['tables_info'])
                            st.metric("Total Columns", total_cols)
                        
                        # Display each table
                        st.subheader("📊 Extracted Tables")
                        
                        for i, table in enumerate(tables):
                            with st.expander(f"Table {i+1} ({table.shape[0]} rows × {table.shape[1]} columns)"):
                                st.dataframe(table, use_container_width=True)
                                
                                # Download individual table
                                csv = table.to_csv(index=False)
                                st.download_button(
                                    label=f"📥 Download Table {i+1} as CSV",
                                    data=csv,
                                    file_name=f"table_{i+1}.csv",
                                    mime="text/csv"
                                )
                        
                        # Download all tables as Excel
                        st.subheader("💾 Download All Tables")
                        
                        # Create Excel file in memory
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            for i, table in enumerate(tables):
                                sheet_name = f'Table_{i+1}'
                                table.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                        excel_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download All Tables as Excel",
                            data=excel_buffer.getvalue(),
                            file_name="extracted_tables.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                        # Download all tables as ZIP of CSV files
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                            for i, table in enumerate(tables):
                                csv_data = table.to_csv(index=False)
                                zip_file.writestr(f"table_{i+1}.csv", csv_data)
                        
                        zip_buffer.seek(0)
                        
                        st.download_button(
                            label="📥 Download All Tables as ZIP (CSV files)",
                            data=zip_buffer.getvalue(),
                            file_name="extracted_tables.zip",
                            mime="application/zip"
                        )
                    
                    else:
                        st.warning("⚠️ No tables found in the PDF. Try a different extraction method or check if the PDF contains tabular data.")
                        
                        # Show troubleshooting tips
                        with st.expander("🔧 Troubleshooting Tips"):
                            st.markdown("""
                            **If no tables were found, try:**
                            - Using a different extraction method (especially 'pdfplumber' or 'tabula')
                            - Checking if the PDF contains actual tabular data (not just text)
                            - Ensuring the PDF is not password-protected or corrupted
                            - Trying with specific page numbers if you know where the tables are located
                            """)
                
                except Exception as e:
                    st.error(f"❌ Error extracting tables: {str(e)}")
                    
                    # Show error details
                    with st.expander("🔍 Error Details"):
                        st.code(str(e))
    
    else:
        # Show instructions when no file is uploaded
        st.markdown("""
        <div class="info-box">
        <h3>📖 How to Use</h3>
        <ol>
        <li><strong>Upload a PDF file</strong> containing tabular data using the file uploader above</li>
        <li><strong>Choose extraction settings</strong> in the sidebar (method, pages, etc.)</li>
        <li><strong>Click "Extract Tables"</strong> to process the PDF</li>
        <li><strong>View and download</strong> the extracted tables in various formats</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Show supported formats and methods
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📋 Supported Extraction Methods:**
            - **Auto**: Tries multiple methods for best results
            - **PDFPlumber**: Good for simple tables
            - **Tabula**: Excellent for complex tables
            - **Camelot**: Best for high-quality PDFs
            """)
        
        with col2:
            st.markdown("""
            **💾 Download Formats:**
            - Individual CSV files
            - Excel workbook with multiple sheets
            - ZIP archive of CSV files
            """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit, pandas, and PDF extraction libraries"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()