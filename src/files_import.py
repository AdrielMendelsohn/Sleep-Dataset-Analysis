# Imports
import os
import pandas as pd


# Function to turn json files into pandas df and exports a csv file
def folder_to_csv(directory_path, column_to_check, make_csv):
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

