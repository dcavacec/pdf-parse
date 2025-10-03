"""
Tests for PDF parser functionality.
"""

import pytest
import io
from unittest.mock import Mock, patch
from pdf_parse import PDFParser, ParseConfig
from pdf_parse.parser import PDFParseError


class TestPDFParser:
    """Test cases for PDFParser class."""
    
    def test_parser_initialization(self):
        """Test parser initialization with default config."""
        parser = PDFParser()
        assert parser.config is not None
        assert isinstance(parser.config, ParseConfig)
    
    def test_parser_initialization_with_config(self):
        """Test parser initialization with custom config."""
        config = ParseConfig(min_table_size=5)
        parser = PDFParser(config=config)
        assert parser.config.min_table_size == 5
    
    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file."""
        parser = PDFParser()
        with pytest.raises(FileNotFoundError):
            parser.parse_pdf("nonexistent.pdf")
    
    @patch('pdf_parse.parser.PyPDF2')
    def test_parse_pdf_from_bytes(self, mock_pypdf2):
        """Test parsing PDF from bytes."""
        # Mock PyPDF2 components
        mock_reader = Mock()
        mock_page = Mock()
        mock_page.extract_text.return_value = "Header1\tHeader2\nValue1\tValue2\nValue3\tValue4"
        mock_reader.pages = [mock_page]
        mock_pypdf2.PdfReader.return_value = mock_reader
        
        parser = PDFParser()
        pdf_bytes = b"fake pdf content"
        
        tables = parser.parse_pdf_from_bytes(pdf_bytes)
        
        assert len(tables) == 1
        table = tables[0]
        assert table.row_count == 3  # Header + 2 data rows
        assert table.column_count == 2
    
    @patch('pdf_parse.parser.PyPDF2')
    def test_parse_pdf_with_page_range(self, mock_pypdf2):
        """Test parsing PDF with specific page range."""
        # Mock PyPDF2 components
        mock_reader = Mock()
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page1\tData\nValue1\tValue2"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page2\tData\nValue3\tValue4"
        mock_reader.pages = [mock_page1, mock_page2]
        mock_pypdf2.PdfReader.return_value = mock_reader
        
        config = ParseConfig(page_range=(1, 1))  # Only first page
        parser = PDFParser(config=config)
        pdf_bytes = b"fake pdf content"
        
        tables = parser.parse_pdf_from_bytes(pdf_bytes)
        
        assert len(tables) == 1  # Only one table from first page
    
    def test_detect_tables_in_text(self):
        """Test table detection in text."""
        parser = PDFParser()
        
        # Test text with tab-separated values
        text_with_tabs = "Name\tAge\tCity\nJohn\t25\tNYC\nJane\t30\tLA"
        tables = parser._detect_tables_in_text(text_with_tabs)
        
        assert len(tables) == 1
        assert len(tables[0]) == 3  # 3 rows
        assert len(tables[0][0]) == 3  # 3 columns
    
    def test_detect_tables_in_text_with_spaces(self):
        """Test table detection with space-separated values."""
        parser = PDFParser()
        
        # Test text with multiple spaces
        text_with_spaces = "Name    Age    City\nJohn    25     NYC\nJane    30     LA"
        tables = parser._detect_tables_in_text(text_with_spaces)
        
        assert len(tables) == 1
        assert len(tables[0]) == 3  # 3 rows
    
    def test_is_valid_table(self):
        """Test table validation."""
        parser = PDFParser()
        
        # Valid table
        valid_table = [["A", "B"], ["1", "2"], ["3", "4"]]
        assert parser._is_valid_table(valid_table) is True
        
        # Invalid table (too small)
        config = ParseConfig(min_table_size=5)
        parser_small = PDFParser(config=config)
        assert parser_small._is_valid_table(valid_table) is False
        
        # Invalid table (inconsistent columns)
        invalid_table = [["A", "B"], ["1", "2", "3"]]
        assert parser._is_valid_table(invalid_table) is False
        
        # Empty table
        assert parser._is_valid_table([]) is False


class TestParseConfig:
    """Test cases for ParseConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ParseConfig()
        assert config.min_table_size == 2
        assert config.merge_cells is True
        assert config.preserve_formatting is False
        assert config.encoding == "utf-8"
        assert config.page_range is None
        assert config.table_detection_threshold == 0.5
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = ParseConfig(
            min_table_size=5,
            merge_cells=False,
            preserve_formatting=True,
            encoding="latin-1",
            page_range=(1, 10),
            table_detection_threshold=0.8
        )
        
        assert config.min_table_size == 5
        assert config.merge_cells is False
        assert config.preserve_formatting is True
        assert config.encoding == "latin-1"
        assert config.page_range == (1, 10)
        assert config.table_detection_threshold == 0.8
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Invalid min_table_size
        with pytest.raises(ValueError):
            ParseConfig(min_table_size=0)
        
        # Invalid table_detection_threshold
        with pytest.raises(ValueError):
            ParseConfig(table_detection_threshold=1.5)
        
        # Invalid page_range
        with pytest.raises(ValueError):
            ParseConfig(page_range=(5, 3))  # start > end