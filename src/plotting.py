#     Imports
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress



def plot_correlation_matrix(data, name):
    """
    Computes and plots a heatmap of the correlation matrix for a given DataFrame.

    Parameters:
    - data: pandas DataFrame containing the dataset.

    Returns:
    None
    """
    # Compute the correlation matrix
    correlation_matrix = data.corr()

    # Plot the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title(name +' Feature Correlation')
    plt.tight_layout()
    plt.savefig("results/" + name + " Feature Correlation.png", dpi = 300)
    plt.show()


def scatterplot_regression_by_group(data, group_col, x_col, y_col):
    """
    Creates a single scatterplot with different colors and regression lines for each group in the dataset, and saves as .png.

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

    for group, color in zip(groups, palette):
        group_data = data[data[group_col] == group]

        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = linregress(group_data[x_col], group_data[y_col])

        # Scatterplot
        sns.scatterplot(
            data=group_data, x=x_col, y=y_col, color=color, label=f'Group {group}', s=50, alpha=0.4
        )

        # Regression line
        x_vals = group_data[x_col]
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color=color, linestyle='--', label=f'{group} Regression (r={r_value:.2f}, P value={p_value:.3f}), STD error={std_err:.2f}')

    plt.title(x_col + ' and ' + y_col + 'Scatter Plot', fontsize=16)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.legend(title="Groups", fontsize=10, title_fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("results/" + x_col + " " + y_col + " Scatter Plot.png", dpi = 300)
    plt.show()