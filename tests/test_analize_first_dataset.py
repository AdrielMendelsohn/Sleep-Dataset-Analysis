import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add the src directory to sys.path dynamically
repo_root = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(repo_root, "..", "src")         
sys.path.append(src_path)

from first_dataset_analysis import (
    make_interactive_heat_map, make_regular_heat_map, plot_gpa_correlations,
    plot_sleep_correlations, plot_more_correlations
)

class TestAnalyzeFirstDataset(unittest.TestCase):
    def setUp(self):
        # יצירת DataFrame לדוגמא עם נתונים מספריים
        np.random.seed(42)
        self.df = pd.DataFrame({
            "User": [f"u{i:02}" for i in range(10)],
            "gpa_all": np.random.rand(10) * 4,
            "avg_working_percentage": np.random.rand(10) * 100,
            "avg_workout_per_day": np.random.rand(10) * 3,
            "stressed_percentage": np.random.rand(10) * 100,
            "avg_sad_rating": np.random.rand(10) * 10,
            "avg_sleep_rating": np.random.rand(10) * 10,
            "happy_percentage": np.random.rand(10) * 100,
            "avg_stress_level": np.random.rand(10) * 10,
            "number_of_people": np.random.randint(1, 10, size=10),
            "avg_happy_rating": np.random.rand(10) * 10,
            "avg_sleep_hours": np.random.rand(10) * 10,
            "gpa_13s": np.random.rand(10) * 4
        })
    
    def test_make_interactive_heat_map(self):
        try:
            make_interactive_heat_map(self.df)
        except Exception as e:
            self.fail(f"make_interactive_heat_map raised an exception: {e}")
    
    def test_make_regular_heat_map(self):
        try:
            make_regular_heat_map(self.df)
        except Exception as e:
            self.fail(f"make_regular_heat_map raised an exception: {e}")
    
    def test_plot_gpa_correlations(self):
        try:
            plot_gpa_correlations(self.df)
        except Exception as e:
            self.fail(f"plot_gpa_correlations raised an exception: {e}")
    
    def test_plot_sleep_correlations(self):
        try:
            plot_sleep_correlations(self.df)
        except Exception as e:
            self.fail(f"plot_sleep_correlations raised an exception: {e}")
    
    def test_plot_more_correlations(self):
        try:
            plot_more_correlations(self.df)
        except Exception as e:
            self.fail(f"plot_more_correlations raised an exception: {e}")
    
    def test_user_column_removed(self):
        df_numeric = self.df.drop(columns=["User"], errors="ignore")
        self.assertNotIn("User", df_numeric.columns)
    
    def test_correlation_matrix_computation(self):
        df_numeric = self.df.drop(columns=["User"], errors="ignore")
        correlation_matrix = df_numeric.corr()
        self.assertEqual(correlation_matrix.shape[0], len(df_numeric.columns))
        self.assertEqual(correlation_matrix.shape[1], len(df_numeric.columns))

if __name__ == "__main__":
    unittest.main()
