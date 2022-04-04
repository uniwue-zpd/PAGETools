import lxml

# keep this
import time
import glob
from pathlib import Path
import click
import sys
import multiprocessing
from multiprocessing import Semaphore
from PIL import Image

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


def chunks(lst, n):
    """Yields successive n-sized chunks from lst"""
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def name_pages(pages):
    """
    returns a list of all objects in pages with pagename followed by a 4-digit pagenumber
    removed iterative
    """
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


def progress(count, total, status='.'):
    """displays a progress bar"""
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '_' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def make_page(page_with_name, semaphore):
    merged =


class CliOptions:
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
        self.spacer = 5
        self.img_ext = '.nrm.png'

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
                print(
                    "WARNING: The File " + str(self.gt_folder) + img_name + ".gt.txt could not be found! Omitting line from page")
        print("matching files")


    def merge_images(self, page):
        """Merge list of images into one, displayed on top of each other
        :return: the merged Image object
        """
        img_list = []
        img_width = 0
        img_height = 0
        spacer_height = self.spacer * (len(page) - 1)
        for line in page:
            image_data = Image.open(line[0])
            image = image_data.copy()
            image_data.close()
            (width, height) = image.size
            img_width = max(img_width, width)
            img_height += height
            img_list.append(image)
        if 'nrm' not in self.img_ext:
            result = Image.new('RGB', (img_width + self.border * 2, img_height + self.border * 2 + spacer_height), (255, 255, 255))
        else:
            result = Image.new('LA', (img_width + self.border))


@click.command()
@click.option('-c', '--creator', default='user', help='Creator tag for PAGE XML')
@click.option('-s', '--source_folder', default=Path.cwd(), help='Path to images and GT')
@click.option('-i', '--image_folder', default='', help='Path to images')
@click.option('-gt', '--gt_folder', default='', help='Path to GT')
@click.option('-d', '--dest_folder', default=Path(Path.cwd(), 'merged'), help='Path to merge objects')
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
    click.echo("start cli()")
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
    click.echo("object created")
    option_object.match_files()
    pages = list(chunks(option_object.matches, option_object.lines))
    pages = name_pages(pages)

    i = 0
    processes = []
    concurrency = option_object.threads
    click.echo("Currently using " + str(concurrency) + " Thread(s)")
    sema = Semaphore(concurrency)
    for page in pages:
        sema.acquire()
        progress(i + 1, len(pages) * 2, "Processing page " + str(i + 1) + " of " + str(len(pages)))
        processes = multiprocessing.Process(target=)
    click.echo("cli() finished")


if __name__ == '__main__':
    """python script to merge GT lines to page images and xml

        tic = time counter
        options = object with the desired meta data
    """
    tic = time.perf_counter()
    # options = cli(standalone_mode=False)
    # options.match_files()
    click.echo("call cli()")
    cli()
    click.echo("\nProgramm finished")

# help(Parser)
# help(main)
"""
path = "/home/User/Documents/file.txt"
obj = Path(path)
print(obj)
print(obj.name)
print(obj.is_dir())
cur_dir = Path.cwd()
print(cur_dir)
print(cur_dir.is_dir())
# print(os.path.basename(path))
name = strip_path(path.split('.')[0])
name2 = strip_path(path)
print("\n" + path)
print(name)
print(name2)
"""