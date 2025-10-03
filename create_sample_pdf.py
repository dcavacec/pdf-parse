"""
Create a sample PDF with tabular data for testing the PDF Table Extractor.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import os


def create_sample_pdf():
    """Create a sample PDF with multiple tables for testing."""
    
    # Create the PDF document
    filename = "sample_tables.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Add title
    title = Paragraph("Sample PDF with Tabular Data", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Table 1: Sales Data
    sales_data = [
        ['Product', 'Q1 Sales', 'Q2 Sales', 'Q3 Sales', 'Q4 Sales', 'Total'],
        ['Widget A', '$1,200', '$1,500', '$1,800', '$2,100', '$6,600'],
        ['Widget B', '$800', '$950', '$1,200', '$1,400', '$4,350'],
        ['Widget C', '$2,100', '$2,300', '$2,500', '$2,800', '$9,700'],
        ['Widget D', '$1,500', '$1,600', '$1,700', '$1,900', '$6,700'],
        ['Total', '$5,600', '$6,350', '$7,200', '$8,200', '$27,350']
    ]
    
    sales_table = Table(sales_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    sales_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Sales Data by Quarter", styles['Heading2']))
    elements.append(sales_table)
    elements.append(Spacer(1, 20))
    
    # Table 2: Employee Information
    employee_data = [
        ['Employee ID', 'Name', 'Department', 'Position', 'Salary', 'Start Date'],
        ['EMP001', 'John Smith', 'Engineering', 'Senior Developer', '$85,000', '2020-01-15'],
        ['EMP002', 'Jane Doe', 'Marketing', 'Marketing Manager', '$75,000', '2019-03-22'],
        ['EMP003', 'Bob Johnson', 'Sales', 'Sales Representative', '$60,000', '2021-06-10'],
        ['EMP004', 'Alice Brown', 'HR', 'HR Specialist', '$65,000', '2020-09-05'],
        ['EMP005', 'Charlie Wilson', 'Engineering', 'Junior Developer', '$55,000', '2022-02-14']
    ]
    
    employee_table = Table(employee_data, colWidths=[1*inch, 1.5*inch, 1.2*inch, 1.5*inch, 1*inch, 1*inch])
    employee_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    elements.append(Paragraph("Employee Information", styles['Heading2']))
    elements.append(employee_table)
    elements.append(Spacer(1, 20))
    
    # Table 3: Financial Summary
    financial_data = [
        ['Metric', '2021', '2022', '2023', 'Change (%)'],
        ['Revenue', '$2.5M', '$3.2M', '$4.1M', '+28.1%'],
        ['Expenses', '$1.8M', '$2.1M', '$2.6M', '+23.8%'],
        ['Net Profit', '$700K', '$1.1M', '$1.5M', '+36.4%'],
        ['ROI', '28.0%', '34.4%', '36.6%', '+6.4%']
    ]
    
    financial_table = Table(financial_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Financial Summary", styles['Heading2']))
    elements.append(financial_table)
    
    # Build PDF
    doc.build(elements)
    print(f"Sample PDF created: {filename}")


if __name__ == "__main__":
    create_sample_pdf()