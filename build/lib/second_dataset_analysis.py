import cleaning, plotting



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
    """
    Generates a heatmap displaying correlations between selected sleep variables and the target "Grades Score".

    Parameters:
    -----------
    sleep_data : DataFrame
        The input DataFrame containing sleep study data, including various sleep metrics and scores.
        
    show_choice : bool
        If True, the heatmap will be displayed interactively.
        
    save_choice : bool
        If True, the heatmap will be saved to a specified location (the implementation of saving is handled within the plotting module).
    
    Columns Used:
    -------------
    - study : Group identifier for sleep studies.
    - demo_firstgen : Demographic variable for first-generation participants.
    - bedtime_mssd : Mean squared successive differences in bedtime, measuring variability.
    - TotalSleepTime : Total sleep duration in hours.
    - midpoint_sleep : The midpoint of sleep calculated based on bedtime and wake time.
    - frac_nights_with_data : Fraction of nights with complete sleep data.
    - daytime_sleep : Sleep duration during daytime.
    - score_scaled : Scaled version of the score used for correlation analysis.

    Returns:
    --------
    None
        The function triggers plotting but does not return any value.
    """
    columns_to_keep = ["study", "demo_firstgen", "bedtime_mssd", "TotalSleepTime", "midpoint_sleep",
                        "frac_nights_with_data", "daytime_sleep", "score_scaled"]
    sleep_data_copy = sleep_data[columns_to_keep]
    plotting.plot_correlation_matrix(sleep_data_copy , "Grades Score", show_choice, save_choice)

def create_sleep_scatter_plots(sleep_data, show_choice, save_choice):
    """
    Creates scatter plots with regression lines to visualize relationships between sleep metrics and scores, grouped by study.

    Parameters:
    -----------
    sleep_data : DataFrame
        The input DataFrame containing sleep study data, including various sleep metrics and scores.
        
    show_choice : bool
        If True, the scatter plots will be displayed interactively.
        
    save_choice : bool
        If True, the scatter plots will be saved to a specified location (the implementation of saving is handled within the plotting module).

    Scatter Plots Created:
    ----------------------
    - Midpoint of sleep vs. score (grouped by study)
    - Bedtime variability (bedtime_mssd) vs. score (grouped by study)
    - Total sleep time vs. score (grouped by study)

    Returns:
    --------
    None
        The function triggers plotting but does not return any value.
    """
    plotting.scatterplot_regression_by_group(sleep_data, "study", "midpoint_sleep", "score", show_choice, save_choice)
    plotting.scatterplot_regression_by_group(sleep_data, "study", "bedtime_mssd", "score", show_choice, save_choice)
    plotting.scatterplot_regression_by_group(sleep_data, "study", "TotalSleepTime", "score", show_choice, save_choice)

def run_full_sleep_analysis(sleep_dataset_path, show_choice, save_choice):
    """
    Executes the complete sleep analysis pipeline, including data cleaning, feature creation, heatmap generation, and scatter plot creation.

    Parameters:
    -----------
    sleep_dataset_path : str
        The file path to the sleep study dataset (e.g., a CSV or other compatible file).
        
    show_choice : bool
        If True, visualizations (heatmap and scatter plots) will be displayed interactively.
        
    save_choice : bool
        If True, visualizations will be saved to a specified location (the implementation of saving is handled within the plotting module).

    Workflow Steps:
    ---------------
    1. Clean the sleep data using the `clean_sleep_data` function.
    2. Generate new features necessary for analysis using `create_new_features`.
    3. Create a heatmap showing correlations between sleep metrics and the target score.
    4. Create scatter plots showing regression lines between sleep metrics and scores, grouped by study.

    Returns:
    --------
    None
        The function orchestrates the analysis pipeline but does not return any value.
    """
    if show_choice or save_choice:
        sleep_data = cleaning.clean_sleep_data(sleep_dataset_path)
        create_new_features(sleep_data)
        create_sleep_heatmap(sleep_data, show_choice, save_choice)
        create_sleep_scatter_plots(sleep_data, show_choice, save_choice)
