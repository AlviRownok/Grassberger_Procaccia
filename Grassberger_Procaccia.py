import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, Canvas, Scrollbar, Label
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk  # To display images
import numpy as np

# Ensure TkAgg backend is used
import matplotlib
matplotlib.use('TkAgg')

# Dummy imports for the analysis (replace these with your actual functions)
from ImageFractalDimension_GP import ImageFractalDimension2
from utils_gp import read_fractalyse_data, read_from_file, compute_diff_between_methods, plot_correlation_gp_python


class GrassbergerProcacciaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grassberger-Procaccia Fractal Dimension Analyzer")
        self.geometry("1000x700")
        self.configure(bg='white')

        # Variables to store file/folder paths
        self.fol_name = ""
        self.plot_fol_name = ""
        self.fractalyse_file_path = ""
        self.python_GP_data = []
        self.fractalyse_GP_data = []
        self.progress_var = tk.DoubleVar()

        # Bind the close event (X button) to a custom handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create widgets and layout the interface
        self.create_widgets()

        # Data for plots and logs
        self.xdata = []
        self.ydata = []

    def on_closing(self):
        """Handle window closing event and exit the Python script."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()  # Stops the mainloop
            self.destroy()  # Destroys the window

    def create_widgets(self):
        # Main layout frame (to help with positioning boxes)
        self.main_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Blue Box: Area for input buttons
        self.blue_box = tk.Frame(self.main_frame, bg="lightblue", bd=2, relief="groove")
        self.blue_box.place(x=10, y=10, width=350, height=300)

        # Create input buttons inside Blue Box
        self.create_input_buttons()

        # Green Bar: Progress bar for computation status
        self.green_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate", variable=self.progress_var)
        self.green_bar.place(x=10, y=320, width=350, height=30)

        # Orange Box: Area for displaying individual computational outputs (log area)
        self.orange_box = tk.Frame(self.main_frame, bg="orange", bd=2, relief="groove")
        self.orange_box.place(x=10, y=360, width=350, height=300)

        # Text widget inside Orange Box for logs
        self.text_area = tk.Text(self.orange_box, height=10, width=45)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Purple Box: Area for fractal dimension plots with slider
        self.purple_box = tk.Frame(self.main_frame, bg="lightblue", bd=2, relief="groove")
        self.purple_box.place(x=370, y=10, width=600, height=300)

        # Add a canvas for images and a scrollbar inside Purple Box
        self.plot_canvas = tk.Canvas(self.purple_box, bg="white")
        self.plot_canvas.pack(fill=tk.BOTH, expand=True)

        self.slider = ttk.Scale(self.purple_box, orient='horizontal', from_=0, to=10, command=self.update_image)
        self.slider.pack(fill=tk.X, padx=10, pady=5)

        # Red Box: Area for the correlation plot between Python GP and Fractalyse
        self.red_box = tk.Frame(self.main_frame, bg="lightcoral", bd=2, relief="groove")
        self.red_box.place(x=370, y=320, width=600, height=350)

        # Placeholder for correlation plot in Red Box
        self.figure, self.ax = plt.subplots()
        self.canvas_red_box = FigureCanvasTkAgg(self.figure, master=self.red_box)
        self.canvas_red_box.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_input_buttons(self):
        """Create the input buttons for folder/file selection"""
        ttk.Button(self.blue_box, text="Select Folder with Images", command=self.select_image_folder).pack(pady=5)
        ttk.Button(self.blue_box, text="Select Folder to Save Plots", command=self.select_plot_folder).pack(pady=5)
        ttk.Button(self.blue_box, text="Select Fractalyse Data File", command=self.select_fractalyse_file).pack(pady=5)
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

    def run_analysis_thread(self):
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.start()

    def run_analysis(self):
        if not self.fol_name or not self.plot_fol_name:
            messagebox.showerror("Error", "Please select image and plot folders.")
            return

        try:
            total_images = len([f for f in os.listdir(self.fol_name) if f.endswith(".png")])
            progress_step = 100 / total_images

            self.runForEveryImageInFolder(self.fol_name, self.plot_fol_name, progress_step)

            if self.fractalyse_file_path:
                self.fractalyse_GP_data = read_fractalyse_data(self.fractalyse_file_path)
                file_path = "results.csv"
                read_from_file(file_path, self.python_GP_data)
                compute_diff_between_methods(self.fractalyse_GP_data, self.python_GP_data)
                self.plot_correlation()

            self.log("Analysis complete!")
            self.log(f"Output saved to {self.plot_fol_name}")

        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

    def update_progress(self, increment):
        self.progress_var.set(self.progress_var.get() + increment)

    def runForEveryImageInFolder(self, fol_name, plot_fol_name, progress_step):
        os.makedirs(plot_fol_name, exist_ok=True)
        image_files = [f for f in os.listdir(fol_name) if f.endswith(".png")]
        for i, filename in enumerate(image_files):
            file_path = os.path.join(fol_name, filename)
            self.log(f"Processing: {file_path}")
            save_path = os.path.join(plot_fol_name, filename.replace(".png", "") + "_plot.png")
            curr_fractal = ImageFractalDimension2(file_path, 256)
            self.log(f"Fractal Dimension: {curr_fractal.fractal_dim}")
            curr_fractal.graph(save=True, path=save_path)
            self.update_progress(progress_step)

            # Display the first image as an example
            if i == 0:
                self.display_image(save_path)

    def display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((600, 300), Image.Resampling.LANCZOS)  # Fixed attribute error
        self.img_tk = ImageTk.PhotoImage(image)
        self.plot_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def update_image(self, event):
        """Update the displayed image based on the slider"""
        if self.plot_fol_name:
            image_files = [f for f in os.listdir(self.plot_fol_name) if f.endswith("_plot.png")]
            index = int(self.slider.get())
            if 0 <= index < len(image_files):
                image_path = os.path.join(self.plot_fol_name, image_files[index])
                self.display_image(image_path)

    def plot_correlation(self):
        """Plot correlation between Python GP and Fractalyse data in the red box"""
        self.ax.clear()
        self.ax.plot(self.python_GP_data, self.fractalyse_GP_data, 'o-', label="Correlation")
        self.ax.set_title("Correlation between Python GP and Fractalyse")
        self.ax.set_xlabel("Python G-P")
        self.ax.set_ylabel("Fractalyse")
        self.ax.legend()
        self.canvas_red_box.draw()


if __name__ == '__main__':
    app = GrassbergerProcacciaApp()
    app.mainloop()
