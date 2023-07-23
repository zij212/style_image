from PIL import Image
import numpy as np

from utils import load_image


def apply_1d_upsampling(image_array, num_ribbons, orientation="vertical", repeat=2):
    """
    Upsample an image in vertical or horizontal direction

    :param image_array: np.array, 3 channel image
    :param num_ribbons: int, number of ribbons to split the original image
    :param orientation: str, orientation of the ribbon, default is "vertical"
    :param repeat: int, frequency to repeat a ribbon
    :return: np.array
    """

    try:
        assert orientation in ["vertical", "horizontal"]
    except AssertionError:
        raise Exception("Orientation needs to be either 'vertical' or 'horizontal'.")

    img_h, img_w = image_array.shape[0], image_array.shape[1]

    if orientation == "vertical":
        ribbon_width = img_w // num_ribbons
        stack = np.hstack
    else:
        ribbon_width = img_h // num_ribbons
        stack = np.vstack

    start_of_ribbons = list(range(0, ribbon_width * num_ribbons, ribbon_width))

    criss_crossed_img_array = []
    for ribbon_start in start_of_ribbons:

        if orientation == "vertical":
            ribbon = image_array[:, ribbon_start:ribbon_start + ribbon_width, :]
        else:
            ribbon = image_array[ribbon_start:ribbon_start + ribbon_width, :, :]

        for i in range(repeat):
            criss_crossed_img_array.append(ribbon)

    return stack(criss_crossed_img_array)


def apply_upsampling(img_array, num_ribbons=10, repeat=2):
    """
    Upsample the image array vertically and horizontally

    :param img_array: np.array, 3 channel image
    :param num_ribbons: number of ribbons to split the image
    :param repeat: frequency to repeat a ribbon
    :return:
    """
    img_array = apply_1d_upsampling(img_array, num_ribbons, "vertical", repeat)
    img_array = apply_1d_upsampling(img_array, num_ribbons, "horizontal", repeat)
    return img_array


if __name__ == "__main__":

    fname = "daisy_square.jpg"
    img = load_image(fname, color=True)

    transform = apply_upsampling
    new_fname = f"{fname.split('.')[0]}_{transform.__name__}_color.jpg"
    img = transform(img, num_ribbons=10)
    img = Image.fromarray(img)
    img.save(new_fname, quality=100, subsampling=0)

