import numpy as np
from PIL import Image

from utils import load_image


def apply_1d_downsampling(image_array: np.ndarray, num_ribbons: int, ribbon_width: int) -> np.ndarray:
    """
    Downsample an image horizontally

    :param image_array: np.array, 3 channel image
    :param num_ribbons: int, number of ribbons to split the original image
    :param ribbon_width: int, number of columns in the np.ndarray that makes up the ribbon
    :return: np.array
    """
    start_of_ribbons = range(0, ribbon_width * num_ribbons, ribbon_width)

    left_image = []
    right_image = []

    for i, ribbon_start in enumerate(start_of_ribbons):
        ribbon = image_array[:, ribbon_start : ribbon_start + ribbon_width,:]
        if i % 2 == 0:
            right_image.append(ribbon)
        else:
            left_image.append(ribbon)

    image_array = np.hstack([np.hstack(left_image), np.hstack(right_image)])
    return image_array


def apply_downsampling(image_array: np.ndarray, num_ribbons: int=10) -> np.ndarray:
    """
    Downsample an image to 4 smaller images.

    :param image_array: np.array, 3 channel image
    :param num_ribbons: int, number of ribbons to split the original image
    :return: np.array
    """
    if num_ribbons % 2 != 0:
        raise Exception("The number of ribbons must be an even number")
    
    img_w = image_array.shape[1]
    ribbon_width = img_w // num_ribbons

    image_array = apply_1d_downsampling(image_array, num_ribbons, ribbon_width)
    image_array = np.rot90(image_array, 3)

    num_ribbons = img_w // ribbon_width
    image_array = apply_1d_downsampling(image_array, num_ribbons, ribbon_width)

    return np.rot90(image_array)

    

if __name__ == "__main__":

    fname = "daisy_square.jpg"
    img = load_image(fname, color=True)

    transform = apply_downsampling
    new_fname = f"{fname.split('.')[0]}_{transform.__name__}_color.jpg"

    img = transform(img, num_ribbons=60)
    img = Image.fromarray(img)
    img.save(new_fname, quality=100, subsampling=0)