import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import pandas as pd  # Needed for correlation computation
import csv

def read_fractalyse_data(file_path):
    """Read fractalyse data from the file and return a sorted list of tuples (river, fractal_value)."""
    fractalyse_GP_data = []
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if len(row) == 2:
                river, fractal_value = row[0], float(row[1])
                fractalyse_GP_data.append((river, fractal_value))
            else:
                print(f"Invalid line format: {row}")
    # Sort the data by river name
    return sorted(fractalyse_GP_data, key=lambda x: x[0])

def read_from_file(file_path, python_GP_data):
    """Read Python GP data from the results.csv and return a sorted list of tuples (river, fractal_value)."""
    python_GP_data.clear()  # Make sure the list is empty before reading
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Skip the header
        for row in reader:
            if len(row) == 2:
                river, fractal_value = row[0], round(float(row[1]), 2)
                python_GP_data.append((river, fractal_value))
    # Sort the data by river name
    return sorted(python_GP_data, key=lambda x: x[0])

def compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path=None, fractalyse_file_path=None):
    """Compute the difference between fractalyse GP and Python GP data, ensuring both lists are sorted and aligned."""
    if not python_GP_data:  # Check if the Python GP data list is empty
        if file_path is not None:
            python_GP_data = read_from_file(file_path, python_GP_data)  # Read and sort Python GP data
        else:
            raise ValueError("No data available and no file path provided")

    if not fractalyse_GP_data:  # Check if fractalyse_GP_data is empty
        if fractalyse_file_path is not None:
            fractalyse_GP_data = read_fractalyse_data(fractalyse_file_path)  # Read and sort Fractalyse data
        else:
            raise ValueError("No fractalyse data available and no file path provided")

    # Check if the lengths match
    if len(fractalyse_GP_data) != len(python_GP_data):
        raise ValueError("Data lists are of unequal length even after sorting")

    # Calculate the difference between the two lists and log discrepancies if river names do not match
    differences = []
    for (river_f, fractal_value_f), (river_p, fractal_value_p) in zip(fractalyse_GP_data, python_GP_data):
        if river_f != river_p:
            raise ValueError(f"Rivers do not match: {river_f} vs {river_p}")
        differences.append(round(fractal_value_f - fractal_value_p, 2))

    print("Differences between Fractalyse and Python G-P methods:")
    print(differences)
    return differences

def plot_correlation_gp_python(fractalyse_GP_data, python_GP_data, file_path="results.csv"):
    """Plot correlation between Python GP and Fractalyse data after sorting and alignment."""
    if not python_GP_data:  # Check if the data needs to be read
        python_GP_data = read_from_file(file_path, python_GP_data)

    if len(python_GP_data) != len(fractalyse_GP_data):
        raise ValueError("The lists should be of equal length to compute correlation.")

    # Extract only the fractal values (after sorting and alignment by river name)
    python_values = [fractal_value for _, fractal_value in python_GP_data]
    fractalyse_values = [fractal_value for _, fractal_value in fractalyse_GP_data]

    # Calculate the Pearson correlation coefficient
    y = pd.Series(fractalyse_values)
    x = pd.Series(python_values)

    try:
        correlation = y.corr(x)
        print("Correlation coeff: ", correlation)
    except Exception as e:
        print("Error computing correlation:", str(e))
        return

    # Plotting
    plt.title('Correlation between Fractalyse and Python G-P')
    plt.scatter(x, y, label='Rivers')
    # Fit a linear polynomial (line) to the data and plot
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='red', label='Fit Line')

    plt.xlabel("Python G-P")
    plt.ylabel("Fractalyse")
    plt.legend()

    plt.show()

def resizeAndPad(img, p_h, p_w, padColor=255):
    """Resize and pad an image to fit the specified dimensions."""
    h, w = img.shape[:2]
    interp = cv2.INTER_AREA if max(h, w) > max(p_h, p_w) else cv2.INTER_CUBIC

    # Calculate new height and width to maintain aspect ratio
    aspect_ratio = w / h
    target_aspect_ratio = p_w / p_h

    if target_aspect_ratio >= aspect_ratio:
        new_h = p_h
        new_w = int(new_h * aspect_ratio)
    else:
        new_w = p_w
        new_h = int(new_w / aspect_ratio)

    # Calculate padding values
    pad_vert = (p_h - new_h) // 2
    pad_horz = (p_w - new_w) // 2

    pad_top = pad_vert
    pad_bot = p_h - new_h - pad_top
    pad_left = pad_horz
    pad_right = p_w - new_w - pad_left

    # Convert padColor to the correct format if it isn't already
    if isinstance(padColor, int):
        padColor = [padColor] * 3 if len(img.shape) == 3 else padColor

    # Resize and pad the image
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right,
                                    cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img
