# Imports
import os
import pandas as pd


# Function to turn json files into pandas df and exports a csv file
def folder_to_csv(directory_path, column_to_check, make_csv):
    """
    The `folder_to_csv` function reads JSON files from a given directory, combines them into a single DataFrame,
    filters rows based on a specified column, and optionally exports the result to a CSV file.

    ### Parameters:
    - `directory_path` (str): 
        - The path to the directory containing the JSON files. 
        - Each JSON file is expected to follow a naming convention where a user ID is embedded in the file name.
    - `column_to_check` (str): 
        - The column name used for filtering out rows with missing values (`NaN`). 
        - If the column is not found or the combined data is empty, the function returns an empty DataFrame.
    - `make_csv` (bool): 
        - If `True`, the filtered DataFrame is saved as a CSV file in the same directory.
        - The CSV file is named based on the directory name with the suffix `_data.csv`.

    ### Returns:
    - `pd.DataFrame`: 
        - A DataFrame containing the combined and filtered data from all JSON files in the directory.

    ### Example Usage:
    ```python
    # Example: Combining JSON files in a directory and exporting filtered results to a CSV file
    filtered_df = folder_to_csv("/path/to/json_directory", "target_column", make_csv=True)
    """
    
    combined_data = pd.DataFrame()

    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".json"):
            user_id = file_name.split("_")[1].split(".")[0]
            file_path = os.path.join(directory_path, file_name)
            data = pd.read_json(file_path)
            data.insert(0, "User", user_id) # Add the user ID as the first column
            combined_data = pd.concat([combined_data, data], ignore_index=True)
    

    if combined_data.empty or column_to_check not in combined_data.columns:
        return pd.DataFrame()  # Returns an empty DataFrame if there is no data or if the column does not exist


    filtered_data = combined_data.dropna(subset=[column_to_check])

    if make_csv:
        output_csv = directory_path.split("/")[-1] + "_data.csv"
        filtered_data.to_csv(output_csv, index=True)

    return filtered_data

