import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# All Rivers

# fractalyse_GP_data = [
#     0.99, # Achankovil
#     1.57, # Aconcagua
#     1.51, # Adda
#     1.27, # Adige
#     1.53, # Aeolis Planum
#     1.95, # Al- Abiadh
#     1.64, # Amazon
#     1.37, # Amur
#     1.95, # AnjaniandJhiri
#     1.52, # Arabia Quadrangle
#     1.35, # Arno
#     1.36, # Baholomeo
#     1.50, # Bangga
#     1.32, # Basento
#     1.43, # Bharathappuzha
#     1.05, # BioBio
#     1.59, # Blanchard
#     1.34, # Boquet
#     1.42, # Bradano
#     1.51, # Bunta
#     1.45, # Candelaro
#     1.45, # Captina
#     1.28, # Chalakudy
#     1.37, # Chaliyar
#     1.43, # Chari
#     1.19, # Chryse Planitia
#     1.63, # Congo
#     1.42, # Cusus Valles
#     1.58, # Danube
#     1.49, # Devoll
#     1.49, # Dniester
#     1.62, # Don
#     1.33, # Drin
#     1.52, # Eberswalde Delta
#     1.51, # Eberswalde Delta2
#     1.54, # Ebro
#     1.48, # Efesto Fossae
#     0.56, # Elqui
#     1.22, # Eufrate
#     1.38, # Gale
#     1.41, # Ganges
#     1.32, # Huang He
#     1.25, # Huasco
#     1.37, # Huygens_Hellas_craters
#     1.32, # Idice
#     1.42, # Indus
#     1.57, # Indus Valley
#     1.29, # Isonzo
#     1.49, # Itata
#     1.62, # Jharkhand
#     1.61, # Jordan
#     1.48, # Kadalundi
#     1.76, # Kadvi
#     1.37, # Kallada
#     1.49, # Karamana
#     1.57, # Karuvannur
#     1.43, # Kaveri
#     1.22, # Kentucky
#     1.30, # Kolyma
#     1.32, # Krishna
#     1.62, # Kuttiyadi
#     1.38, # Lena
#     1.38, # Liri
#     1.43, # Lockras Valley
#     1.47, # Loire
#     1.31, # Luni
#     1.39, # Ma_adim Vallis 1
#     1.08, # Ma_adim Vallis 2
#     1.50, # Mackenze
#     1.56, # Mahe
#     1.34, # Maipo
#     1.50, # Malino
#     0.86, # Manimala
#     1.60, # Maule
#     1.48, # Meenachil
#     1.29, # Mekong
#     1.39, # Meuse
#     1.56, # Mississipi
#     1.30, # Missouri
#     1.31, # Moreau
#     1.23, # Muvattupuhza
#     1.30, # Nagkton Vallei
#     1.39, # Neyyar
#     1.56, # Niger
#     1.44, # Nile
#     1.21, # Nirgal Vallei
#     1.27, # Ob
#     1.20, # Oder
#     1.40, # Ohio
#     1.30, # Olenek
#     1.36, # Ombrone
#     1.66, # Orr
#     1.38, # Osuga Vallei
#     1.69, # Ottawa
#     1.10, # Pamba
#     1.50, # Paraguay
#     1.41, # Parana
#     1.41, # Parana Vallei
#     1.44, # Periyar
#     1.54, # Petrace
#     1.41, # Piave
#     1.41, # Pinamula
#     1.36, # Pinios
#     1.46, # Po
#     1.36, # Powder
#     1.50, # Rapel
#     1.39, # Rhine
#     1.60, # Rhone
#     1.39, # Russian
#     1.23, # Sabarmati
#     1.57, # Saitama
#     1.64, # SaludaReedy
#     1.49, # SanJoaquin
#     1.28, # Sava
#     1.34, # Schiapparelli crater
#     1.48, # Seine
#     1.44, # Simeto
#     1.50, # Singkoyo
#     1.52, # Snake
#     1.46, # StJoseph
#     1.66, # Susquehanna
#     1.48, # Tambun
#     1.41, # Tanaro
#     1.70, # Tarali
#     1.40, # Terra Cimeria 1
#     1.42, # Terra Cimeria 2
#     1.56, # Tevere
#     1.46, # Thames
#     1.24, # Ticino
#     1.18, # Tigri
#     1.36, # Titan 1 (Titan2)
#     1.50, # Titan 2 (Titanoriver)
#     1.42, # Toaya
#     1.37, # Tobol
#     1.56, # Turkey
#     1.38, # Tyras Vallei
#     1.63, # Umbro
#     1.21, # Uruguay
#     1.50, # Vamanapuram
#     1.53, # Varuna
#     1.37, # Vergas
#     1.53, # Vishwamitri
#     1.33, # Vistula
#     1.19, # Vjosa
#     1.01, # Volfe-Bell Canyon
#     1.34, # Volga
#     1.54, # Volturno
#     1.65, # Wabash
#     1.27, # WadiQuena
#     1.54, # Warrego Valles 1
#     1.43,  # Warrego Valles 2
#     1.58, # Wheeling
#     1.68, # Wyoming
#     1.43, # Yangtze
#     1.36, # Yellowstone
#     1.33, # Yenisey
#     1.41  # Zambezi
# ]

