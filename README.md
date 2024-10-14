# **Fractal Dimension Analysis for River Networks**

This project computes the fractal dimensions of river networks using the **Grassberger-Procaccia** algorithm. The application analyzes fractal structures from image files and compares the results of fractal dimensions calculated using two methods: a custom Python implementation and the Fractalyse tool.

## **Project Overview**

This project performs fractal analysis on river images and computes their fractal dimensions using a modified Grassberger-Procaccia (G-P) method. The application compares fractal dimensions computed by **Fractalyse** and Python-based methods, providing a visual and statistical correlation between them.

Additionally, it processes multiple images from a directory, generating fractal dimension plots and saving them, along with a CSV file containing the computed results for further analysis.

### **Key Features**

- Compute fractal dimensions from river network images using the G-P method.
- Visualize correlation between fractal dimensions calculated using Python and Fractalyse.
- Tkinter-based GUI for user-friendly folder and file selection.
- Automated processing of multiple images.
- Generate visual plots of fractal dimension analysis.

---

## **Prerequisites**

Before you can run the project, ensure you have the following software installed on your system:

1. **Python** (recommended version: Python 3.11 or later)
2. **Virtual Environment** (optional but recommended)

### **Python Packages**

The project depends on several Python packages, which can be installed via `pip` using a `requirements.txt` file (included in the project). Additionally, `Tkinter` is required for the GUI, which might need to be installed separately in some environments.

---

## **Installation Instructions**

Follow these steps to set up the project on your local machine:

### **Step 1: Clone the Project Repository**

Clone the repository or download the project files to your local machine.

```bash
git clone https://github.com/AlviRownok/Grassberger_Procaccia.git
cd Grassberger_Procaccia
```

### **Step 2: Create a Virtual Environment**

Creating a virtual environment is recommended to avoid conflicts with other Python projects.

```bash
python -m venv venv
```

### **Step 3: Activate the Virtual Environment**

- On **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- On **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### **Step 4: Install Dependencies**

With the virtual environment activated, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### **Step 5: Install Tkinter (if necessary)**

On some systems, especially if you're working in a minimal Python installation, `Tkinter` might not be included by default. To install `Tkinter`, you can use:

- On **Windows** and **macOS**, Tkinter is usually bundled with Python. You can check if Tkinter is available by running:

  ```bash
  python -m tkinter
  ```

  If the Tkinter window opens, you're good to go.

- On **Linux**, you may need to install `Tkinter` separately. For Debian-based systems (like Ubuntu), run:

  ```bash
  sudo apt-get install python3-tk
  ```

If you're using a Python distribution without `Tkinter` (rare but possible), you can install it via `pip`:

```bash
pip install tk
```

---

## **Running the Application**

Once you have installed the prerequisites and activated the virtual environment, follow these steps to run the application:

### **Step 1: Activate Virtual Environment**

Activate your virtual environment (if not already active):

```bash
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### **Step 2: Run the Application**

Run the main application script `Grassberger_Procaccia.py`:

```bash
python Grassberger_Procaccia.py
```

### **Step 3: Select Required Files**

The application will open a Tkinter-based file selection dialog for you to choose:

1. The folder containing river network images.
2. The folder where plots should be saved (default is `Outputs` folder if nothing is selected).
3. The text file containing `fractalyse_GP_data`, which contains pre-computed fractal dimensions for comparison (in the format: `river_name;fractal_value`).

After selecting these files, the application will perform fractal analysis and generate the outputs.

---

## **Folder Structure**

Here is the folder structure based on your project:

```
GP/
│
├── Grassberger_Procaccia/
│   ├── __pycache__/              # Python cache folder (auto-generated)
│   ├── Outputs/                  # Folder where the output plots will be saved
│   ├── Test/                     # (Optional) Test files folder
│   ├── venv/                     # Virtual environment folder
│   ├── Grassberger_Procaccia.py   # Main script to run the project
│   ├── ImageFractalDimension_GP.py# Script that handles fractal analysis
│   ├── requirements.txt           # File containing dependencies
│   ├── results.csv                # CSV file containing computed fractal dimensions
│   └── utils_gp.py                # Utility functions for reading and plotting
```

---

## **Example Input and Output**

### **Input Example**

- **Input Folder**: A directory containing `.png` images of river networks.
- **Fractalyse Data File**: A text file structured as follows:

  ```
  Achankovil;0.99
  Aconcagua;1.57
  Adda;1.51
  Adige;1.27
  Aeolis Planum;1.53
  ```

### **Output**

- **Fractal Dimension CSV**: `results.csv` containing the computed fractal dimensions.
- **Plots**: Correlation plots between fractal dimensions computed by Fractalyse and Python methods, saved in the `Outputs/` folder (or the folder you specified).

Example structure of `results.csv`:

```
Filename;Fractal Dimension
river1.png;1.53
river2.png;1.27
...
```

---

## **Explanation of Key Features**

1. **Fractal Dimension Calculation**:
   - The `ImageFractalDimension_GP.py` script performs fractal dimension calculations using a modified Grassberger Procaccia method.
   - It processes each image, binarizes it, extracts points, and computes the fractal dimension.

2. **Correlation Analysis**:
   - `utils_gp.py` handles correlation analysis between Fractalyse and Python results.
   - The script compares the fractal dimensions and plots the results, showing correlations and differences.

3. **Tkinter GUI**:
   - The GUI prompts users to select directories and files, making the process user-friendly.
   - It eliminates the need for hardcoded paths, allowing dynamic selection of input data.

---

## **License**

This project is released under the MIT License. You are free to use, modify, and distribute the code as long as proper attribution is given.

---

## **Conclusion**

This project provides a complete tool for performing fractal analysis on river network images using python and Grassberger Procaccia Algorithm and comparing the results with Fractalyse-calculated dimensions. The tool is flexible, allowing users to input their data through a GUI and generate meaningful outputs like CSV files and correlation plots.

If you encounter any issues or need further assistance, feel free to open an issue or contact us.

---

### **Contributors**

- [Alvi Rownok] - Masters in Data Science, Department of Physics, University of Naples Federico II.

---