import pagetools.src.utils.page_processing as page_processing
import numpy as np


def test_string_to_coords():
    string_coords = "1,1 2000,1 1,2000 2000,2000"
    coords = np.array([[1, 1], [2000, 1], [1, 2000], [2000, 2000]])
    np.testing.assert_array_equal(page_processing.string_to_coords(string_coords), coords)
