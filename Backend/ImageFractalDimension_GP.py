import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from utils_gp import resizeAndPad

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
        distances = pdist(self.points, 'euclidean')
        distance_matrix = squareform(distances)

        # Determine the range of epsilon values, with adjustments
        min_epsilon = np.min(distances[distances > 0]) * 1.01
        max_epsilon = np.max(distances)

        # Generate fewer epsilons across this new range
        epsilons = np.logspace(np.log10(min_epsilon), np.log10(max_epsilon), num=50)  # Playing with the value of num

        # Calculate the correlation sums for each epsilon
        # Convert calculation to use numpy directly for improved memory usage and possibly better performance
        C = np.array([np.sum(distance_matrix < eps) for eps in epsilons], dtype=np.float32) / distance_matrix.size

        # Fit a line to the log-log data to find the slope (correlation dimension)
        log_eps = np.log(epsilons)
        log_C = np.log(C)
        slope, _ = np.polyfit(log_eps, log_C, 1)

        # Return the slope rounded to two decimal places
        return round(slope, 2)


    def graph(self, save=False, **kwargs):
        path = kwargs.get('path', 'output.png')  # Set default path if none provided
        
        distances = pdist(self.points, 'euclidean')
        distance_matrix = squareform(distances)
        min_epsilon = np.min(distances[distances > 0]) * 1.01
        max_epsilon = np.max(distances)
        epsilons = np.logspace(np.log10(min_epsilon), np.log10(max_epsilon), num=50) # Playing with the value of num

        # Ensure C is a floating-point array to handle division properly
        C = np.array([(distance_matrix < eps).sum() for eps in epsilons], dtype=np.float32)
        C /= np.size(distance_matrix)  # Normalize by the total number of elements in the distance matrix

        log_eps = np.log(epsilons)
        log_C = np.log(C)

        plt.figure()
        plt.plot(log_eps, log_C, marker='o')
        plt.xlabel('Log(Epsilon)')
        plt.ylabel('Log(Correlation Sum)')
        plt.title(f"Log-Log Plot of Correlation Sum vs Epsilon\nFractal Dimension: {self.fractal_dim:.2f}")

        if save and path:
            plt.savefig(path)
        plt.close()  # Ensure closure of the figure to free up memory
