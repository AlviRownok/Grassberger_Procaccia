import cv2
import numpy as np

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


def read_from_file(file_path, python_GP_data):
    with open(file_path, "r") as file:
        lines = file.readlines()  # read the lines of the file
        for line in lines[1:]:  # for each line in the file, starting from the second line (header)
            fractal_dimension = round(float(line.split(';')[1].strip()), 2)
            python_GP_data.append(fractal_dimension)