# Only Mars rivers

#fractalyse_GP_data = [
    #1.53, # Aeolis Planum
    #1.52, # Arabia Quadrangle
    #1.19, # Chryse Planitia
    #1.42, # Cusus Valles
    #1.52, # Eberswalde Delta
    #1.51, # Eberswalde Delta2
    #1.48, # Efesto Fossae
    #1.38, # Gale
    #1.37, # Huygens_Hellas_craters
    #1.57, # Indus Valley
    #1.43, # Lockras Valley
    #1.39, # Ma_adim Vallis 1
    #1.08, # Ma_adim Vallis 2
    #1.30, # Nagkton Vallei
    #1.21, # Nirgal Vallei
    #1.38, # Osuga Vallei
    #1.41, # Parana Vallei
    #1.34, # Schiapparelli crater
    #1.40, # Terra Cimeria 1
    #1.42, # Terra Cimeria 2
    #1.36, # Titan 1 (Titan2)
    #1.50, # Titan 2 (Titanoriver)
    #1.38, # Tyras Vallei
    #1.54, # Warrego Valles 1
    #1.43  # Warrego Valles 2
#]

# Brazil rivers

fractalyse_GP_data = [
    0.00, # Paraíba do Sul
    0.00, # São Francisco
    0.00, # Jequitinhonha
]

python_GP_data = []  # Empty list that will be filled with fractal dimensions calculated by the Python method

def read_from_file(file_path, python_GP_data):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read the lines of the file
        for line in lines[1:]:  # for each line in the file, starting from the second line (header)
            #Extract the value, convert to float, round to two decimal places, and append to the list
            fractal_dimension = round(float(line.split(';')[1].strip()), 2)
            python_GP_data.append(fractal_dimension)
            
            
#def read_from_file(file_path, python_GP_data):
    #with open(file_path, "r") as file:
        #lines = file.readlines()  # read the lines of the file
        #for line in lines[1:]:  # for each line in the file, starting from the second line (header)
            # Extract the value, convert to float, and append to the list without rounding
            #fractal_dimension = float(line.split(';')[1].strip())
            #python_GP_data.append(fractal_dimension)


def compute_diff_between_methods(fractalyse_GP_data, python_GP_data, file_path=None):
    if not python_GP_data:  # Check if the Python GP data list is empty
        if file_path is not None:
            read_from_file(file_path, python_GP_data)  # Read fractal dimensions from the file
        else:
            raise ValueError("No data available and no file path provided")

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
