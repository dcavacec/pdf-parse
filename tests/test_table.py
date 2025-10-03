"""
Tests for Table class functionality.
"""

import pytest
import tempfile
import os
from pdf_parse import Table


class TestTable:
    """Test cases for Table class."""
    
    def test_table_initialization(self):
        """Test table initialization."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        table = Table(data)
        
        assert table.data == data
        assert table.columns == ["Column_1", "Column_2"]
        assert table.row_count == 3
        assert table.column_count == 2
    
    def test_table_initialization_with_columns(self):
        """Test table initialization with custom columns."""
        data = [["1", "2"], ["3", "4"]]
        columns = ["Name", "Age"]
        table = Table(data, columns)
        
        assert table.data == data
        assert table.columns == columns
    
    def test_get_cell(self):
        """Test getting individual cells."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        table = Table(data)
        
        assert table.get_cell(0, 0) == "A"
        assert table.get_cell(1, 1) == "2"
        assert table.get_cell(2, 0) == "3"
    
    def test_get_cell_out_of_range(self):
        """Test getting cells out of range."""
        data = [["A", "B"], ["1", "2"]]
        table = Table(data)
        
        with pytest.raises(IndexError):
            table.get_cell(5, 0)  # Row out of range
        
        with pytest.raises(IndexError):
            table.get_cell(0, 5)  # Column out of range
    
    def test_get_row(self):
        """Test getting entire rows."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        table = Table(data)
        
        assert table.get_row(0) == ["A", "B"]
        assert table.get_row(1) == ["1", "2"]
        assert table.get_row(2) == ["3", "4"]
    
    def test_get_row_out_of_range(self):
        """Test getting rows out of range."""
        data = [["A", "B"], ["1", "2"]]
        table = Table(data)
        
        with pytest.raises(IndexError):
            table.get_row(5)
    
    def test_get_column(self):
        """Test getting entire columns."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        table = Table(data)
        
        assert table.get_column(0) == ["A", "1", "3"]
        assert table.get_column(1) == ["B", "2", "4"]
    
    def test_get_column_out_of_range(self):
        """Test getting columns out of range."""
        data = [["A", "B"], ["1", "2"]]
        table = Table(data)
        
        with pytest.raises(IndexError):
            table.get_column(5)
    
    def test_to_dict(self):
        """Test converting table to dictionary."""
        data = [["A", "B"], ["1", "2"]]
        columns = ["Name", "Value"]
        table = Table(data, columns)
        
        result = table.to_dict()
        
        expected = {
            "columns": ["Name", "Value"],
            "rows": [["A", "B"], ["1", "2"]],
            "row_count": 2,
            "column_count": 2
        }
        
        assert result == expected
    
    def test_to_csv(self):
        """Test exporting table to CSV."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        columns = ["Name", "Value"]
        table = Table(data, columns)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            csv_path = f.name
        
        try:
            table.to_csv(csv_path)
            
            # Read back and verify
            with open(csv_path, 'r') as f:
                content = f.read()
            
            expected = "Name,Value\nA,B\n1,2\n3,4\n"
            assert content == expected
        
        finally:
            os.unlink(csv_path)
    
    def test_to_json(self):
        """Test exporting table to JSON."""
        data = [["A", "B"], ["1", "2"]]
        columns = ["Name", "Value"]
        table = Table(data, columns)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_path = f.name
        
        try:
            table.to_json(json_path)
            
            # Read back and verify
            import json
            with open(json_path, 'r') as f:
                content = json.load(f)
            
            expected = {
                "columns": ["Name", "Value"],
                "rows": [["A", "B"], ["1", "2"]],
                "row_count": 2,
                "column_count": 2
            }
            assert content == expected
        
        finally:
            os.unlink(json_path)
    
    def test_to_string(self):
        """Test converting table to string representation."""
        data = [["A", "B"], ["1", "2"], ["3", "4"]]
        columns = ["Name", "Value"]
        table = Table(data, columns)
        
        result = table.to_string()
        
        # Should contain headers and data
        assert "Name" in result
        assert "Value" in result
        assert "A" in result
        assert "1" in result
    
    def test_empty_table(self):
        """Test handling of empty table."""
        table = Table([])
        
        assert table.row_count == 0
        assert table.column_count == 0
        assert table.columns == []
        
        # String representation of empty table
        assert table.to_string() == "Empty table"
    
    def test_repr(self):
        """Test string representation."""
        data = [["A", "B"], ["1", "2"]]
        table = Table(data)
        
        repr_str = repr(table)
        assert "Table" in repr_str
        assert "rows=2" in repr_str
        assert "columns=2" in repr_str