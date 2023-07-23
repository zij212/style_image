import numpy as np
from PIL import Image


def load_image(file_dir, color=True):
    """
    Load jpeg image into numpy array

    :param file_dir: location of the image file
    :param color: boolean, load the image as color or 3 channel black and white image
    :return: np.array
    """

    if color:
        img_array = np.array(Image.open(file_dir))
    else:
        img_array = np.array(Image.open(file_dir).convert('L').convert('RGB'))

    return img_array.astype(np.uint8)