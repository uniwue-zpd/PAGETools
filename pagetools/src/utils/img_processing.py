from typing import Tuple, Union

import numpy as np
import cv2


def background_calc_dispatch_table(mode: str):
    dispatch_table = {
        "dominant": calc_dominat_color,
        "mean": calc_mean_color,
        "median": calc_median_color
    }

    return dispatch_table[mode]


def calc_dominat_color(img: np.array) -> Tuple[int]:
    """Calculates the dominant color of an image using bincounts

    :param img:
    :return:
    """
    two_dim = img.reshape(-1, img.shape[-1])
    color_range = (256,)*3
    one_dim = np.ravel_multi_index(two_dim.T, color_range)
    return tuple([int(c) for c in np.unravel_index(np.bincount(one_dim).argmax(), color_range)])


def calc_mean_color(img: np.array) -> Tuple[int]:
    """

    :param img:
    :return:
    """
    return img.mean(axis=0).mean(axis=0)


def calc_median_color(img: np.array) -> np.ndarray:
    """

    :param img:
    :return:
    """
    return np.median(np.median(img, axis=0), axis=0)


def rotate_img(image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]) -> np.ndarray:
    """

    :param image:
    :param angle:
    :param background:
    :return:
    """
    rows = image.shape[0]
    cols = image.shape[1]

    img_center = (cols / 2, rows / 2)
    rot_mat = cv2.getRotationMatrix2D(img_center, angle*-1, 1)

    rotated_image = cv2.warpAffine(image, rot_mat, (cols, rows), borderValue=background)
    return rotated_image
