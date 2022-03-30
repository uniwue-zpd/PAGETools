# use this
import click
import lxml

#  remove this
import argparse

# keep this
import os.path
import time
import glob
import os.path


def check_dest(dest):
    """
    Checks if the destination is legitimate.
    Creates directory, if it does not exist yet
    Adds seperator if dest argument does not include it yet
    """
    if not os.path.exists(dest):
        print(dest + " dir not found, creating directory")
        os.mkdir(dest)
    # Needed?
    if not dest.endswith(os.path.sep):
        dest += os.path.sep
    return dest


def strip_path(path):
    """extracts the basename of path"""
    return os.path.basename(path)


def get_text(file):
    """extracts the text from inside the file"""
    with open(file, 'r') as read_file:
        data = read_file.read().rstrip()
        return data


class CliOptions:
    """Object, which includes the meta data"""

    def __init__(self, creator, source, i_f, gt_f, dest, ext, pred, lines, spacing, border, debug, threads):
        self.creator = creator
        self.source = source
        self.image_folder = i_f
        if not i_f == source:
            check_dest(self.image_folder)
        self.gt_folder = gt_f
        if not gt_f == source:
            check_dest(self.gt_folder)
        self.dest_folder = check_dest(dest)
        self.ext = ext
        self.pred = pred
        self.lines = lines
        self.line_spacing = spacing
        self.border = border
        self.debug = debug
        self.threads = threads

        # List of all images in the folder with the desired extension
        self.imgList = [f for f in sorted(glob.glob(self.image_folder + '*' + self.ext))]
        self.gtList = []
        self.nameList = []
        self.matches = []

    def match_files(self):
        """"""
        pairing = []
        for img in self.imgList:
            img_name = strip_path(img.split('.')[0])
            self.gtList = [f for f in glob.glob(self.gt_folder + img_name + ".gt.txt")]
            if len(self.gtList) > 0:
                self.nameList.append(img_name)
                pairing.append(img)
                gt_filename = self.gtList[0]
                pairing.append(gt_filename)
                pairing.append(get_text(gt_filename))
                if self.pred:
                    pred_filelist = [f for f in glob.glob(self.gt_folder + img_name + ".pred.text")]
                    if len(pred_filelist) > 0:
                        pred_filename = pred_filelist[0]
                        pairing.append(pred_filename)
                        pairing.append(get_text(pred_filename))
                    else:
                        print(
                            "WARNING: The File " + self.gt_folder + img_name + ".pred.txt could not be found! Omitting line from page")
                self.matches.append(self.pairing.copy())
            else:
                print(
                    "WARNING: The File " + self.gt_folder + img_name + ".gt.txt could not be found! Omitting line from page")
        print("matching files")


@click.command()
@click.option('-c', '--creator', default='user', help='Creator tag for PAGE XML')
@click.option('-s', '--source_folder', default=os.getcwd(), help='Path to images and GT')
@click.option('-i', '--image_folder', default='', help='Path to images')
@click.option('-gt', '--gt_folder', default='', help='Path to GT')
@click.option('-d', '--dest_folder', default=os.getcwd() + '/merged/', help='Path to merge objects')
@click.option('-e', '--ext', default='.bin.png', help='image extension')
@click.option('-p', '--pred', default=False, type=bool, help='Set Flag to also store .pred.txt')
@click.option('-l', '--lines', default=20, type=int, help='lines per page')
@click.option('-ls', '--line_spacing', default=5, type=int, help='line spacing')
@click.option('-b', '--border', default=10, type=int, help='border in px')
@click.option('--debug', default=False, help='prints debug xml')
@click.option('--threads', default=16, type=int, help='thread count to be used')
def cli(creator, source_folder, image_folder, gt_folder, dest_folder, ext, pred, lines, line_spacing, border, debug,
        threads):
    """Initialises a CLIArgument object, which saves the added cli options."""
    # replace argparse with click
    # self.parser = argparse.ArgumentParser(description='python script to merge GT lines to page images and xml')
    if image_folder == "":
        image_path = source_folder
    else:
        image_path = image_folder
    if gt_folder == "":
        gt_path = source_folder
    else:
        gt_path = gt_folder
    option_object = CliOptions(creator, source_folder, image_path, gt_path, dest_folder, ext, pred, lines, line_spacing,
                               border, debug, threads)
    return option_object


if __name__ == '__main__':
    """python script to merge GT lines to page images and xml

        tic = time counter
        options = object with the desired meta data
    """
    tic = time.perf_counter()
    options = cli(standalone_mode=False)
    options.match_files()

    click.echo("Programm finished")

# help(Parser)
# help(main)

path = "'/home/User/Documents/file.txt'"
name = strip_path(path.split('.')[0])
name2 = strip_path(path)
print(path)
print(name)
print(name2)
