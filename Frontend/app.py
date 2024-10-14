# app.py
import streamlit as st
import sys
import os
import pandas as pd
import zipfile
import io

# Add the parent directory to sys.path to access the Backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the backend modules
from Backend.ImageFractalDimension_GP import runForEveryImageInFolder
from Backend.Grassberger_Procaccia import plot_correlation_gp_python, compute_diff_between_methods
from Backend.utils_gp import read_from_file

# Now you can use st in your code
st.title('Fractal Dimension Analysis')

# Get the absolute path to the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Paths to 'Test' and 'Outputs' directories
test_dir = os.path.join(parent_dir, 'Test')
outputs_dir = os.path.join(parent_dir, 'Outputs')  # Updated from 'Output' to 'Outputs'

# Ensure the directories exist
if not os.path.isdir(test_dir):
    st.error(f"The directory {test_dir} does not exist.")
else:
    # Get the list of subdirectories inside 'Test' directory
    image_folders = [name for name in os.listdir(test_dir)
                     if os.path.isdir(os.path.join(test_dir, name))]
    if image_folders:
        # Step 1: Allow user to select folder containing the images
        image_folder_name = st.selectbox('Select the folder containing the images:', image_folders)
        image_folder = os.path.join(test_dir, image_folder_name)
    else:
        st.error(f"No subdirectories found in {test_dir}")
        image_folder = ''

# For the plot folder, since Outputs has no subfolders
if not os.path.isdir(outputs_dir):
    st.error(f"The directory {outputs_dir} does not exist.")
else:
    st.info(f"Plots will be saved in the Outputs folder: {outputs_dir}")
    plot_folder = outputs_dir  # Use the Outputs directory directly

# Step 2: Select the fractalyse_GP_data.txt file from the Test directory
txt_files = [f for f in os.listdir(test_dir) if f.endswith('.txt')]
if txt_files:
    fractalyse_file_name = st.selectbox('Select the fractalyse_GP_data.txt file:', txt_files)
    fractalyse_file_path = os.path.join(test_dir, fractalyse_file_name)
else:
    st.error(f"No .txt files found in {test_dir}")
    fractalyse_file_path = ''

# Step 3: Select the results.csv file from the Outputs directory
csv_files = [f for f in os.listdir(outputs_dir) if f.endswith('.csv')]
if csv_files:
    results_file_name = st.selectbox('Select the results.csv file:', csv_files)
    results_file_path = os.path.join(outputs_dir, results_file_name)
else:
    st.error(f"No .csv files found in {outputs_dir}")
    results_file_path = ''

# Initialize variables to store data
fractalyse_GP_data = []
river_names = []
python_GP_data = []

# Handle fractalyse file selection
if fractalyse_file_path and os.path.exists(fractalyse_file_path):
    with open(fractalyse_file_path, 'r') as file:
        content = file.readlines()
        for line in content:
            if line.strip():  # Skip empty lines
                parts = line.strip().split(';')
                if len(parts) == 2:
                    river_names.append(parts[0])
                    fractalyse_GP_data.append(float(parts[1]))
                else:
                    st.error(f"Invalid format in line: {line}")
else:
    st.error('Please select a valid fractalyse_GP_data.txt file.')

# Step 4: Button to run the calculations and plotting
if st.button('Run Analysis'):
    if image_folder and plot_folder:
        # Run the fractal dimension calculations
        runForEveryImageInFolder(image_folder, plot_folder)

        # Read the results file (python_GP_data) and compute differences
        if results_file_path and os.path.exists(results_file_path):
            python_GP_data = []
            read_from_file(results_file_path, python_GP_data)

            if fractalyse_GP_data and python_GP_data:
                compute_diff_between_methods(fractalyse_GP_data, python_GP_data, results_file_path, river_names)
                plot_correlation_gp_python(fractalyse_GP_data, 'Fractalyse G-P', results_file_path, river_names)
                st.success('Analysis completed and plots generated!')

                # Provide download link for updated results.csv
                updated_results_path = os.path.join(plot_folder, 'results.csv')
                if os.path.exists(updated_results_path):
                    with open(updated_results_path, 'rb') as f:
                        st.download_button(
                            label='Download Updated results.csv',
                            data=f,
                            file_name='results.csv',
                            mime='text/csv'
                        )

                # Zip the plots and provide a download link
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for root, dirs, files in os.walk(plot_folder):
                        for file in files:
                            if file.endswith('_plot.png'):
                                file_path = os.path.join(root, file)
                                zip_file.write(file_path, arcname=file)
                zip_buffer.seek(0)
                st.download_button(
                    label='Download Plots as ZIP',
                    data=zip_buffer,
                    file_name='plots.zip',
                    mime='application/zip'
                )

            else:
                st.error('Fractalyse data and Python G-P data are required for comparison.')
        else:
            st.error('Please select a valid results.csv file.')
    else:
        st.error('Please select a valid image folder.')
