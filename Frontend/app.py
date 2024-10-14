# app.py
import streamlit as st
import sys
import os

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

# Paths to 'Test' and 'Output' directories
test_dir = os.path.join(parent_dir, 'Test')
output_dir = os.path.join(parent_dir, 'Output')

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

# For the plot folder, since Output has no subfolders
if not os.path.isdir(output_dir):
    st.error(f"The directory {output_dir} does not exist.")
else:
    st.info(f"Plots will be saved in the Output folder: {output_dir}")
    plot_folder = output_dir  # Use the Output directory directly

# Step 2: Upload the fractalyse_GP_data list as a text file
fractalyse_file = st.file_uploader('Upload fractalyse_GP_data.txt file (RiverName;Value format)', type=['txt'])

# Step 3: Upload the results CSV file for correlation
results_file = st.file_uploader('Upload results.csv file', type=['csv'])

# Initialize variables to store data
fractalyse_GP_data = []
river_names = []
python_GP_data = []

# Handle fractalyse file upload
if fractalyse_file:
    # Read and parse the fractalyse_GP_data file
    content = fractalyse_file.read().decode('utf-8').splitlines()
    for line in content:
        if line.strip():  # Skip empty lines
            parts = line.strip().split(';')
            if len(parts) == 2:
                river_names.append(parts[0])
                fractalyse_GP_data.append(float(parts[1]))
            else:
                st.error(f"Invalid format in line: {line}")

# Step 4: Button to run the calculations and plotting
if st.button('Run Analysis'):
    if image_folder and plot_folder:
        # Run the fractal dimension calculations
        runForEveryImageInFolder(image_folder, plot_folder)

        # Read the results file (python_GP_data) and compute differences
        if results_file:
            python_GP_data = []
            # Save the uploaded results.csv file temporarily
            with open('results.csv', 'wb') as f:
                f.write(results_file.read())

            read_from_file('results.csv', python_GP_data)

            if fractalyse_GP_data and python_GP_data:
                compute_diff_between_methods(fractalyse_GP_data, python_GP_data, 'results.csv', river_names)
                plot_correlation_gp_python(fractalyse_GP_data, 'Fractalyse G-P', 'results.csv', river_names)
                st.success('Analysis completed and plots generated!')
            else:
                st.error('Fractalyse data and Python G-P data are required for comparison.')
        else:
            st.error('Please upload the results.csv file for correlation.')
    else:
        st.error('Please select a valid image folder.')
