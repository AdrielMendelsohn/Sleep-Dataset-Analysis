import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import second_dataset_analysis

class TestSecondDatasetAnalysis(unittest.TestCase):
    
    def test_create_new_features(self):
        data = pd.DataFrame({
            "term_gpa": [3.0, 3.5, 4.0],
            "study": ["A", "A", "B"],
            "midpoint_sleep": [420, 480, 300]
        })
        
        result = second_dataset_analysis.create_new_features(data.copy())
        
        self.assertIn("score", result.columns)
        self.assertIn("score_scaled", result.columns)
        self.assertIn("midpoint_sleep_hour", result.columns)
        
        self.assertTrue((result["score"] == data["term_gpa"] * 25).all())
        self.assertTrue(((result["midpoint_sleep_hour"] - ((data["midpoint_sleep"] / 60 + 23) % 24)).abs() < 1e-6).all())
    
    @patch("second_dataset_analysis.plotting.plot_correlation_matrix")
    def test_create_sleep_heatmap(self, mock_plot):
        data = pd.DataFrame({
            "study": ["A", "B", "A"],
            "demo_firstgen": [1, 0, 1],
            "bedtime_mssd": [30, 45, 60],
            "TotalSleepTime": [7.5, 6.0, 8.0],
            "midpoint_sleep": [450, 480, 420],
            "frac_nights_with_data": [0.9, 0.8, 0.85],
            "daytime_sleep": [0.5, 1.0, 0.7],
            "score_scaled": [50, 75, 30]
        })
        second_dataset_analysis.create_sleep_heatmap(data, True, False)
        mock_plot.assert_called_once()
    
    @patch("second_dataset_analysis.plotting.scatterplot_regression_by_group")
    def test_create_sleep_scatter_plots(self, mock_plot):
        data = pd.DataFrame({
            "study": ["A", "B", "A"],
            "midpoint_sleep": [450, 480, 420],
            "bedtime_mssd": [30, 45, 60],
            "TotalSleepTime": [7.5, 6.0, 8.0],
            "score": [75, 85, 90]
        })
        second_dataset_analysis.create_sleep_scatter_plots(data, True, False)
        self.assertEqual(mock_plot.call_count, 3)

if __name__ == "__main__":
    unittest.main()
