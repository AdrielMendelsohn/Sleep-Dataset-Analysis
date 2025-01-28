import re

import numpy as np
import pandas as pd

from . import files_import


def clean_data_from_jsons_folder(folder_path):
    # הפעלת הפונקציה לעיבוד התיקייה
    results = files_import.process_folder(folder_path)

    # ניקוי הנתונים
    for student in results:
        if "data" in student:
           # סינון הנתונים כך שלא יכילו ערכים עם המפתח 'null'
            student["data"] = [obj for obj in student["data"] if "null" not in obj]
        if "record_count" in student:
            # update relevant record_count
            student["record_count"] = len(student["data"])

    # החזרת המידע הנקי
    return results


def drop_blanks_and_nulls(data):
    # Replace blank strings with NaN and drop rows with missing values
    data = data.replace(r"^\s*$", np.nan, regex=True)
    data = data.dropna()
    return data

def extract_participant(filename):
    matches = re.findall(r"u\d+(?=\.)", filename)
    if len(matches)>1:
        raise Exception("Multiple participants in name")
    return matches[0]

def clean_sleep_data(file_path):
    """Cleans the data from a given CSV file by performing the following steps:
    
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
