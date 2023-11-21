import glob
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

from lxml import etree
import cv2
import numpy as np


class Line2Page:
    """Object, which stores meta data
    source, image_folder, gt_folder, dest_folder are Path objects
    """

    def __init__(self,
                 creator: str,
                 source: str,
                 image_folder: str,
                 gt_folder: str,
                 destination_folder: str,
                 ext: str,
                 pred: str,
                 lines: int,
                 spacing: int,
                 output_extension: str,
                 border: Tuple[int],
                 background_color: Tuple[int],
                 debug: bool,
                 threads: int,
                 xml_schema: str):
        logging.basicConfig(level=int(debug))
        self.log = logging.getLogger(__name__)

        self.creator = creator
        self.source = self.check_dest(Path(source).resolve())
        if image_folder == source or image_folder:
            self.image_folder = self.source
        else:
            self.image_folder = self.check_dest(Path(image_folder).resolve())
        if gt_folder == str(self.source) or gt_folder:
            self.gt_folder = self.source
        else:
            self.gt_folder = self.check_dest(Path(gt_folder).resolve())

        self.dest_folder = self.check_dest(Path(destination_folder).resolve(), True)
        self.ext = ext
        self.pred = pred
        self.lines = lines
        self.line_spacing = spacing
        self.threads = threads

        # List of all images in the folder with the desired extension
        self.imgList = [f for f in sorted(glob.glob(f"{str(self.image_folder)}/*{self.ext}"))]
        self.gtList = []
        self.nameList = []
        self.matches = []

        # Extension strings used
        self.gt_suffix = ".gt.txt"
        self.pred_suffix = ".pred.txt"
        self.img_suffix = output_extension if output_extension else ext

        self.background_colour = background_color
        self.colour_channels = 3
        if border[1] > lines:
            footer_size = border[1] - lines
        else:
            footer_size = 0
        self.border = (border[0], footer_size, border[2], border[3])

        self.nsmap = f'http://schema.primaresearch.org/PAGE/gts/pagecontent/{xml_schema}-07-15'
        self.xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        self.xmlSchemaLocation = \
            f'http://schema.primaresearch.org/PAGE/gts/pagecontent/{xml_schema}-07-15 ' \
            f'http://schema.primaresearch.org/PAGE/gts/pagecontent/{xml_schema}-07-15/pagecontent.xsd'

        self.log.debug(f"Attributes: \nCreator: {self.creator}\nSource Folder: {self.source}\n"
                       f"Image Folder: {self.image_folder}\nGT Folder: {self.gt_folder}\n"
                       f"Destination Folder: {self.dest_folder}\nImage Extension: {self.ext}\n"
                       f"Predecessor: {self.pred}\nNumber of lines per image: {self.lines}\n"
                       f"Line Spacing: {self.line_spacing}\nBorder: (head:{self.border[0]}, footer: {self.border[1]}, "
                       f"left: {self.border[2]}, right:{self.border[3]})\nThreads: {self.threads}\n"
                       f"XML Schema: {self.xmlSchemaLocation}")

    @staticmethod
    def get_text(file: str) -> str:
        """Extracts the text from inside the file"""
        with Path(file).open('r') as read_file:
            return read_file.read().rstrip()

    @staticmethod
    def chunks(lst: list, n: int):
        """Yields successive n-sized chunks from lst"""
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    @staticmethod
    def name_pages(pages: List[str]) -> List[List[str]]:
        """Returns a list of all objects in pages with pagename followed by a 4-digit pagenumber"""
        page_with_name = []
        pages_with_name = []
        page_iterator = 0
        for page in pages:
            page_iterator += 1
            name = str(page_iterator).zfill(4)
            page_with_name.append(page)
            page_with_name.append(name)
            pages_with_name.append(page_with_name.copy())
            page_with_name.clear()
        return pages_with_name

    def check_dest(self, dest: Path, create_folder=False):
        """Checks if the destination is legitimate and creates directory, if create is True"""
        if not dest.is_dir():
            if create_folder:
                dest.expanduser()
                Path.mkdir(dest, parents=True, exist_ok=True)
                self.log.info(f" {str(dest)} directory created")
            else:
                error_msg = f" {str(dest)} does not exist"
                self.log.error(error_msg)
                raise NameError(error_msg)
        return dest

    def make_page(self, page_with_name, semaphore):
        """Creates img and corresponding xml of a page"""
        merged = self.merge_images(page_with_name[0])
        cv2.imwrite(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + self.img_suffix, merged)
        xml_tree = self.build_xml(page_with_name[0], page_with_name[1] + self.img_suffix, merged.shape[0],
                                  merged.shape[1])

        self.log.debug(etree.tostring(xml_tree, encoding='unicode', pretty_print=True))
        xml = etree.tostring(xml_tree, encoding='utf-8', xml_declaration='xml')
        xml_tree.clear()
        myfile = open(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + ".xml", "wb")
        myfile.write(xml)
        myfile.close()
        semaphore.release()

    def match_files(self):
        """Pairs image with GT text and adds the pairing to matches"""
        for img in self.imgList:
            pairing = []
            img_name = Path(img.split('.')[0]).name
            self.gtList = [f for f in glob.glob(str(self.gt_folder.joinpath(img_name)) + self.gt_suffix)]
            if len(self.gtList) > 0:
                self.nameList.append(img_name)
                pairing.append(img)
                gt_filename = self.gtList[0]
                pairing.append(gt_filename)
                pairing.append(self.get_text(gt_filename))

                if self.pred:
                    pred_filelist = [f for f in glob.glob(str(self.gt_folder.joinpath(img_name)) + self.pred_suffix)]
                    if len(pred_filelist) > 0:
                        pred_filename = pred_filelist[0]
                        pairing.append(pred_filename)
                        pairing.append(self.get_text(pred_filename))
                    else:
                        self.log.warning(f" The File {self.gt_folder.joinpath(img_name)}{self.pred_suffix} could not be"
                                         f" found! Omitting line from page")
                self.matches.append(pairing.copy())
            else:
                self.log.warning(
                    f" The File {str(self.gt_folder.joinpath(img_name))}{self.gt_suffix} could not be found! "
                    f"Omitting line from page")

    def merge_images(self, page):
        """
        Merge list of images into one, displayed on top of each other
        :return: the merged Image object
        """
        img_list = []
        img_width = 0
        # find max-width of all images
        for line in page:
            image_data = cv2.imread(line[0])
            image = image_data.copy()
            width = image.shape[1]
            img_width = max(img_width, width)
            img_list.append(image)
            result = np.full((self.border[0], img_width + self.border[2] + self.border[3], self.colour_channels),
                             self.background_colour, np.uint8)
        # All images need the same width for np.concatenate to work -> padding on the image at its right side
        for img in img_list:
            padding = img_width - img.shape[1]
            img = cv2.copyMakeBorder(img, 0, self.line_spacing, self.border[2], padding + self.border[3],
                                     cv2.BORDER_CONSTANT, None, self.background_colour)
            result = np.concatenate((result, img), axis=0)
            footer = np.full((self.border[1], img_width + self.border[2] + self.border[3], self.colour_channels),
                             self.background_colour, np.uint8)
        result = np.concatenate((result, footer), axis=0)
        return result

    def build_xml(self, line_list, img_name, img_height, img_width):
        """
        Builds PageXML from list of images, with corresponding text
        :return: the built PageXml[.xml] file
        """
        attribute_schema_location = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        NSMAP = {None: self.nsmap,
                 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        pcgts = etree.Element('PcGts', {attribute_schema_location: self.xmlSchemaLocation}, nsmap=NSMAP)

        metadata = etree.SubElement(pcgts, 'Metadata')
        creator = etree.SubElement(metadata, 'Creator')
        creator.text = self.creator
        created = etree.SubElement(metadata, 'Created')
        generated_on = datetime.now().isoformat()
        created.text = generated_on
        last_change = etree.SubElement(metadata, 'LastChange')
        last_change.text = generated_on

        page = etree.SubElement(pcgts, 'Page')
        page.set('imageFilename', img_name)
        page.set('imageHeight', str(img_height))
        page.set('imageWidth', str(img_width))

        text_region = etree.SubElement(page, 'TextRegion')
        text_region.set('id', 'r0')
        text_region.set('type', 'paragraph')
        region_coords = etree.SubElement(text_region, 'Coords')
        min_x = self.border[2]
        max_x = img_width - self.border[3]
        min_y = self.border[0]
        max_y = img_height - self.border[1]
        coord_string = f'{min_x},{min_y} {max_x},{min_y} {max_x},{max_y} {min_x},{max_y}'
        region_coords.set('points', coord_string)
        last_bottom = min_y
        for line in line_list:
            text_line = etree.SubElement(text_region, 'TextLine')
            text_line.set('id', 'r0_l' + str(Path(line[0]).name.split('.')[0].zfill(3)))
            line_coords = etree.SubElement(text_line, 'Coords')
            image = cv2.imread(line[0])
            height = image.shape[0]
            width = image.shape[1]
            line_coords.set('points', self.make_coord_string(last_bottom, width, height))
            last_bottom += (height + self.line_spacing)
            line_gt_text = etree.SubElement(text_line, 'TextEquiv')
            line_gt_text.set('index', str(0))
            unicode_gt = etree.SubElement(line_gt_text, 'Unicode')
            unicode_gt.text = line[2]
            if self.pred:
                line_prediction_text = etree.SubElement(text_line, 'TextEquiv')
                line_prediction_text.set('index', str(1))
                unicode_prediction = etree.SubElement(line_prediction_text, 'Unicode')
                unicode_prediction.text = line[4]

        return pcgts

    def make_coord_string(self, previous_lower_left, line_width, line_height):
        """Builds value string, to be incorporated into the xml"""
        x_min = self.border[0]
        x_max = x_min + line_width
        y_min = previous_lower_left
        y_max = y_min + line_height
        return f'{x_min},{y_min} {x_max},{y_min} {x_max},{y_max} {x_min},{y_max}'
