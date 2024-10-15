# **Grassberger-Procaccia Algorithm for Fractal Analysis in Geographic River Networks**

This dedicated application is built for researchers in the field of geographic analysis, focusing on the classification and fractal analysis of river networks. The application employs the **Grassberger-Procaccia (G-P) Algorithm**, a well-known method for determining the fractal dimension of a set of points, which is particularly useful in analyzing complex, non-linear systems such as river networks. This tool allows users to compute the fractal dimensions of river images, facilitating the comparison between Python-based results and those from the **Fractalyse** tool.

## **Theoretical Overview: Grassberger-Procaccia Algorithm**

The Grassberger-Procaccia algorithm (G-P) was first introduced in 1983 by Peter Grassberger and Itamar Procaccia to compute the fractal dimension of strange attractors in chaotic systems. The algorithm is widely used to calculate the **correlation dimension**, a specific type of fractal dimension that quantifies how the number of pairs of points within a given distance scales as the distance itself varies.

### **Mathematical Foundations**

The G-P algorithm is based on the idea that, for a fractal object, the number of pairs of points separated by a distance less than or equal to `ε` (epsilon) scales as a power law with respect to `ε`. More formally:

$$
C(\epsilon) = \frac{2}{N(N-1)} \sum_{i=1}^{N} \sum_{j=i+1}^{N} \Theta(\epsilon - ||X_i - X_j||)
$$

Where:
- $N$ is the number of points.
- $$ X_i $$ and $$ X_j $$ are two points in the dataset.
- $$ ||X_i - X_j|| $$ is the Euclidean distance between two points.
- $$ \Theta $$ is the Heaviside step function, which counts the number of pairs of points that are closer than $$ \epsilon $$.

The function $$ C(\epsilon) $$ represents the **correlation sum**, which counts how many pairs of points have a distance smaller than $$ \epsilon $$. The correlation dimension $$ D_2 $$ can be estimated by analyzing the slope of the log-log plot of $$ C(\epsilon) $$ versus $$ \epsilon $$:

$$
D_2 = \lim_{\epsilon \to 0} \frac{d \log C(\epsilon)}{d \log \epsilon}
$$

This slope is the fractal dimension of the system, and it reveals the self-similarity of the system at different scales.

### **Fractal Dimension in Geographic River Systems**

In geographic analysis, river networks can be considered as fractal structures due to their self-similarity across different scales. The fractal dimension provides insight into the complexity and distribution of river channels. By applying the Grassberger-Procaccia algorithm, this tool calculates the fractal dimensions of various river networks, aiding in the classification and analysis of river patterns.

### **Key Features of the Grassberger-Procaccia Algorithm:**
1. **Correlation Dimension**: The core output of the algorithm, measuring the fractal complexity.
2. **Log-Log Plot**: A visualization that helps identify the linear region from which the correlation dimension is extracted.
3. **Multiscale Analysis**: The G-P algorithm is ideal for studying natural systems that exhibit self-similar patterns, such as river networks.

For further theoretical details, refer to the original paper by Grassberger and Procaccia or this comprehensive [scholarpedia article](http://www.scholarpedia.org/article/Grassberger-Procaccia_algorithm).

---

## **Application Overview**

This application implements the Grassberger-Procaccia algorithm to perform fractal analysis on river network images, making it a powerful tool for geographic research. It processes multiple images from a directory, calculating the fractal dimension of each and comparing the results with those from the **Fractalyse** tool. 

### **Key Features**

- **Fractal Dimension Calculation**: Computes the correlation dimension using the Grassberger-Procaccia algorithm from river network images.
- **Correlation with Fractalyse**: Compares results from Python-based calculations with pre-calculated fractal dimensions obtained via the Fractalyse tool.
- **Tkinter GUI**: A user-friendly graphical interface that allows researchers to easily select directories and files for processing.
- **Batch Processing**: Automates the analysis of multiple images, generating visual plots and saving them to a designated output folder.

---

## **Prerequisites**

Before you can run the application, ensure you have the following installed:

1. **Python** (recommended version: Python 3.11 or later)
2. **Tkinter** (for the GUI, may require separate installation on some systems)
3. **Virtual Environment** (optional but recommended)

### **Python Packages**

The necessary Python packages can be installed using `pip` and the provided `requirements.txt` file. These packages include `numpy`, `scipy`, `matplotlib`, `pandas`, and `opencv-python`.

---

## **Installation Instructions**

Follow these steps to set up the application:

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/AlviRownok/Grassberger_Procaccia.git
cd Grassberger_Procaccia
```

### **Step 2: Set Up a Virtual Environment**

```bash
python -m venv venv
```

### **Step 3: Activate the Virtual Environment**

- **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### **Step 4: Install Required Libraries**

```bash
pip install -r requirements.txt
```

### **Step 5: Install Tkinter (if necessary)**

Tkinter is usually bundled with Python on **Windows** and **macOS**. If you're on **Linux**, or if Tkinter is not available, install it with:

```bash
sudo apt-get install python3-tk  # For Debian-based Linux systems
```

---

## **Running the Application**

### **Step 1: Activate Virtual Environment**

```bash
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### **Step 2: Run the Application**

```bash
python Grassberger_Procaccia.py
```

### **Step 3: Select Required Files**

The application will prompt you to select:
1. A folder containing river network images.
2. A folder to save the output plots.
3. A text file containing `fractalyse_GP_data`, structured as `river_name;fractal_value`.

---

## **Folder Structure**

```
GP/
│
├── Grassberger_Procaccia/
│   ├── __pycache__/              # Python cache folder (auto-generated)
│   ├── Outputs/                  # Folder where output plots will be saved
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
- **Fractalyse Data File**: A text file structured as:

  ```
  Achankovil;0.99
  Aconcagua;1.57
  Adda;1.51
  ```

### **Output**

- **Fractal Dimension CSV**: `results.csv` containing computed fractal dimensions.
- **Correlation Plots**: Saved in the `Outputs/` folder, showing correlations between Python and Fractalyse results.

---

## **License**

This project is licensed under the MIT License. For details, refer to the [LICENSE.md](./LICENSE.md) file.

---

## **Citations**

This application and its methodology are cited in:

> Grassberger, P., & Procaccia, I. (1983). "Characterization of strange attractors." *Physical Review Letters, 50(5)*, 346–349.

The work presented at the European Planetary Science Congress (EPSC2024) is cited as:

> D'Aniello, M., Zampella, M. R., Dosi, A., Rownok, A., Delli Veneri, M., Ettari, A., Cavuoti, S., Sannino, L., Brescia, M., Donadio, C., & Longo, G. (2024). Rivers' classification: Integrating deep learning and statistical techniques for terrestrial and extraterrestrial drainage networks analysis. *European Planetary Science Congress 2024*.

---