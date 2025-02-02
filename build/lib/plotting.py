#     Imports
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress


def plot_correlation_matrix(data, name, show_choice, save_choice):
    """
    Computes and plots a heatmap of the correlation matrix for a given dataset to visualize relationships between features.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input dataset containing numerical features for which the correlation matrix will be calculated. 
        If a "User" column is present, it will be excluded from the analysis.

    name : str
        The title to be displayed on the heatmap, typically describing the context or target variable being analyzed.

    show_choice : bool
        If True, the heatmap will be displayed interactively.

    save_choice : bool
        If True, the heatmap will be saved to the "results" directory as a PNG image.

    Function Workflow:
    ------------------
    1. Drops the "User" column if it exists, to ensure only numerical columns are used.
    2. Computes the correlation matrix using `data.corr()`.
    3. Creates a heatmap with color coding based on correlation strength using the "coolwarm" colormap.
    4. Adds annotations to display correlation values within the heatmap.
    5. Saves the plot to `results/{name} Feature Correlation.png` if `save_choice` is True.
    6. Displays the plot interactively if `show_choice` is True; otherwise, it closes the plot.

    Returns:
    --------
    None
        The function generates a plot but does not return any values.

    Example:
    --------
    >>> plot_correlation_matrix(data, "Sleep Data", show_choice=True, save_choice=False)
    """
    if "User" in data.columns: # Only use the numeric columns
        data = data.drop(columns=["User"])
    # Compute the correlation matrix
    correlation_matrix = data.corr()

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title(name +" Feature Correlation")
    plt.tight_layout()
    if save_choice:
        plt.savefig(f"results/{name} Feature Correlation.png", dpi = 300)
    if show_choice:
        plt.show()
    else:
        plt.close()


def plot_correlation(df, x, y, title=None, ax=None, show_choice=False, save_choice=False):
    """
    Creates a correlation plot between two variables
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The input dataframe containing the data
    x : str
        Name of the x-axis variable
    y : str
        Name of the y-axis variable
    title : str, optional
        Custom title for the plot
    ax : matplotlib.axes.Axes, optional
        The axes to plot on. If None, creates a new figure
    show_choice : bool
        Whether to display the plot
    save_choice : bool
        Whether to save the plot
    
    Returns:
    --------
    matplotlib.axes.Axes
        The axes object containing the plot
    """
    # Create new figure if no axes provided
    if ax is None:
        plt.figure(figsize=(8, 6))
        ax = plt.gca()
    
    # Create the regression plot
    sns.regplot(x=x, y=y, data=df, ax=ax)
    
    # Calculate and display correlation
    correlation = df[[x, y]].corr().iloc[0, 1]
    ax.text(0.05, 0.9, f"Correlation: {correlation:.2f}", 
            transform=ax.transAxes, fontsize=12, 
            bbox=dict(facecolor="white", alpha=0.5))
    
    # Set title
    if title is None:
        title = f"{y} vs {x}"
    ax.set_title(title)
    
    # Save if requested and it's a standalone plot
    if save_choice and ax.figure.number == plt.gcf().number:
        filename = f"results/{y} vs {x} Correlation.png"
        plt.savefig(filename, dpi=300)
    
    # Show if requested and it's a standalone plot
    if show_choice and ax.figure.number == plt.gcf().number:
        plt.show()
    elif not show_choice and ax.figure.number == plt.gcf().number:
        plt.close()
    
    return ax

def scatterplot_regression_by_group(data, group_col, x_col, y_col, show_choice, save_choice):
    """Creates a single scatterplot with different colors and regression lines for each group in the dataset, and saves as .png.

    Parameters:
    - data: pandas DataFrame containing the dataset.
    - group_col: Name of the column representing the groups.
    - x_col: Name of the column for the x-axis variable.
    - y_col: Name of the column for the y-axis variable.

    Returns:
    None
    """
    plt.figure(figsize=(10, 6))

    groups = data[group_col].unique()
    palette = sns.color_palette("husl", len(groups))

    for group, color in zip(groups, palette, strict=False):
        group_data = data[data[group_col] == group]

        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = linregress(group_data[x_col], group_data[y_col])

        # Scatterplot
        sns.scatterplot(
            data=group_data, x=x_col, y=y_col, color=color, label=f"Group {group}", s=50, alpha=0.4
        )

        # Regression line
        x_vals = group_data[x_col]
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color=color, linestyle="--", label=f"{group} Regression (r={r_value:.2f}, P value={p_value:.3f}), STD error={std_err:.2f}")

    plt.title(x_col + " and " + y_col + "Scatter Plot", fontsize=16)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.legend(title="Groups", fontsize=10, title_fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()

    if save_choice:
        plt.savefig(f"results/{x_col} {y_col} Scatter Plot.png", dpi = 300)
    if show_choice:
        plt.show()
    else:
        plt.close()
