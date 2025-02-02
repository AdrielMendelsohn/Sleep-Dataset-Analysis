import os
import tempfile
import pytest
from first_dataset_analysis import make_interactive_heat_map

@pytest.fixture
def sample_dataframe():
    import pandas as pd
    data = {
        'User': ['u00', 'u01', 'u02'],
        'avg_working_percentage': [75, 85, 90],
        'gpa_all': [3.5, 3.8, 4.0],
        'avg_workout_per_day': [30, 45, 20],
        'stressed_percentage': [20, 30, 25],
        'avg_sleep_hours': [7, 6.5, 8],
        'screen_time': [3, 4, 2],
        'avg_stress_level': [3, 4, 2],
        'number_of_peaks': [5, 6, 4]
    }
    return pd.DataFrame(data)

def test_make_interactive_heat_map_creates_file(sample_dataframe):
    """
    Test if the interactive heatmap HTML file is created
    Run inside a temporary folder to make sure the code will run whether the 'result' folder exists or not
    """
    # Create a temporary folder
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = os.path.join(temp_dir, "results")
        os.makedirs(output_dir)  # Create the 'results' folder inside the temporary folder
        output_path = os.path.join(output_dir, "plot.html")

        # Change the workspace to the temporary folder
        original_cwd = os.getcwd()
        os.chdir(temp_dir)

        try:
            # Running the function
            make_interactive_heat_map(sample_dataframe)

            # Checking the existence of the file
            assert os.path.exists(output_path), f"{output_path} was not created."
        finally:
            # Return to the original workspace
            os.chdir(original_cwd)
