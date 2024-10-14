import sys
import os

# Add the parent directory to sys.path to access the Backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the backend modules
from Backend.ImageFractalDimension_GP import runForEveryImageInFolder
from Backend.Grassberger_Procaccia import plot_correlation_gp_python, compute_diff_between_methods
from Backend.utils_gp import read_from_file


# Function to parse the txt file with river names and fractal dimensions
def parse_fractalyse_file(file):
    fractalyse_GP_data = []
    river_names = []
    
    # Read the file line by line
    for line in file:
        name, value = line.decode("utf-8").strip().split(';')
        river_names.append(name)  # Extract river names
        fractalyse_GP_data.append(float(value))  # Extract and convert fractal dimensions to float
    
    return river_names, fractalyse_GP_data


# Streamlit UI
st.title('Fractal Dimension Analysis')

# Step 1: Allow user to input folders and file paths
image_folder = st.text_input('Enter the folder path containing the images:')
plot_folder = st.text_input('Enter the folder path to save plots:')

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
    river_names, fractalyse_GP_data = parse_fractalyse_file(fractalyse_file)

# Step 4: Button to run the calculations and plotting
if st.button('Run Analysis'):
    # Run the fractal dimension calculations
    if image_folder and plot_folder:
        runForEveryImageInFolder(image_folder, plot_folder)

    # Read the results file (python_GP_data) and compute differences
    if results_file:
        python_GP_data = []
        file_path = results_file.name
        read_from_file(file_path, python_GP_data)
        
        if fractalyse_GP_data and python_GP_data:
            compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path, river_names)
            plot_correlation_gp_python(fractalyse_GP_data, 'Fractalyse G-P', file_path, river_names)

    st.success('Analysis completed and plots generated!')
