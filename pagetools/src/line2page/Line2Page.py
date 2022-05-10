# Nachfragen
import lxml

# keep this
import glob
from pathlib import Path
import sys
from PIL import Image
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from datetime import datetime
from xml.dom import minidom


class Line2Page:
    """Object, which stores meta data
    source, image_folder, gt_folder, dest_folder are Path objects
    """

    def __init__(self, creator, source, i_f, gt_f, dest, ext, pred, lines, spacing, border, debug, threads):
        self.creator = creator
        self.source = self.check_absolute(Path(source))
        self.check_dest(self.source)
        if i_f == source or i_f == '':
            self.image_folder = self.source
        else:
            self.image_folder = self.check_absolute(Path(i_f))
            self.check_dest(self.image_folder)
        if gt_f == str(self.source) or gt_f == '':
            self.gt_folder = self.source
        else:
            self.gt_folder = self.check_absolute(Path(gt_f))
            self.check_dest(self.gt_folder)

        self.dest_folder = self.check_dest(self.check_absolute(Path(dest)), True)
        self.ext = ext
        self.pred = pred
        self.lines = lines
        self.line_spacing = spacing
        self.border = border
        self.debug = debug
        if threads <= 0:
            self.threads = 1
            print(f"Warning: thread-count can not be <0; Setting threads to 1!")
        else:
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

        self.xmlSchemaLocation = \
            'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15 ' \
            'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15/pagecontent.xsd'

        self.print_self()

    @staticmethod
    def check_dest(dest: Path, create=False):
        """Checks if the destination is legitimate and creates directory, if create is True"""
        if not dest.is_dir():
            if create:
                dest.expanduser()
                Path.mkdir(dest, parents=True, exist_ok=True)
                print(str(dest) + " directory created")
            else:
                raise Exception(f"Error: {str(dest)} does not exist")
        return dest

    @staticmethod
    def check_absolute(folder: Path):
        """Checks if the given Path is absolute, if not it makes it absolute"""
        if folder.is_absolute():
            return folder
        else:
            return Path.cwd().joinpath(folder)

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

    @staticmethod
    def prettify(elem):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml("  ")

    def make_page(self, page_with_name, semaphore):
        """Creates img and corresponding xml of a page"""
        merged = self.merge_images(page_with_name[0])
        merged.save(str(self.dest_folder.joinpath(Path(page_with_name[1]).name)) + self.img_suffix)
        merged.close()
        xml_tree = self.build_xml(page_with_name[0], page_with_name[1] + self.img_suffix, merged.height, merged.width)
        if self.debug is True:
            print(self.prettify(xml_tree))
        xml = ElementTree.tostring(xml_tree, 'utf8', 'xml')
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
            image_data = Image.open(line[0])
            image = image_data.copy()
            image_data.close()
            (width, height) = image.size
            img_width = max(img_width, width)
            img_height += height
            img_list.append(image)
        if 'nrm' not in self.img_suffix:
            result = Image.new('RGB', (img_width + self.border * 2, img_height + self.border * 2 + spacer_height),
                               (255, 255, 255))
        else:
            result = Image.new('LA', (img_width + self.border, img_height + self.border + spacer_height))
        before = self.border

        for img in img_list:
            result.paste(img, (self.border, before))
            before += img.size[1] + self.line_spacing
            img.close()
        return result

    def build_xml(self, line_list, img_name, img_height, img_width):
        """
        Builds PageXML from list of images, with txt files corresponding to each one of them
        :return: the built PageXml[.xml] file
        """
        pcgts = Element('PcGts')
        pcgts.set('xmlns', 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2017-07-15')
        pcgts.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        pcgts.set('xsi:schemaLocation', self.xmlSchemaLocation)

        metadata = SubElement(pcgts, 'Metadata')
        creator = SubElement(metadata, 'Creator')
        creator.text = self.creator
        created = SubElement(metadata, 'Created')
        generated_on = datetime.now().isoformat()
        created.text = generated_on
        last_change = SubElement(metadata, 'LastChange')
        last_change.text = generated_on

        page = SubElement(pcgts, 'Page')
        page.set('imageFilename', img_name)
        page.set('imageHeight', str(img_height))
        page.set('imageWidth', str(img_width))

        text_region = SubElement(page, 'TextRegion')
        text_region.set('id', 'r0')
        text_region.set('type', 'paragraph')
        region_coords = SubElement(text_region, 'Coords')
        s = str(self.border)
        coord_string = s + ',' + s + ' ' + s + "," + str(img_height - self.border) \
                       + ' ' + str(img_width - self.border) + ',' + str(img_height - self.border) \
                       + ' ' + str(img_width - self.border) + ',' + s
        region_coords.set('points', coord_string)
        i = 1
        last_bottom = self.border
        for line in line_list:
            text_line = SubElement(text_region, 'TextLine')
            text_line.set('id', 'r0_l' + str(Path(line[0]).name.split('.')[0].zfill(3)))
            i += 1
            line_coords = SubElement(text_line, 'Coords')
            image = Image.open(line[0])
            (width, height) = image.size
            image.close()
            line_coords.set('points', self.make_coord_string(last_bottom, width, height))
            last_bottom += (height + self.line_spacing)
            line_gt_text = SubElement(text_line, 'TextEquiv')
            line_gt_text.set('index', str(0))
            unicode_gt = SubElement(line_gt_text, 'Unicode')
            unicode_gt.text = line[2]
            if self.pred:
                line_prediction_text = SubElement(text_line, 'TextEquiv')
                line_prediction_text.set('index', str(1))
                unicode_prediction = SubElement(line_prediction_text, 'Unicode')
                unicode_prediction.text = line[4]

        return pcgts

    def make_coord_string(self, previous_lower_left, line_width, line_height):
        """Builds value string, to be incorporated into the xml"""
        b = str(self.border)
        p = str(previous_lower_left)
        w = str(line_width + self.border)
        h = str(line_height + previous_lower_left)
        coord_string = b + ',' + p + ' ' + b + "," + h + ' ' + w + ',' + h + ' ' + w + ',' + p
        return coord_string

    def print_self(self):
        """Prints all info saved in the object"""
        # remove
        print("Object_info:")
        print("Creator - " + str(self.creator))
        print("Source_Folder - " + str(self.source))
        print("Image_Folder - " + str(self.image_folder))
        print("GT_Folder - " + str(self.gt_folder))
        print("Dest_Folder - " + str(self.dest_folder))
        print("Ext - " + str(self.ext))
        print("pred - " + str(self.pred))
        print("Lines - " + str(self.lines))
        print("Spacing - " + str(self.line_spacing))
        print("Border - " + str(self.border))
        print("Debug - " + str(self.debug))
        print("Threads - " + str(self.threads))

        # print("Image_List - " + str(self.imgList))
        print("gt_List - " + str(self.gtList))
        print("Name_list - " + str(self.nameList))
        print("Matches - " + str(self.matches))
        print("Spacer - " + str(self.line_spacing))

        print("GT_Suffix - " + str(self.gt_suffix))
        print("Pred_Suffix - " + str(self.pred_suffix))
        print("Img_Suffix - " + str(self.img_suffix))

        print("\n")
