# Imports
import os
import pandas as pd
import re
import json


# Function to process text files
def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        word_count = len(re.findall(r'\w+', content))
    return {
        'file_name': os.path.basename(file_path),
        'word_count': word_count
    }

# Function to process CSV files
def analyze_csv(file_path):
    df = pd.read_csv(file_path)
    return {
        'file_name': os.path.basename(file_path),
        'row_count': len(df),
        'column_count': len(df.columns),
        'summary': df.describe().to_dict()
    }

# Function to process JSON files
def analyze_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Load the JSON data
    return {
        'file_name': os.path.basename(file_path),
        'record_count': len(data),
        'keys': list(data[0].keys()) if data else [],
        'data': data  # Add the full JSON data here
    }

# Function to process whole folder
def process_folder(folder_path):
    results = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Check if it's a file
        if os.path.isfile(file_path):
            if file_name.endswith('.txt'):
                result = analyze_text(file_path)
            elif file_name.endswith('.csv'):
                result = analyze_csv(file_path)
            elif file_name.endswith('.json'):
                result = analyze_json(file_path)
            else:
                result = {
                    'file_name': file_name,
                    'error': 'Unsupported file type'
                }
            results.append(result)
    return results
