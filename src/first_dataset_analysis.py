import matplotlib.pyplot as plt
import pandas as pd
import plotly.figure_factory as ff
import plotly.io as pio
import seaborn as sns


def make_interactive_heat_map(df):
    pio.renderers.default = "iframe_connected"
    # Removing the "User" column because it is not numeric
    df_numeric = df.drop(columns=["User"])
    # Calculation of the correlation matrix
    correlation_matrix = df_numeric.corr()
    # Create an interactive heat map
    fig = ff.create_annotated_heatmap(
        z=correlation_matrix.values,
        x=list(df_numeric.columns),
        y=list(df_numeric.columns),
        colorscale="RdBu",
        annotation_text=correlation_matrix.round(2).values
    )
    fig.write_html("results/plot.html")

def make_regular_heat_map(df, show_choice, save_choice):
    # Removes ID column
    if "User" in df.columns:
        df = df.drop(columns=["User"])
    # Checking correlations
    correlation_matrix = df.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    if save_choice:
        plt.savefig("results/Full Data Correlation Matrix.png", dpi = 300)
    if show_choice:
        plt.show()
    else:
        plt.close()

def plot_gpa_correlations(df, show_choice, save_choice):
    # Correlation between gpa_all and (avg_working_percentage, avg_workout_per_day, stressed_percentage, avg_sad_rating)
    gpa_factors = ["avg_working_percentage", "avg_workout_per_day", "stressed_percentage", "avg_sad_rating"]
    for factor in gpa_factors:
        plt.figure(figsize=(8, 6))
        sns.regplot(x="gpa_all", y=factor, data=df)
        correlation = df[["gpa_all", factor]].corr().iloc[0, 1]
        plt.text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
        plt.title(f"GPA vs {factor}")
        if save_choice:
            plt.savefig(f"results/GPA vs {factor} Correlation.png", dpi = 300)
        if show_choice:
            plt.show()
        else:
            plt.close()

def plot_sleep_correlations(df, show_choice, save_choice):
    # Correlation between avg_sleep_rating and (happy_percentage, avg_stress_level)
    sleep_factors = ["happy_percentage", "avg_stress_level"]
    for factor in sleep_factors:
        plt.figure(figsize=(8, 6))
        sns.regplot(x="avg_sleep_rating", y=factor, data=df)
        correlation = df[["avg_sleep_rating", factor]].corr().iloc[0, 1]
        plt.text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
        plt.title(f"sleep rating vs {factor}")
        if save_choice:
            plt.savefig(f"results/sleep rating vs {factor} Correlation.png", dpi = 300)
        if show_choice:
            plt.show()
        else:
            plt.close()

def plot_more_correlations(df, show_choice, save_choice):
    # Other promising correlations
    # Correlation between number_of_people and avg_happy_rating
    plt.figure(figsize=(8, 6))
    sns.regplot(x="number_of_people", y="avg_happy_rating", data=df)
    correlation = df[["number_of_people", "avg_happy_rating"]].corr().iloc[0, 1]
    plt.text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
    plt.title("avg_happy_rating vs number_of_people")
    if save_choice:
        plt.savefig("results/avg_happy_rating vs number_of_people Correlation.png", dpi = 300)
    if show_choice:
        plt.show()
    else:
        plt.close()

    # Correlation between avg_workout_per_day and (stressed_percentage, happy_percentage)
    workout_factors = ["stressed_percentage", "happy_percentage"]
    for factor in workout_factors:
        plt.figure(figsize=(8, 6))
        sns.regplot(x=factor, y="avg_workout_per_day", data=df)
        correlation = df[[factor, "avg_workout_per_day"]].corr().iloc[0, 1]
        plt.text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
        plt.title(f"avg_workout_per_day vs {factor}")
        if save_choice:
            plt.savefig(f"results/sleep avg_workout_per_day vs {factor} Correlation.png", dpi = 300)
        if show_choice:
            plt.show()
        else:
            plt.close()


    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    # Graph 1: correlation between gpa_13s and avg_sleep_rating
    sns.regplot(x="avg_sleep_rating", y="gpa_13s", data=df, ax=axes[0])
    correlation = df[["avg_sleep_rating", "gpa_13s"]].corr().iloc[0, 1]
    axes[0].text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=axes[0].transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
    axes[0].set_title("GPA vs Sleep Quality")
    # Graph 2: correlation between gpa_13s and avg_sleep_hours
    sns.regplot(x="avg_sleep_hours", y="gpa_13s", data=df, ax=axes[1])
    correlation = df[["avg_sleep_hours", "gpa_13s"]].corr().iloc[0, 1]
    axes[1].text(0.05, 0.9, f"Correlation: {correlation:.2f}", transform=axes[1].transAxes, fontsize=12, bbox=dict(facecolor="white", alpha=0.5))
    axes[1].set_title("GPA vs Sleep Hours")
    plt.tight_layout()
    if save_choice:
        plt.savefig(f"results/GPA vs Sleep Hours and Sleep Quality Correlation.png", dpi = 300)
    if show_choice:
        plt.show()
    else:
        plt.close()

def run_full_data_analysis(file_path = "data/output.xlsx", show_choice = 0, save_choice = 0):
    # Default - looks for "output.xlsx" in the directory, doesn't save or show
    df = pd.read_excel(file_path)
    # plot all graphs:
    if save_choice:
        make_interactive_heat_map(df)
    if show_choice or save_choice:
        make_regular_heat_map(df, show_choice, save_choice)
        plot_gpa_correlations(df, show_choice, save_choice)
        plot_sleep_correlations(df, show_choice, save_choice)
        plot_more_correlations(df, show_choice, save_choice)
