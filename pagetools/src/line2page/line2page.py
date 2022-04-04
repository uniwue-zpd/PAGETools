# use this
import pathlib
import stat

import lxml

#  remove this
import argparse

# keep this
import time
import glob
from pathlib import Path


def check_dest(dest: Path):
    """Checks if the destination is legitimate and creates directory, if it does not exist yet"""
    if not dest.exists():
        print(str(dest) + " dir not found, creating directory")
        # dest.parent.chmod(stat.S_IWRITE)
        print(dest)
        dest.expanduser()
        print(dest)
        Path.mkdir(dest, parents=True, exist_ok=True)
    # Needed?
    #if not dest.endswith(os.path.sep):
    #    dest += os.path.sep
    return dest


def strip_path(path: Path):
    """extracts the basename of path"""
    return path.name


def get_text(file):
    """extracts the text from inside the file"""
    with open(file, 'r') as read_file:
        data = read_file.read().rstrip()
        return data


class Line2Page:
    """Object, which includes the meta data
    source, image_folder, gt_folder, dest_folder are Path objects
    """

    def __init__(self, creator, source, i_f, gt_f, dest, ext, pred, lines, spacing, border, debug, threads):
        self.creator = creator
        self.source = Path(source)
        self.image_folder = Path(i_f)
        if not i_f == source:
            check_dest(self.image_folder)
        self.gt_folder = Path(gt_f)
        if not gt_f == source:
            check_dest(self.gt_folder)
        self.dest_folder = check_dest(Path(dest))
        self.ext = ext
        self.pred = pred
        self.lines = lines
        self.line_spacing = spacing
        self.border = border
        self.debug = debug
        self.threads = threads

        # List of all images in the folder with the desired extension
        self.imgList = [f for f in sorted(glob.glob(str(self.image_folder) + '*' + self.ext))]
        self.gtList = []
        self.nameList = []
        self.matches = []

    def match_files(self):
        """"""
        pairing = []
        for img in self.imgList:
            img_name = strip_path(img.split('.')[0])
            self.gtList = [f for f in glob.glob(str(self.gt_folder) + img_name + ".gt.txt")]
            if len(self.gtList) > 0:
                self.nameList.append(img_name)
                pairing.append(img)
                gt_filename = self.gtList[0]
                pairing.append(gt_filename)
                pairing.append(get_text(gt_filename))
                if self.pred:
                    pred_filelist = [f for f in glob.glob(str(self.gt_folder) + img_name + ".pred.text")]
                    if len(pred_filelist) > 0:
                        pred_filename = pred_filelist[0]
                        pairing.append(pred_filename)
                        pairing.append(get_text(pred_filename))
                    else:
                        print("WARNING: The File " + str(self.gt_folder) + img_name + ".pred.txt could not be found! Omitting line from page")
                self.matches.append(self.pairing.copy())
            else:
                print("WARNING: The File " + str(self.gt_folder) + img_name + ".gt.txt could not be found! Omitting line from page")
        print("matching files")

