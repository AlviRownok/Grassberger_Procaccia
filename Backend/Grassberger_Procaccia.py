import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .utils_gp import read_from_file


python_GP_data = []  # Empty list that will be filled with fractal dimensions calculated by the Python method

def compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path=None, river_names=None):
    if not python_GP_data:  # Check if the Python GP data list is empty
        if file_path is not None:
            read_from_file(file_path, python_GP_data)  # Read fractal dimensions from the file
        else:
            raise ValueError("No data available and no file path provided")

    if len(fractalyse_GP_data) != len(python_GP_data):
        raise ValueError("Data lists are of unequal length")

    # Calculate the difference between the two lists and round each difference to two decimal places
    diff = [round(el1 - el2, 2) for el1, el2 in zip(fractalyse_GP_data, python_GP_data)]

    if river_names:
        print("Differences between Fractalyse and Python G-P methods:")
        for i, river in enumerate(river_names):
            print(f"{river}: {diff[i]}")
    else:
        print("Differences between Fractalyse and Python G-P methods:", diff)

def plot_correlation_gp_python(list1, name1, file_path="results.csv", river_names=None):
    global python_GP_data  # Ensure this is defined globally or passed appropriately
    if not python_GP_data:  # Check if the data needs to be read
        read_from_file(file_path, python_GP_data)

    if len(python_GP_data) != len(list1):
        raise ValueError("The lists should be of equal length to compute correlation.")

    # Convert lists to pandas Series for easier manipulation and analysis
    y = pd.Series(list1)
    x = pd.Series(python_GP_data)

    # Calculate the Pearson correlation coefficient
    try:
        correlation = y.corr(x)
        print(f"Correlation coefficient: {correlation:.2f}")
    except Exception as e:
        print("Error computing correlation:", str(e))
        return

    # Plotting
    fig, ax = plt.subplots()
    ax.scatter(x, y, label='Rivers')

    if river_names:
        # Annotate points with river names
        for i, txt in enumerate(river_names):
            ax.annotate(txt, (x[i], y[i]), fontsize=8)

    # Fit a linear polynomial (line) to the data and plot
    ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='red', label='Fit Line')

    ax.set_xlabel("Python G-P")
    ax.set_ylabel(name1)
    ax.legend()
    plt.show()
