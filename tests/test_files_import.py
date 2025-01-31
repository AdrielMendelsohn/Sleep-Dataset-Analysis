import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
import os
import sys
repo_root = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(repo_root, "..", "src")         
sys.path.append(src_path)
import to_csv

class TestToCSV(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_df = pd.DataFrame({
            'test_column': ['data1', 'data2'],
            'other_column': [1, 2]
        })
        
        self.test_json_data = [
            {
                "file_name": "test_u001.json",
                "data": [{"value": 1}, {"value": 2}],
                "record_count": 2
            }
        ]

    @patch('os.listdir')
    @patch('pandas.read_json')
    def test_folder_to_csv_basic(self, mock_read_json, mock_listdir):
        """Test basic functionality of folder_to_csv"""
        mock_listdir.return_value = ['test_u001.json']
        mock_read_json.return_value = self.test_df
        
        result = to_csv.folder_to_csv("test/path", "test_column", False)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_folder_to_csv_no_files(self):
        """Test folder_to_csv with no JSON files"""
        with patch('os.listdir', return_value=[]):
            result = to_csv.folder_to_csv("test/path", "test_column", False)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(result.empty)

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")

if __name__ == '__main__':
    unittest.main()
