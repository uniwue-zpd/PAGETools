from pagetools.src.Page import Page
from pagetools.src.Image import Image, ProcessedImage
from pagetools.src.utils import filesystem
from pagetools.src.utils.constants import extractable_regions

from pathlib import Path
from typing import List, Iterator, Set, Tuple


class Extractor:
    def __init__(self, xml: Path, images: List[Path], include: List[str], exclude: List[str], no_text: bool, out: Path,
                 enumerate_output: bool, background, padding: Tuple[int], auto_deskew: bool, deskew: float,
                 gt_index: int, pred_index: int):
        self.xml = self.xml_to_page(xml)
        self.images = self.get_images(images)

        self.element_list = self.build_element_list(include, exclude)

        self.extract_text = not no_text

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

    @staticmethod
    def build_element_list(include: List[str], exclude: List[str]) -> Set[str]:
        element_list = extractable_regions.copy()
        if "*" in exclude:
            element_list.clear()
        else:
            element_list = [element_list.remove(element_type) for element_type in exclude]
        if "*" in include:
            element_list = extractable_regions.copy()
        else:
            element_list.extend([elem_type for elem_type in include if elem_type != "*"])
        return element_list

    # TODO: Rewrite as soon as PAGEpy is available
    def extract(self, enumerator):
        data = self.xml.get_element_data(self.element_list)

        for image in self.images:
            for entry in data:
                img = ProcessedImage(image.get_filename(), background=self.background, orientation=entry["orientation"])

                img.cutout(shape=entry["coords"], padding=self.padding, background=self.background)

                if self.deskew:
                    img.deskew(self.deskew)
                elif self.auto_deskew:
                    img.auto_deskew()

                img_suffix = filesystem.get_suffix(image.get_filename())
                file_basename = filesystem.get_file_basename(self.xml.get_filename())

                if self.enumerate_output:
                    base_filename = Path(self.out, f"{str(enumerator[0]).zfill(6)}")
                else:
                    base_filename = Path(self.out, f"{file_basename}_{entry['id']}")

                img_filename = base_filename.with_suffix(img_suffix)
                img.export_image(img_filename)

                if self.extract_text:
                    num_non_indexed_text_equivs = 0
                    for text_equiv in entry["text_equivs"]:
                        if text_equiv["index"] is None:
                            text_suffix = f".u{num_non_indexed_text_equivs}.txt"
                            num_non_indexed_text_equivs += 1
                        elif int(text_equiv["index"]) == self.gt_index:
                            text_suffix = ".gt.txt"
                        elif int(text_equiv["index"]) == self.pred_index:
                            text_suffix = ".pred.txt"
                        else:
                            text_suffix = f".i{text_equiv['index']}.txt"
                        filesystem.write_text_file(text_equiv["content"], base_filename.with_suffix(text_suffix))

                enumerator[0] += 1
