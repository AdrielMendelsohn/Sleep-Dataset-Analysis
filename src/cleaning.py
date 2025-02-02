import re
import numpy as np
import pandas as pd

def drop_blanks_and_nulls(data):

    """
    The `drop_blanks_and_nulls` function cleans a given DataFrame by handling missing values and removing incomplete data.

    ### Parameters:
    - `data` (pd.DataFrame): 
        - The input DataFrame potentially containing blank strings or null values.

    ### Returns:
    - `pd.DataFrame`: 
        - The cleaned DataFrame with blank strings replaced by NaN and rows containing missing values dropped.
    """
    # Replace blank strings with NaN and drop rows with missing values
    data = data.replace(r"^\s*$", np.nan, regex=True)
    data = data.dropna()
    return data

def extract_participant(filename):
    """
    The `extract_participant` function identifies and extracts the participant ID from the given filename using a specific pattern.

    ### Parameters:
    - `filename` (str): 
        - The name of the file containing a participant ID in the format `u<number>`, e.g., `data_u123.csv`.

    ### Returns:
    - `str`: 
        - The participant ID found within the filename.

    ### Raises:
    - `Exception`: 
        - Raised if multiple participant IDs are detected in the filename.
    """
    matches = re.findall(r"u\d+(?=\.)", filename)
    if len(matches)>1:
        raise Exception("Multiple participants in name")
    return matches[0]

def clean_sleep_data(file_path):
    """Cleans the sleep data from a given CSV file by performing the following steps:
    
    1. Reads the data from the specified CSV file.
    2. Drops the 'cohort' column.
    3. Replaces blank values with NaN and removes rows containing blanks or nulls.
    4. Converts all columns to numeric, coercing invalid parsing to NaN.
    5. Removes outliers based on specific thresholds for 'bedtime_mssd' and 'daytime_sleep'.

    Parameters:
    file_path (str): Path to the CSV file containing the data.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
    # Read the data
    data = pd.read_csv(file_path)

    # Drop the 'cohort' column
    if "cohort" in data.columns:
        data = data.drop("cohort", axis=1)

    # Replace blanks with NaN and drop rows with blanks or nulls
    data = data.replace(r"^\s*$", pd.NA, regex=True)  # Replace blanks with NaN
    data = data.dropna()  # Remove rows with NaN values

    # Convert all columns to numeric, coercing invalid values to NaN
    data = data.apply(pd.to_numeric, errors="coerce")

    # Remove outliers based on thresholds
    if "bedtime_mssd" in data.columns:
        data = data[data["bedtime_mssd"] <= 5]
    if "daytime_sleep" in data.columns:
        data = data[data["daytime_sleep"] <= 150]

    return data
