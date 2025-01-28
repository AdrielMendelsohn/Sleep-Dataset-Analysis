import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
import first_dataset_excel

class TestFirstDatasetExcel(unittest.TestCase):
    def setUp(self):
        self.test_output_path = "test_output.xlsx"
        first_dataset_excel.output_path = self.test_output_path
        
    def tearDown(self):
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    @patch('os.path.exists')
    @patch('os.remove')
    @patch('openpyxl.Workbook.save')
    def test_initialize_excel_file(self, mock_save, mock_remove, mock_exists):
        mock_exists.return_value = True
        first_dataset_excel.initialize_excel_file()
        mock_remove.assert_called_once_with(self.test_output_path)

    @patch('to_csv.folder_to_csv')
    def test_load_survey_data(self, mock_folder_to_csv):
        mock_folder_to_csv.return_value = pd.DataFrame({'User': ['u01'], 'level': [1]})
        data = first_dataset_excel.load_survey_data()
        self.assertIn('Stress', data)
        self.assertIsInstance(data['Stress'], pd.DataFrame)

    def test_process_stress_social(self):
        test_data = {
            'Stress': pd.DataFrame({
                'User': ['u01', 'u02'],
                'level': [1, 2]
            }),
            'Social': pd.DataFrame({
                'User': ['u01', 'u02'],
                'number': [1, 2]
            })
        }
        combined_csv = {}
        first_dataset_excel.process_stress_social(test_data, combined_csv)
        self.assertIn('avg_stress_level', combined_csv)
        self.assertIn('number_of_people', combined_csv)

    def test_process_exercise(self):
        test_data = {
            'Exercise': pd.DataFrame({
                'User': ['u01', 'u02'],
                'have': [1, 0],
                'exercise': [2, 3],
                'walk': [1, 2]
            })
        }
        combined_csv = {}
        first_dataset_excel.process_exercise(test_data, combined_csv)
        self.assertIn('amount_of_workouts', combined_csv)
        self.assertIn('avg_workout_per_day', combined_csv)

    def test_process_sleep(self):
        test_data = {
            'Sleep': pd.DataFrame({
                'User': ['u01', 'u02'],
                'hour': [1, 2],
                'rate': [1, 2]
            })
        }
        combined_csv = {}
        first_dataset_excel.process_sleep(test_data, combined_csv)
        self.assertIn('avg_sleep_hours', combined_csv)
        self.assertIn('avg_sleep_rating', combined_csv)

    def test_process_mood(self):
        test_data = {
            'Mood': pd.DataFrame({
                'User': ['u01', 'u02'],
                'happy': [1, 0],
                'sad': [0, 1],
                'happyornot': [1, 2],
                'sadornot': [1, 2]
            }),
            'Mood2': pd.DataFrame({
                'User': ['u01', 'u02'],
                'how': [1, 2]
            })
        }
        combined_csv = {}
        first_dataset_excel.process_mood(test_data, combined_csv)
        self.assertIn('avg_happy_rating', combined_csv)
        self.assertIn('happy_percentage', combined_csv)

    def test_process_time_management(self):
        test_data = {
            'Activity': pd.DataFrame({
                'User': ['u01'],
                'working': [1],
                'relaxing': [2],
                'other_working': [3],
                'other_relaxing': [4]
            })
        }
        combined_csv = {}
        first_dataset_excel.process_time_managment(test_data, combined_csv)
        self.assertIn('avg_alone_percentage', combined_csv)
        self.assertIn('avg_working_percentage', combined_csv)

    @patch('first_dataset_excel.pd.read_csv')
    def test_create_grades_dictionary(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            'uid': ['u01'],
            ' gpa all': [3.5],
            ' gpa 13s': [3.7]
        })
        grades_dict = first_dataset_excel.create_grades_dictionary()
        self.assertIn('u01', grades_dict)
        self.assertEqual(grades_dict['u01']['gpaAll'], 3.5 * 25)

if __name__ == '__main__':
    unittest.main()