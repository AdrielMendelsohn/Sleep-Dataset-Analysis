import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
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

    @patch('pandas.DataFrame.to_csv')
    def test_json_pd_to_csv_basic(self, mock_to_csv):
        """Test json_pd_to_csv function"""
        to_csv.json_pd_to_csv(self.test_json_data, "test_output.csv")
        mock_to_csv.assert_called_once()

    @patch('pandas.DataFrame.to_csv')
    def test_amount_of_entries_csv_simple_basic(self, mock_to_csv):
        """Test amount_of_entries_csv_simple function"""
        test_datasets = {"test_dataset": "test/path"}
        
        with patch('to_csv.cleaning.clean_data_from_jsons_folder') as mock_clean, patch('to_csv.cleaning.extract_participant') as mock_extract:
            
            mock_clean.return_value = self.test_json_data
            mock_extract.return_value = "u001"
            
            to_csv.amount_of_entries_csv_simple(test_datasets, "test_output.csv")
            mock_to_csv.assert_called_once()

    @patch('to_csv.files_import.process_folder')
    @patch('pandas.DataFrame.to_csv')
    def test_amount_of_entries_csv_basic(self, mock_to_csv, mock_process):
        """Test amount_of_entries_csv function"""
        test_datasets = {"test_dataset": "test/path"}
        mock_process.return_value = self.test_json_data
        
        to_csv.amount_of_entries_csv(test_datasets, "test_output.csv")
        mock_to_csv.assert_called_once()

    def test_folder_to_csv_no_files(self):
        """Test folder_to_csv with no JSON files"""
        with patch('os.listdir', return_value=[]):
            result = to_csv.folder_to_csv("test/path", "test_column", False)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(result.empty)

    def test_json_pd_to_csv_empty_data(self):
        """Test json_pd_to_csv with empty data"""
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            to_csv.json_pd_to_csv([], "test_output.csv")
            # Verify that to_csv was called once even when data is empty
            mock_to_csv.assert_called_once()

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists("test_output.csv"):
            os.remove("test_output.csv")

if __name__ == '__main__':
    unittest.main()