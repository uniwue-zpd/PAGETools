from pagetools.src.Page import Page
from pagetools.src.Image import Image, ProcessedImage
from pagetools.src.utils import filesystem

from pathlib import Path
from typing import List, Iterator, Tuple


class Extractor:
    def __init__(self, xml: Path, images: List[Path], out: Path, enumerate_output: bool, background, padding: Tuple[int],
                 auto_deskew: bool, deskew: float, gt_index: int, pred_index: int):
        self.xml = self.xml_to_page(xml)
        self.images = self.get_images(images)

        self.out = out
        self.enumerate_output = enumerate_output

        self.background = background
        self.padding = padding

        self.auto_deskew = auto_deskew
        self.deskew = deskew

        self.gt_index = gt_index
        self.pred_index = pred_index

    @staticmethod
    def xml_to_page(xml: Path):
        return Page(xml)

    @staticmethod
    def get_images(images: List[Path]) -> Iterator[Image]:
        return [Image(img) for img in images]


class TextLineExtractor(Extractor):
    def __init__(self, xml: Path, images: List[Path], out: Path, enumerate_output: bool, background,
                 padding: Tuple[int], auto_deskew: bool, deskew: float, gt_index: int, pred_index: int):
        super().__init__(xml, images, out, enumerate_output, background, padding, auto_deskew, deskew, gt_index,
                         pred_index)

    def extract_line_text_pairs(self, enumerator):
        data = self.xml.get_text_lines_data()

        for image in self.images:
            for entry in data:
                line_img = ProcessedImage(image.get_filename(), background=self.background,
                                          orientation=entry["orientation"])

                line_img.cutout(shape=entry["coords"], padding=self.padding)

                if self.deskew:
                    line_img.deskew(self.deskew)
                elif self.auto_deskew:
                    line_img.auto_deskew()

                img_suffix = filesystem.get_suffix(image.get_filename())
                file_basename = filesystem.get_file_basename(self.xml.get_filename())

                if self.enumerate_output:
                    base_filename = Path(self.out, f"{str(enumerator[0]).zfill(6)}")
                else:
                    base_filename = Path(self.out, f"{file_basename}_{entry['id']}")

                img_filename = base_filename.with_suffix(img_suffix)
                line_img.export_image(img_filename)

                for text_equiv in entry["text_equivs"]:
                    if text_equiv["index"] == self.gt_index:
                        text_suffix = ".gt.txt"
                    elif text_equiv["index"] == self.pred_index:
                        text_suffix = ".pred.txt"
                    else:
                        text_suffix = f".{text_equiv['index']}.txt"
                    filesystem.write_text_file(text_equiv["content"], base_filename.with_suffix(text_suffix))

                enumerator[0] += 1

