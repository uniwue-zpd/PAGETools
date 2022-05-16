# Nachfragen
import cv2

# keep this
import glob
from pathlib import Path
import sys

import numpy
import numpy as np
from PIL import Image
from datetime import datetime

from lxml import etree

class Line2Page:
    """Object, which stores meta data
    source, image_folder, gt_folder, dest_folder are Path objects
    """

    def __init__(self, creator, source, image_folder, gt_folder, destination_folder, ext, pred, lines, spacing, border,
                 debug, threads, xml_schema):
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
        #self.border = border
        self.debug = debug
        self.threads = threads

        # List of all images in the folder with the desired extension
        self.imgList = [f for f in sorted(glob.glob(str(self.image_folder) + '/*' + self.ext))]
        self.gtList = []
        self.nameList = []
        self.matches = []

        # Extension strings used
        self.gt_suffix = ".gt.txt"
        self.pred_suffix = ".pred.txt"
        self.img_suffix = '.nrm.png'

        self.background_colour = (0, 255, 0)
        if border[1] > lines:
            footer_size = border[1] - lines
        else:
            footer_size = 0
        self.border = (border[0], footer_size, border[2], border[3])

        self.nsmap = f'http://schema.primaresearch.org/PAGE/gts/pagecontent/20{xml_schema}-07-15'
        self.xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        self.xmlSchemaLocation = \
            f'http://schema.primaresearch.org/PAGE/gts/pagecontent/20{xml_schema}-07-15 ' \
            f'http://schema.primaresearch.org/PAGE/gts/pagecontent/20{xml_schema}-07-15/pagecontent.xsd'
        # remove
        # self.print_self()

    @staticmethod
    def check_dest(dest: Path, create_folder=False):
        """Checks if the destination is legitimate and creates directory, if create is True"""
        if not dest.is_dir():
            if create_folder:
                dest.expanduser()
                Path.mkdir(dest, parents=True, exist_ok=True)
                print(f"{str(dest)} directory created")
            else:
                raise Exception(f"Error: {str(dest)} does not exist")
        return dest

    @staticmethod
    def get_text(file):
        """extracts the text from inside the file"""
        with open(file, 'r') as read_file:
            data = read_file.read().rstrip()
            return data

    @staticmethod
    def chunks(lst, n):
        """Yields successive n-sized chunks from lst"""
        for i in range(0, len(lst), n):
            yield lst[i: i + n]

    @staticmethod
    def name_pages(pages):
        """ returns a list of all objects in pages with pagename followed by a 4-digit pagenumber """
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

    @staticmethod
    def progress(count, total, status='.'):
        """displays a progress bar"""
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '█' * filled_len + '_' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()

    def make_page(self, page_with_name, semaphore):
        """Creates img and corresponding xml of a page"""
        merged = self.merge_images(page_with_name[0])
        # merged.save(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + self.img_suffix) # pillow
        cv2.imwrite(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + self.img_suffix, merged)
        # merged.close() # pillow
        # build_xml(page_with_name[0], page_with_name[1] + self.img_suffix, merged.height, merged.width) # pillow
        xml_tree = self.build_xml(page_with_name[0], page_with_name[1] + self.img_suffix, merged.shape[0], merged.shape[1])
        if self.debug is True:
            print(etree.tostring(xml_tree, encoding='unicode', pretty_print=True))
        xml = etree.tostring(xml_tree, encoding='utf-8', xml_declaration='xml')
        xml_tree.clear()
        myfile = open(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + ".xml", "wb")
        myfile.write(xml)
        myfile.close()
        semaphore.release()

    def match_files(self):
        """Pairs image with gt-Text and adds the pairing to matches"""
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
                        print(
                            f"WARNING: The File {self.gt_folder.joinpath(img_name)}{self.pred_suffix} could not be "
                            f"found! Omitting line from page")
                self.matches.append(pairing.copy())
            else:
                print(
                    f"WARNING: The File {str(self.gt_folder)} {img_name}{self.gt_suffix} could not be found! Omitting line "
                    f"from page")

    def merge_images(self, page):
        """
        Merge list of images into one, displayed on top of each other
        :return: the merged Image object
        """
        img_list = []
        img_width = 0
        img_height = 0
        spacer_height = self.line_spacing * (len(page) - 1)
        for line in page:
            image_data = cv2.imread(line[0])
            # image_data = Image.open(line[0]) # pillow
            image = image_data.copy()
            # image_data.close() # pillow
            # (width, height) = image.size # pillow
            (height, width, channels) = image.shape
            img_width = max(img_width, width)
            img_height += height
            img_list.append(image)
        if 'nrm' not in self.img_suffix:
            # result = Image.new('RGB', (img_width + self.border * 2, img_height + self.border * 2 + spacer_height), (255, 255, 255)) #pillow
            result = np.full((self.border[0], img_width + self.border[2] + self.border[3], channels), self.background_colour, np.uint8)
        else:
            # result = Image.new('LA', (img_width + self.border, img_height + self.border + spacer_height)) # pillow
            result = np.zeros((self.border[0], img_width + self.border[2] + self.border[3], channels), np.uint8)
        # cv2.imwrite("Test_Zeroes.jpg", result) # remove

        # before = self.border
        # print(f'Result-width {result.shape[1]}')
        for img in img_list:
            # result.paste(img, (self.border, before)) # pillow
            #if img.shape[1] < img_width:
                # print(f'Img shape before {img.shape[1]}, should be {result.shape[1]}')
            padding = img_width - img.shape[1]
            img = cv2.copyMakeBorder(img, 0, self.line_spacing, self.border[2], padding + self.border[3], cv2.BORDER_CONSTANT, None, self.background_colour)
            # print(f'Img shape after {img.shape[1]}')
            result = np.concatenate((result, img), axis=0)
            # before += img.size[1] + self.line_spacing # pillow
            # before += img.shape[0] + self.line_spacing
        footer = np.full((self.border[1], img_width + self.border[2] + self.border[3], channels), self.background_colour, np.uint8)
        result = np.concatenate((result, footer), axis=0)
            # img.close() # pillow
        return result

    def build_xml(self, line_list, img_name, img_height, img_width):
        """
        Builds PageXML from list of images, with txt files corresponding to each one of them
        :return: the built PageXml[.xml] file
        """
        attribute_schema_location = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        NSMAP = {None : self.nsmap,
                 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        pcgts = etree.Element('PcGts', {attribute_schema_location : self.xmlSchemaLocation}, nsmap=NSMAP)

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
        coord_string = f'{min_x},{min_y} {max_x},{min_y} {max_x},{max_y} ({min_x},{max_y}'
        region_coords.set('points', coord_string)
        i = 1
        # last_bottom = self.border # pillow
        last_bottom = min_y
        for line in line_list:
            text_line = etree.SubElement(text_region, 'TextLine')
            text_line.set('id', 'r0_l' + str(Path(line[0]).name.split('.')[0].zfill(3)))
            i += 1
            line_coords = etree.SubElement(text_line, 'Coords')
            # image = Image.open(line[0]) # pillow
            image = cv2.imread(line[0])
            # (width, height) = image.size # pillow
            height = image.shape[0]
            width = image.shape[1]
            # image.close() # pillow
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
        b = str(self.border[0])
        p = str(previous_lower_left)
        w = str(line_width + self.border[1] + self.border[2])
        h = str(line_height + previous_lower_left)
        x_min = self.border[0]
        x_max = x_min + line_width
        y_min = previous_lower_left
        y_max = y_min + line_height
        # coord_string = b + ',' + p + ' ' + b + "," + h + ' ' + w + ',' + h + ' ' + w + ',' + p
        coord_string = f'{x_min},{y_min}) {x_max},{y_min} {x_max},{y_max} {x_min},{y_max}'
        return coord_string

    # remove
    def print_self(self):
        """Prints all info saved in the object"""

        print("Object_info:")
        print(f"Creator - {str(self.creator)}")
        print(f"Source_Folder - {str(self.source)}")
        print(f"Image_Folder - {str(self.image_folder)}")
        print(f"GT_Folder - {str(self.gt_folder)}")
        print(f"Dest_Folder - {str(self.dest_folder)}")
        print(f"Ext - {str(self.ext)}")
        print(f"pred - {str(self.pred)}")
        print(f"Lines - {str(self.lines)}")
        print(f"Spacing - {str(self.line_spacing)}")
        print(f"Border - {str(self.border)}")
        print(f"Debug - {str(self.debug)}")
        print(f"Threads - {str(self.threads)}")

        print(f"GT_Suffix - {str(self.gt_suffix)}")
        print(f"Pred_Suffix - {str(self.pred_suffix)}")
        print(f"Img_Suffix - {str(self.img_suffix)}\n")
