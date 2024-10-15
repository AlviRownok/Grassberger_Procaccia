import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, Canvas, Scrollbar, Label
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk  # To display images
import numpy as np
from sklearn.linear_model import LinearRegression

# Ensure TkAgg backend is used
import matplotlib
matplotlib.use('TkAgg')

from ImageFractalDimension_GP import ImageFractalDimension2
from utils_gp import read_fractalyse_data, read_from_file, compute_diff_between_methods, plot_correlation_gp_python

def normalize_river_name(river_name):
    """Normalize river names by removing extensions and unnecessary parts."""
    river_name = river_name.replace('.png', '')
    river_name = river_name.replace('_', ' ').replace('-', ' ')
    river_name = ''.join([i for i in river_name if not i.isdigit()]).strip()
    return river_name

class GrassbergerProcacciaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grassberger-Procaccia Fractal Dimension Analyzer")
        self.geometry("1200x800")  # Adjusted default window size for larger UI
        self.configure(bg='white')

        # Variables to store file/folder paths
        self.fol_name = ""
        self.plot_fol_name = ""
        self.fractalyse_file_path = ""
        self.results_file_path = ""  # Added variable for results.csv
        self.python_GP_data = []
        self.fractalyse_GP_data = []
        self.progress_var = tk.DoubleVar()

        # Bind the close event (X button) to a custom handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create widgets and layout the interface
        self.create_widgets()

        # Adjust layout when window is maximized
        self.bind("<Configure>", self.on_resize)

    def on_closing(self):
        """Handle window closing event and exit the Python script."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()  # Stops the mainloop
            self.destroy()  # Destroys the window

    def create_widgets(self):
        # Main layout frame
        self.main_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Blue Box: Input buttons
        self.blue_box = tk.Frame(self.main_frame, bg="lightblue", bd=2, relief="groove")
        self.blue_box.place(x=10, y=10, width=350, height=350)
        self.create_input_buttons()

        # Green Bar: Progress bar
        self.green_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.green_bar.place(x=10, y=370, width=350, height=30)

        # Orange Box: Log area
        self.orange_box = tk.Frame(self.main_frame, bg="orange", bd=2, relief="groove")
        self.orange_box.place(x=10, y=410, width=350, height=370)
        self.text_area = tk.Text(self.orange_box, height=10, width=45)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Purple Box: River images and fractal plots
        self.purple_box = tk.Frame(self.main_frame, bg="lightblue", bd=2, relief="groove")
        self.purple_box.place(x=370, y=10, width=800, height=370)
        
        # Split into two parts: one for images, one for fractal plots
        self.image_canvas = tk.Canvas(self.purple_box, bg="white", height=370)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.plot_canvas = tk.Canvas(self.purple_box, bg="white", height=370)
        self.plot_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.slider = ttk.Scale(self.main_frame, orient='horizontal', from_=0, to=10, command=self.update_image_and_plot)
        self.slider.place(x=370, y=390, width=800, height=30)

        # Red Box: Correlation plot
        self.red_box = tk.Frame(self.main_frame, bg="lightcoral", bd=2, relief="groove")
        self.red_box.place(x=370, y=430, width=800, height=350)
        self.figure, self.ax = plt.subplots()
        self.canvas_red_box = FigureCanvasTkAgg(self.figure, master=self.red_box)
        self.canvas_red_box.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_input_buttons(self):
        """Create the input buttons for folder/file selection"""
        ttk.Button(self.blue_box, text="Select Folder with Images", command=self.select_image_folder).pack(pady=5)
        ttk.Button(self.blue_box, text="Select Folder to Save Plots", command=self.select_plot_folder).pack(pady=5)
        ttk.Button(self.blue_box, text="Select Fractalyse Data File", command=self.select_fractalyse_file).pack(pady=5)
        ttk.Button(self.blue_box, text="Select Results File", command=self.select_results_file).pack(pady=5)  # Added results file input
        ttk.Button(self.blue_box, text="Run G-P Analysis", command=self.run_analysis_thread).pack(pady=5)

    def log(self, message):
        """Helper function to log messages in the text area."""
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def select_image_folder(self):
        self.fol_name = filedialog.askdirectory(title="Select Folder Containing Images")
        if self.fol_name:
            self.log(f"Selected image folder: {self.fol_name}")

    def select_plot_folder(self):
        self.plot_fol_name = filedialog.askdirectory(title="Select Folder to Save Plots")
        if self.plot_fol_name:
            self.log(f"Selected plot folder: {self.plot_fol_name}")

    def select_fractalyse_file(self):
        self.fractalyse_file_path = filedialog.askopenfilename(title="Select Fractalyse Data File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.fractalyse_file_path:
            self.log(f"Selected Fractalyse data file: {self.fractalyse_file_path}")

    def select_results_file(self):
        self.results_file_path = filedialog.askopenfilename(title="Select Results File (CSV)", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if self.results_file_path:
            self.log(f"Selected results file: {self.results_file_path}")

    def run_analysis_thread(self):
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.start()

    def run_analysis(self):
        if not self.fol_name or not self.plot_fol_name or not self.results_file_path:
            messagebox.showerror("Error", "Please select image, plot, and results file.")
            return

        try:
            total_images = len([f for f in os.listdir(self.fol_name) if f.endswith(".png")])
            progress_step = 100 / total_images

            # Run analysis and update the results.csv before reading for correlation
            self.runForEveryImageInFolder(self.fol_name, self.plot_fol_name, progress_step)

            if self.fractalyse_file_path:
                self.fractalyse_GP_data = read_fractalyse_data(self.fractalyse_file_path)
                read_from_file(self.results_file_path, self.python_GP_data)

                # Normalize the names in both lists before comparison
                self.python_GP_data = [(normalize_river_name(river), value) for river, value in self.python_GP_data]
                self.fractalyse_GP_data = [(normalize_river_name(river), value) for river, value in self.fractalyse_GP_data]

                # Log the contents of the two lists for debugging
                self.log(f"Python GP Data: {self.python_GP_data}")
                self.log(f"Fractalyse GP Data: {self.fractalyse_GP_data}")

                # Check for mismatched river names
                python_rivers = [river for river, _ in self.python_GP_data]
                fractalyse_rivers = [river for river, _ in self.fractalyse_GP_data]

                if python_rivers != fractalyse_rivers:
                    self.log(f"Mismatch in river names! Python GP rivers: {python_rivers}, Fractalyse rivers: {fractalyse_rivers}")

                compute_diff_between_methods(self.fractalyse_GP_data, self.python_GP_data)
                self.after(0, self.plot_correlation)

            self.log("Analysis complete!")
            self.log(f"Output saved to {self.plot_fol_name}")

        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

    def update_image_and_plot(self, event):
        """Update the displayed image and plot based on the slider"""
        if self.plot_fol_name and self.fol_name:
            image_files = [f for f in os.listdir(self.fol_name) if f.endswith(".png")]
            plot_files = [f for f in os.listdir(self.plot_fol_name) if f.endswith("_plot.png")]
            index = int(self.slider.get())

            if 0 <= index < len(image_files) and index < len(plot_files):
                image_path = os.path.join(self.fol_name, image_files[index])
                plot_path = os.path.join(self.plot_fol_name, plot_files[index])
                self.display_image(image_path)
                self.display_plot(plot_path)

    def display_image(self, image_path):
        """Display the river image in the left side of the purple box"""
        image = Image.open(image_path)
        image = image.resize((400, 370), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(image)
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def display_plot(self, plot_path):
        """Display the fractal plot in the right side of the purple box"""
        plot = Image.open(plot_path)
        plot = plot.resize((400, 370), Image.Resampling.LANCZOS)
        self.plot_tk = ImageTk.PhotoImage(plot)
        self.plot_canvas.create_image(0, 0, anchor="nw", image=self.plot_tk)

    def plot_correlation(self):
        """Plot correlation between Python GP and Fractalyse data in the red box"""
        if len(self.python_GP_data) != len(self.fractalyse_GP_data):
            messagebox.showerror("Error", "The lists should be of equal length to compute correlation.")
            return

        python_values = [value for _, value in self.python_GP_data]
        fractalyse_values = [value for _, value in self.fractalyse_GP_data]

        # Fit a straight line using linear regression for low correlation visualization
        X = np.array(python_values).reshape(-1, 1)
        Y = np.array(fractalyse_values)
        model = LinearRegression()
        model.fit(X, Y)
        Y_pred = model.predict(X)

        self.ax.clear()
        self.ax.scatter(python_values, fractalyse_values, label="Correlation")
        self.ax.plot(python_values, Y_pred, color="red", label="Fit Line")
        self.ax.set_title("Correlation between Python GP and Fractalyse")
        self.ax.set_xlabel("Python G-P")
        self.ax.set_ylabel("Fractalyse")
        self.ax.legend()
        self.canvas_red_box.draw()

    def update_progress(self, increment):
        """Update the progress bar"""
        self.progress_var.set(self.progress_var.get() + increment)

    def runForEveryImageInFolder(self, fol_name, plot_fol_name, progress_step):
        os.makedirs(plot_fol_name, exist_ok=True)
        image_files = [f for f in os.listdir(fol_name) if f.endswith(".png")]
        results_csv_path = self.results_file_path

        with open(results_csv_path, "w") as f:
            f.write("Filename;Fractal Dimension\n")  # Write header

            for i, filename in enumerate(image_files):
                file_path = os.path.join(fol_name, filename)
                self.log(f"Processing: {file_path}")
                save_path = os.path.join(plot_fol_name, filename.replace(".png", "") + "_plot.png")
                curr_fractal = ImageFractalDimension2(file_path, 256)
                fractal_dim = curr_fractal.fractal_dim
                self.log(f"Fractal Dimension: {fractal_dim}")
                curr_fractal.graph(save=True, path=save_path)
                self.update_progress(progress_step)

                # Write the result for this image to the CSV file
                f.write(f"{filename};{fractal_dim}\n")

    def on_resize(self, event):
        """Handle window resize and adjust components accordingly"""
        if event.widget == self:
            self.main_frame.update_idletasks()

if __name__ == '__main__':
    app = GrassbergerProcacciaApp()
    app.mainloop()
