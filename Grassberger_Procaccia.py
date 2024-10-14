import os
from ImageFractalDimension_GP import ImageFractalDimension2
from utils_gp import *
import tkinter as tk
from tkinter import filedialog

def runForEveryImageInFolder(fol_name, plot_fol_name):
    os.makedirs(plot_fol_name, exist_ok=True)  # Ensure the plot folder exists
    with open("results.csv", "w") as f:  # Use 'w' to overwrite existing or use 'a' to append
        f.write("Filename;Fractal Dimension\n")  # Write the header to the CSV file

        for filename in os.listdir(fol_name):
            if filename.endswith(".png"):
                file_path = os.path.join(fol_name, filename)
                print(file_path)  # Print the full path of the file

                save_path = os.path.join(plot_fol_name, filename.replace(".png", "") + "_plot.png")
                # Initialize ImageFractalDimension2
                curr_fractal = ImageFractalDimension2(file_path, 256)
                print(curr_fractal.fractal_dim)  # Print the calculated fractal dimension

                f.write(filename.split('.')[0] + ";" + str(curr_fractal.fractal_dim) + "\n")  # Write to CSV

                # Save the plot with a modified file name to include "_plot"
                curr_fractal.graph(save=True, path=save_path)

def main():
    global python_GP_data  # Ensure that python_GP_data is accessible
    python_GP_data = []  # Empty list that will be filled with fractal dimensions calculated by the Python method

    # Use tkinter to get the folder containing images
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask user to select the folder containing images
    fol_name = filedialog.askdirectory(title="Select Folder Containing Images")
    if not fol_name:
        print("No folder selected.")
        return

    # Ask user to select the folder to save plots
    plot_fol_name = filedialog.askdirectory(title="Select Folder to Save Plots")
    if not plot_fol_name:
        print("No plot folder selected. Using default 'plots/'")
        plot_fol_name = "plots/"

    if not os.path.exists(plot_fol_name):
        os.makedirs(plot_fol_name)

    runForEveryImageInFolder(fol_name, plot_fol_name)

    # Ask user to select the file containing fractalyse_GP_data
    fractalyse_file_path = filedialog.askopenfilename(title="Select Fractalyse Data File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not fractalyse_file_path:
        print("No Fractalyse data file selected.")
        return

    # Read fractalyse_GP_data from the file
    fractalyse_GP_data = read_fractalyse_data(fractalyse_file_path)

    # Path to your data file (results.csv)
    file_path = "results.csv"  # Assuming results.csv is in the current directory

    read_from_file(file_path, python_GP_data)

    # Use the function to compute differences
    compute_diff_between_methods(fractalyse_GP_data, python_GP_data)

    # Now plot the correlation
    plot_correlation_gp_python(fractalyse_GP_data, 'Fractalyse G-P', file_path)

if __name__ == '__main__':
    main()
