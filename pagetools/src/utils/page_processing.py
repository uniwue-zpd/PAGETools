import numpy as np


def string_to_coords(coord_string: str) -> np.array:
    """Takes a PAGE XML coordinate string extracted out of PAGE XML `Coord` elements and transforms it into a
    numpy array of 2D coordinates

    :param coord_string:
    :return:
    """
    coordinates = []
    pts = coord_string.split()

    for coord in pts:
        x, y = coord.split(",")
        coordinates.append([int(x), int(y)])

    return np.array(coordinates)
