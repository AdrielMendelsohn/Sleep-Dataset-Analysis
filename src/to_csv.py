# Imports
import os

import pandas as pd

from . import cleaning, files_import


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
    filtered_data = combined_data.dropna(subset=[column_to_check])

    if make_csv:
        output_csv = directory_path.split("/")[-1] + "_data.csv"
        filtered_data.to_csv(output_csv, index=True)

    return filtered_data


# Function to process the extracted JSON data and save to a CSV
def json_pd_to_csv(data, output_csv):
    all_data = []  # List to store DataFrames from all subjects

    for file_data in data:
        # Extract subject number from the file name
        subject_number = file_data["file_name"].split("_")[1].split(".")[0]

        # Create a DataFrame from the 'data' key
        df = pd.DataFrame(file_data["data"])

        # Add a subject number column
        df["subject_number"] = subject_number

        # Append to the list of all data
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_csv, index=False)
    print(f"Data from all JSON files has been saved to {output_csv}")

# Function that given files creates a csv with amount of entries per participant per category
# Cleans the files first
def amount_of_entries_csv_simple(datasets, output_csv):
    number_of_entries = {}
    for name, dir_path in datasets.items():
        files = cleaning.clean_data_from_jsons_folder(dir_path)
        for file in files:
            subject = cleaning.extract_participant(file["file_name"])

            if name not in number_of_entries:
                number_of_entries[name] = {}
            number_of_entries[name][subject] = file["record_count"]

    df = pd.DataFrame(number_of_entries)
    df.to_csv(output_csv, index=True)



# Function that given files creates a csv with amount of entries per participant per category
def amount_of_entries_csv(datasets, output_csv):
    # Initialize a dictionary to store the counts of entries for each user across datasets
    user_entry_counts = {}

    # Process each dataset
    for dataset_name, directory_path in datasets.items():
        raw_data = files_import.process_folder(directory_path)

        # Flatten the JSON data
        flat_data = pd.json_normalize(
            raw_data,
            record_path="data",
            meta=["file_name", "record_count"],  # Include top-level metadata
            errors="ignore"
        )

        # Extract user ID from file_name and count entries
        flat_data["user_id"] = flat_data["file_name"].str.extract(r"u(\d+)").fillna("Unknown")
        user_counts = flat_data["user_id"].value_counts()

        # Add counts to the user_entry_counts dictionary
        for user_id, count in user_counts.items():
            if user_id not in user_entry_counts:
                user_entry_counts[user_id] = {}
            user_entry_counts[user_id][dataset_name] = count

    # Convert the user_entry_counts dictionary to a DataFrame
    user_entries_df = pd.DataFrame.from_dict(user_entry_counts, orient="index").fillna(0).astype(int)
    user_entries_df.reset_index(inplace=True)
    user_entries_df.rename(columns={"index": "User ID"}, inplace=True)

    # Save the DataFrame to a CSV file
    user_entries_df.to_csv(output_csv, index=False)
