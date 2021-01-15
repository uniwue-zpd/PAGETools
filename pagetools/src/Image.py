from pagetools.src.utils.img_processing import rotate_img

from pathlib import Path
from typing import Tuple

import numpy as np
import cv2
from deskew import determine_skew


class Image:
    def __init__(self, img: Path):
        self.img = self.read_img(img)
        self.filename = img

    @staticmethod
    def read_img(img: Path) -> np.array:
        """Reads image from file and transforms it into a numpy array

        :param img: Path obj pointing to the image file
        :return: numpy array representing the input image
        """
        return cv2.imread(str(img))

    def get_image(self) -> np.array:
        """Returns numpy array representation of image

        :return: np.array
        """
        return self.img

    def get_filename(self) -> Path:
        """Returns Path obj pointing to the image file

        :return:
        """
        return self.filename

    def export_image(self, filename: Path):
        """Writes numpy array representation of image to hard drive as image file

        :param filename:
        """
        cv2.imwrite(str(filename), self.img)


class ProcessedImage(Image):
    def __init__(self, img: Path, background: Tuple[str, str], orientation: float):
        super().__init__(img)

        self.background = self.get_background(background)

        if orientation:
            self.deskew(orientation)

    @staticmethod
    def get_background(background: tuple):
        if background[0] == "calculate":
            return
        elif background[0] == "color":
            return background[1]

    def cutout(self, shape: np.array, padding: Tuple[int]):
        """

        :param shape:
        :param padding:
        :return:
        """
        _img = self.img

        rect = cv2.boundingRect(shape)
        x, y, w, h = rect

        cropped = _img[y:y + h, x:x + w].copy()
        pts = shape - shape.min(axis=0)

        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        out = cv2.bitwise_and(cropped, cropped, mask=mask)

        bg = np.ones_like(cropped, np.uint8) * 255
        cv2.bitwise_not(bg, bg, mask=mask)
        out = bg + out

        self.img = out
        self.img = cv2.copyMakeBorder(out, *padding, cv2.BORDER_CONSTANT, value=self.background)

    def deskew(self, angle: float = 0):
        """
        
        :param angle:
        :return:
        """
        self.img = rotate_img(self.img, angle, self.background)

    def auto_deskew(self):
        """

        :return:
        """
        grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)

        rotated = rotate_img(self.img, angle, self.background)

        self.img = rotated
