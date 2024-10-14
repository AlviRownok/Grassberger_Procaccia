import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import pandas as pd  # Needed for correlation computation

def read_fractalyse_data(file_path):
    fractalyse_GP_data = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            # Each line is in the format: Name;Value
            parts = line.strip().split(';')
            if len(parts) == 2:
                try:
                    fractal_dimension = float(parts[1])
                    fractalyse_GP_data.append(fractal_dimension)
                except ValueError:
                    print(f"Could not parse fractal dimension in line: {line}")
            else:
                print(f"Invalid line format: {line}")
    return fractalyse_GP_data

def read_from_file(file_path, python_GP_data):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read the lines of the file
        for line in lines[1:]:  # for each line in the file, starting from the second line (header)
            #Extract the value, convert to float, round to two decimal places, and append to the list
            fractal_dimension = round(float(line.strip().split(';')[1]), 2)
            python_GP_data.append(fractal_dimension)

def compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path=None, fractalyse_file_path=None):
    if not python_GP_data:  # Check if the Python GP data list is empty
        if file_path is not None:
            read_from_file(file_path, python_GP_data)  # Read fractal dimensions from the file
        else:
            raise ValueError("No data available and no file path provided")

    if not fractalyse_GP_data:  # Check if fractalyse_GP_data is empty
        if fractalyse_file_path is not None:
            fractalyse_GP_data = read_fractalyse_data(fractalyse_file_path)
        else:
            raise ValueError("No fractalyse data available and no file path provided")

    if len(fractalyse_GP_data) != len(python_GP_data):
        raise ValueError("Data lists are of unequal length")

    # Calculate the difference between the two lists and round each difference to two decimal places
    diff = [round(el1 - el2, 2) for el1, el2 in zip(fractalyse_GP_data, python_GP_data)]

    print("Differences between Fractalyse and Python G-P methods:")
    print(diff)

def plot_correlation_gp_python(list1, name1, file_path="results.csv"):
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
        print("Correlation coeff: ", correlation)
    except Exception as e:
        print("Error computing correlation:", str(e))
        return

    # Plotting
    plt.title('Correlation between {} and Python G-P'.format(name1))
    plt.scatter(x, y, label='Rivers')
    # Fit a linear polynomial (line) to the data and plot
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='red', label='Fit Line')

    plt.xlabel("Python G-P")
    plt.ylabel(name1)
    plt.legend()

    plt.show()

def resizeAndPad(img, p_h, p_w, padColor=255):
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
