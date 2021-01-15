from typing import Union, Tuple
import math

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
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))),
                          flags=cv2.INTER_CUBIC, borderValue=background)
