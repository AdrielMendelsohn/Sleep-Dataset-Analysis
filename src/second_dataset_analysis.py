
#     Imports
from src import cleaning, plotting

# Variables
sleep_data_file_path = r"data\cmu-sleep.csv"


def create_new_features(data):
    """Creates new features in the given DataFrame:

    1. Adds a 'score' column as a weighted score (0-100), calculated as 25 times 'term_gpa'.
    2. Adds a 'score_scaled' column, which scales 'term_gpa' within each 'study' group to a 0-100 range.
    3. Adds a 'midpoint_sleep_hour' column, transforming 'midpoint_sleep' from minutes to hours in a 24-hour format.

    Parameters:
    data (pd.DataFrame): The input DataFrame containing the columns 'term_gpa', 'study', and 'midpoint_sleep'.

    Returns:
    pd.DataFrame: The DataFrame with new features added.
    """
    # Add a weighted score based on 'term_gpa'
    data["score"] = data["term_gpa"].transform(lambda x: 25 * x)

    # Scale 'term_gpa' within each 'study' group
    data["score_scaled"] = data.groupby("study")["term_gpa"].transform(
        lambda x: 100 * (x - x.min()) / (x.max() - x.min())
    )

    # Transform 'midpoint_sleep' from minutes to hours in 24-hour format
    data["midpoint_sleep_hour"] = data["midpoint_sleep"].transform(lambda x: ((x / 60) + 23) % 24)

    return data


def create_sleep_heatmap(sleep_data, show_choice, save_choice):
    columns_to_keep = ["study", "demo_firstgen", "bedtime_mssd", "TotalSleepTime", "midpoint_sleep",
                        "frac_nights_with_data", "daytime_sleep", "score_scaled"]
    sleep_data_copy = sleep_data[columns_to_keep]
    plotting.plot_correlation_matrix(sleep_data_copy , "Score", show_choice, save_choice)

def create_sleep_scatter_plots(sleep_data, show_choice, save_choice):
    plotting.scatterplot_regression_by_group(sleep_data, "study", "midpoint_sleep", "score", show_choice, save_choice)
    plotting.scatterplot_regression_by_group(sleep_data, "study", "bedtime_mssd", "score", show_choice, save_choice)
    plotting.scatterplot_regression_by_group(sleep_data, "study", "TotalSleepTime", "score", show_choice, save_choice)

def run_full_sleep_analysis(show_choice, save_choice):
    if show_choice or save_choice:
        sleep_data = cleaning.clean_sleep_data(sleep_data_file_path)
        create_new_features(sleep_data)
        create_sleep_heatmap(sleep_data, show_choice, save_choice)
        create_sleep_scatter_plots(sleep_data, show_choice, save_choice)
