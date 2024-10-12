import os
from ImageFractalDimension_GP import ImageFractalDimension2
from utils_gp import *

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
    # fol_name = "C:\\Users\\alvirownok\\Downloads\\Fracture Analysis Project Mariarca, Prof Max and Prof Longo\\G_P\\All rivers"
    # fol_name = "C:\\Users\\alvirownok\\Downloads\\Fracture Analysis Project Mariarca, Prof Max and Prof Longo\\Materiale per Maria\\Images\\Manually extracted 131 imgs\\"
    # fol_name = "C:\\Users\\alvirownok\\Downloads\\Fracture Analysis Project Mariarca, Prof Max and Prof Longo\\extraterrestrial rivers\\Mars"
    fol_name = r"C:\Users\alvirownok\Downloads\Fracture Analysis Project Mariarca, Prof Max and Prof Longo\G_P\Brazil\Resized"
    plot_fol_name = "plots/"

    if not os.path.exists(plot_fol_name):
        os.makedirs(plot_fol_name)

    runForEveryImageInFolder(fol_name, plot_fol_name)
    
    # Path to your data file
    file_path = "C:\\Users\\alvirownok\\Downloads\\Fracture Analysis Project Mariarca, Prof Max and Prof Longo\\G_P\\results.csv"

    read_from_file(file_path, python_GP_data)

    # Use the function to compute differences
    compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path)

    # Now plot the correlation
    plot_correlation_gp_python(fractalyse_GP_data, 'Fractalyse G-P', file_path)

if __name__ == '__main__':
    main()