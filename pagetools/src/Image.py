from pagetools.src.utils.img_processing import rotate_img, background_calc_dispatch_table

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
        """Returns the numpy array representation of an image file

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

        self.orientation = orientation
        self.background = self.get_background(background)

    def get_background(self, background: tuple):
        if background[0] == "calculate":
            return background_calc_dispatch_table(background[1])(self.img)
        elif background[0] == "color":
            return background[1]

    def cutout(self, shape: np.array, padding: Tuple[int], background: tuple):
        """Cuts sub image from base image based on input shape. Adds padding if parameter is set.

        :param shape:
        :param padding:
        :param background:
        :return:
        """
        background = self.get_background(background)
        rect = cv2.boundingRect(shape)
        x, y, w, h = rect

        cropped = self.img[y:y + h, x:x + w].copy()

        pts = shape - shape.min(axis=0)
        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1)

        dst = cv2.bitwise_and(cropped, cropped, mask=mask)

        im2 = np.full((dst.shape[0], dst.shape[1], 3), background, dtype=np.uint8)

        inverted_mask = cv2.bitwise_not(mask)
        bg = cv2.bitwise_or(im2, im2, mask=inverted_mask)
        final = rotate_img(dst + bg, self.orientation, self.background)

        self.img = final
        self.img = cv2.copyMakeBorder(final, *padding, cv2.BORDER_CONSTANT, value=self.background)

    def deskew(self, angle: float = 0.0):
        """Deskews image based on a fixed angle.
        
        :param angle:
        :return:
        """
        self.img = rotate_img(self.img, angle, self.background)

    def auto_deskew(self):
        """Deskews image by calculating optimal rotation angle and then applying rotation.

        :return:
        """
        grayscale = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)

        rotated = rotate_img(self.img, angle, self.background)

        self.img = rotated
