import pytest
import json
import pandas as pd
import os
import sys

# Add the src directory to sys.path dynamically
repo_root = os.path.dirname(os.path.abspath(__file__))  
src_path = os.path.join(repo_root, "..", "src")         
sys.path.append(src_path)
from files_import import analyze_text, analyze_csv, analyze_json, process_folder

# Test fixtures
@pytest.fixture
def setup_test_files(tmp_path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("This is a test file with some words")
    
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })
    df.to_csv(csv_file, index=False)
    
    json_file = tmp_path / "test.json"
    json_data = [
        {"id": 1, "name": "Test1"},
        {"id": 2, "name": "Test2"}
    ]
    json_file.write_text(json.dumps(json_data))
    
    return tmp_path

def test_analyze_text(setup_test_files):
    file_path = setup_test_files / "test.txt"
    result = analyze_text(str(file_path))
    
    assert result['file_name'] == "test.txt"
    assert result['word_count'] == 8

def test_analyze_csv(setup_test_files):
    file_path = setup_test_files / "test.csv"
    result = analyze_csv(str(file_path))
    
    assert result['file_name'] == "test.csv"
    assert result['row_count'] == 3
    assert result['column_count'] == 2
    assert 'summary' in result

def test_analyze_json(setup_test_files):
    file_path = setup_test_files / "test.json"
    result = analyze_json(str(file_path))
    
    assert result['file_name'] == "test.json"
    assert result['record_count'] == 2
    assert result['keys'] == ['id', 'name']
    assert len(result['data']) == 2

def test_process_folder(setup_test_files):
    results = process_folder(str(setup_test_files))
    assert len(results) == 3
    
    file_names = [result['file_name'] for result in results]
    assert 'test.txt' in file_names
    assert 'test.csv' in file_names
    assert 'test.json' in file_names

def test_unsupported_file(setup_test_files):
    unsupported_file = setup_test_files / "test.xyz"
    unsupported_file.write_text("some content")
    
    results = process_folder(str(setup_test_files))
    unsupported_result = next(result for result in results if result['file_name'] == 'test.xyz')
    assert unsupported_result['error'] == 'Unsupported file type'

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        analyze_text("nonexistent.txt")

def test_invalid_json(setup_test_files):
    invalid_json = setup_test_files / "invalid.json"
    invalid_json.write_text("{invalid json}")
    
    with pytest.raises(json.JSONDecodeError):
        analyze_json(str(invalid_json))

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