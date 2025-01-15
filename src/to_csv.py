# Imports
import pandas as pd
from . import files_import


# Function to process the extracted JSON data and save to a CSV
def json_pd_to_csv(data, output_csv):
    all_data = []  # List to store DataFrames from all subjects

    for file_data in data:
        # Extract subject number from the file name
        subject_number = file_data['file_name'].split('_')[1].split('.')[0]

        # Create a DataFrame from the 'data' key
        df = pd.DataFrame(file_data['data'])

        # Add a subject number column
        df['subject_number'] = subject_number

        # Append to the list of all data
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(output_csv, index=False)
    print(f"Data from all JSON files has been saved to {output_csv}")


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
        flat_data["user_id"] = flat_data["file_name"].str.extract(r'u(\d+)').fillna('Unknown')
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