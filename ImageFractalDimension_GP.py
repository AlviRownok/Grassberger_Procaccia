# ImageFractalDimension_GP.py

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from utils_gp import resizeAndPad
import cv2
import io

class ImageFractalDimension2:
    def __init__(self, image_name, SIZE):
        self.SIZE = SIZE
        image = cv2.imread(image_name)
        if image.shape[0] != image.shape[1] or image.shape[0] != SIZE:
            image = resizeAndPad(image, SIZE, SIZE, padColor=255)

        self.img_px_array = np.asarray(image, dtype=np.uint8)  # Ensure image array is uint8 for cv2 operations
        self.binarizeImg()
        self.extractPoints()
        self.fractal_dim = self.calculate_fractal_dim()

    def binarizeImg(self):
        # Iterate over each pixel in the image array
        rows, cols = self.img_px_array.shape[:2]
        for i in range(rows):
            for j in range(cols):
                if len(self.img_px_array.shape) == 3:  # Check if the image is color (3 channels)
                    # Assume all channels must be 255 for the pixel to be considered "white"
                    if np.all(self.img_px_array[i, j] == 255):
                        self.img_px_array[i, j] = 0  # Set all channels to 0
                    else:
                        self.img_px_array[i, j] = 1  # Set all channels to 1
                else:  # Grayscale image
                    if self.img_px_array[i, j] == 255:
                        self.img_px_array[i, j] = 0
                    else:
                        self.img_px_array[i, j] = 1

    def extractPoints(self):
        # Extract points where the pixel value is 1 (foreground)
        if len(self.img_px_array.shape) == 3:  # If color image, check only one channel
            self.points = np.column_stack(np.where(self.img_px_array[:, :, 0] == 1))
        else:  # If grayscale image
            self.points = np.column_stack(np.where(self.img_px_array == 1))

    def calculate_fractal_dim(self):
        # Compute the pairwise distances between points
        self.distances = pdist(self.points, 'euclidean')
        self.distance_matrix = squareform(self.distances)

        # Determine the range of epsilon values, with adjustments
        min_epsilon = np.min(self.distances[self.distances > 0]) * 1.01
        max_epsilon = np.max(self.distances)

        # Generate fewer epsilons across this new range
        self.epsilons = np.logspace(np.log10(min_epsilon), np.log10(max_epsilon), num=50)  # Adjust num as needed

        # Calculate the correlation sums for each epsilon
        self.C = np.array([np.sum(self.distance_matrix < eps) for eps in self.epsilons], dtype=np.float32) / self.distance_matrix.size

        # Fit a line to the log-log data to find the slope (correlation dimension)
        self.log_eps = np.log(self.epsilons)
        self.log_C = np.log(self.C)
        slope, _ = np.polyfit(self.log_eps, self.log_C, 1)

        # Return the slope rounded to two decimal places
        return round(slope, 2)

    def graph(self, save=False, **kwargs):
        path = kwargs.get('path', 'output.png')  # Set default path if none provided

        # Use the data computed during calculate_fractal_dim
        plt.figure()
        plt.plot(self.log_eps, self.log_C, marker='o')
        plt.xlabel('Log(Epsilon)')
        plt.ylabel('Log(Correlation Sum)')
        plt.title(f"Log-Log Plot of Correlation Sum vs Epsilon\nFractal Dimension: {self.fractal_dim:.2f}")

        if save and path:
            plt.savefig(path)
        plt.close()  # Ensure closure of the figure to free up memory