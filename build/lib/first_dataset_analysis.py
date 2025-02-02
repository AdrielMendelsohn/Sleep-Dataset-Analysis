import matplotlib.pyplot as plt
import pandas as pd
import plotly.figure_factory as ff
import plotly.io as pio
import seaborn as sns
from plotting import plot_correlation, plot_correlation_matrix

def make_interactive_heat_map(df):
    """
    Creates an interactive heatmap using plotly
    """
    pio.renderers.default = "iframe_connected"
    df_numeric = df.drop(columns=["User"])
    correlation_matrix = df_numeric.corr()
    fig = ff.create_annotated_heatmap(
        z=correlation_matrix.values,
        x=list(df_numeric.columns),
        y=list(df_numeric.columns),
        colorscale="RdBu",
        annotation_text=correlation_matrix.round(2).values
    )
    fig.write_html("results/plot.html")

def plot_all_correlations(df, show_choice, save_choice):
    """
    Plots all specified correlations
    """
    # Define all correlation pairs
    correlations = [
        ("avg_working_percentage", "gpa_all"),
        ("avg_workout_per_day", "gpa_all"),
        ("stressed_percentage", "gpa_all"),
        ("avg_sad_rating", "gpa_all"),
        ("avg_sleep_rating", "happy_percentage"),
        ("avg_sleep_rating", "avg_stress_level"),
        ("number_of_people", "avg_happy_rating"),
        ("stressed_percentage", "avg_workout_per_day"),
        ("happy_percentage", "avg_workout_per_day"),
        ("avg_sleep_rating", "gpa_13s"),
        ("avg_sleep_hours", "gpa_13s")
    ]
    
    # Plot individual correlations
    for x, y in correlations:
        plot_correlation(df, x, y, show_choice=show_choice, save_choice=save_choice)

def run_full_data_analysis(file_path="data/output.xlsx", show_choice=0, save_choice=0):
    """
    Main function to run the complete data analysis
    
    Parameters:
    -----------
    file_path : str
        Path to the Excel file containing the data
    show_choice : int
        Whether to display the plots (0: no, 1: yes)
    save_choice : int
        Whether to save the plots (0: no, 1: yes)
    """
    df = pd.read_excel(file_path)
    
    if save_choice:
        make_interactive_heat_map(df) # Create corraletoins interactive heatmap
    if show_choice or save_choice:
        plot_correlation_matrix(df,"Students life", show_choice, save_choice) # Create corraletoins regular heatmap
        plot_all_correlations(df, show_choice, save_choice)