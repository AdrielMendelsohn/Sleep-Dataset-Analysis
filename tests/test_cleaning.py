import pytest
import pandas as pd
import numpy as np
import os
from ..src import cleaning

# Fixtures
@pytest.fixture
def sample_json_data():
    return [
        {
            'data': [{'value': 1}, {'null': 'value'}, {'value': 2}],
            'record_count': 3
        },
        {
            'data': [{'value': 3}, {'value': 4}],
            'record_count': 2
        }
    ]

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'A': ['1', '2', ' ', '4'],
        'B': ['a', 'b', '', 'd']
    })

@pytest.fixture
def sample_sleep_data(tmp_path):
    # Create a temporary CSV file with test data
    df = pd.DataFrame({
        'cohort': ['A', 'B', 'C', 'D'],
        'bedtime_mssd': [1.5, 2.0, 6.0, 3.0],
        'daytime_sleep': [100, 160, 120, 90],
        'other_metric': [10, 20, 30, 40]
    })
    file_path = tmp_path / "test_sleep_data.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)

# Tests for drop_blanks_and_nulls
def test_drop_blanks_and_nulls(sample_df):
    result = cleaning.drop_blanks_and_nulls(sample_df)
    
    # Check that blank values are removed
    assert len(result) == 3  # One row should be removed
    assert ' ' not in result['A'].values
    assert '' not in result['B'].values

# Tests for extract_participant
def test_extract_participant_valid():
    filename = "data_u123.json"
    result = cleaning.extract_participant(filename)
    assert result == "u123"

def test_extract_participant_no_match():
    filename = "data.json"
    with pytest.raises(IndexError):
        cleaning.extract_participant(filename)

def test_clean_sleep_data_missing_columns(tmp_path):
    # Create DataFrame without optional columns
    df = pd.DataFrame({
        'other_metric': [10, 20, 30, 40]
    })
    file_path = tmp_path / "test_no_columns.csv"
    df.to_csv(file_path, index=False)
    
    result = cleaning.clean_sleep_data(str(file_path))
    
    # Check that the function still works without optional columns
    assert 'other_metric' in result.columns
    assert len(result) == 4  # No rows should be removed

def test_clean_sleep_data_with_invalid_values(tmp_path):
    # Create DataFrame with invalid values
    df = pd.DataFrame({
        'bedtime_mssd': ['1.5', 'invalid', '3.0', '2.5'],
        'daytime_sleep': [100, 'error', 120, 90]
    })
    file_path = tmp_path / "test_invalid.csv"
    df.to_csv(file_path, index=False)
    
    result = cleaning.clean_sleep_data(str(file_path))
    
    # Check that invalid values are handled correctly
    assert len(result) == 3  # Row with invalid values should be removed
    assert all(result['bedtime_mssd'].notna())
    assert all(result['daytime_sleep'].notna())


class PyTestReporter:
    @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self, terminalreporter, exitstatus):
        yield
        
        passed = len(terminalreporter.stats.get('passed', []))
        failed = len(terminalreporter.stats.get('failed', []))
        
        print("\nTest Summary:")
        if failed == 0:
            print(f"All {passed} tests passed successfully!")
        else:
            print(f"Tests passed: {passed}")
            print(f"Tests failed: {failed}")
            print("\nFailed tests:")
            for failure in terminalreporter.stats.get('failed', []):
                print(f"- {failure.nodeid}")

if __name__ == '__main__':
    # Register the custom reporter
    pytest.main([__file__, "-v"], plugins=[PyTestReporter()])