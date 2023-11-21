from pagetools.src.line2page.Line2Page import Line2Page

import logging
from typing import Tuple
from pathlib import Path
import time
import multiprocessing
from multiprocessing import Semaphore

import click


@click.command("line2page",
               help="Merges line images and line texts into combined images and XML files")
@click.option("-c",
              "--creator",
              type=str,
              default="PAGETools",
              help="Creator tag for PAGE XML",
              show_default=True)
@click.option("-s",
              "--source-folder",
              type=str,
              required=True,
              help="Path to images and GT")
@click.option("-i",
              "--image-folder",
              type=str,
              help="Path to images",
              show_default=True)
@click.option("-gt",
              "--gt-folder",
              type=str,
              help="Path to GT",
              show_default=True)
@click.option("-d",
              "--dest-folder",
              default=Path(Path.cwd(), "merged"),
              type=str,
              help="Path where output gets stored",
              show_default=True)
@click.option("-e",
              "--ext",
              default=".bin.png",
              type=str,
              help="Image extension",
              show_default=True)
@click.option("-p",
              "--pred",
              default=False,
              is_flag=True,
              help="Sets flag to also include .pred.txt",
              show_default=True)
@click.option("-l",
              "--lines",
              default=20,
              type=click.IntRange(min=0, clamp=True),
              help="Lines per page",
              show_default=True)
@click.option("-ls",
              "--line-spacing",
              default=5,
              type=click.IntRange(min=0, clamp=True),
              help="Spacing between lines (in pixel)",
              show_default=True)
@click.option("-oe",
              "--output-extension",
              type=str,
              help="Output image extension")
@click.option("-b",
              "--border",
              nargs=4,
              default=(10, 10, 10, 10),
              type=click.IntRange(min=0, clamp=True),
              help="Border (in pixel): TOP BOTTOM LEFT RIGHT", show_default=True)
@click.option("-bg",
              "--background-color",
              nargs=3,
              default=(255, 255, 255),
              type=click.IntRange(min=0, max=255, clamp=True),
              help="RGB background color",
              show_default=True)
@click.option("--debug",
              default="20",
              type=click.Choice(["10", "20", "30", "40", "50"]),
              help="Sets the level of feedback to receive: DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50",
              show_default=True)
@click.option("--threads",
              default=1,
              type=click.IntRange(min=1, clamp=True),
              help="Thread count to be used",
              show_default=True)
@click.option("--xml-schema",
              default="2019",
              type=click.Choice(["2017", "2019"]),
              help="Sets the year of the xml-Schema to be used",
              show_default=True)
def line2page_cli(creator: str,
                  source_folder: str,
                  image_folder: str,
                  gt_folder: str,
                  dest_folder: str,
                  ext: str,
                  pred: str,
                  lines: int,
                  line_spacing: int,
                  output_extension: str,
                  border: Tuple[int],
                  background_color: Tuple[int],
                  debug: bool,
                  threads: int,
                  xml_schema: str):
    image_path = source_folder if not image_folder else image_folder
    gt_path = source_folder if not gt_folder else gt_folder

    logging.basicConfig(level=int(debug))
    log = logging.getLogger(__name__)
    tic = time.perf_counter()

    opt_obj = Line2Page(creator, source_folder, image_path, gt_path, dest_folder, ext, pred, lines, line_spacing,
                        output_extension, border, background_color, debug, threads, xml_schema)
    opt_obj.match_files()

    pages = list(opt_obj.chunks(opt_obj.matches, opt_obj.lines))
    pages = opt_obj.name_pages(pages)

    processes = []
    concurrency = opt_obj.threads
    log.info(f" Currently using {str(concurrency)} Thread(s)")
    sema = Semaphore(concurrency)

    with click.progressbar(pages, label=f"Processing {len(pages)} Pages") as bar_processing:
        for page in bar_processing:
            sema.acquire()
            process = multiprocessing.Process(target=opt_obj.make_page, args=(page, sema,))
            processes.append(process)
            process.start()

    with click.progressbar(processes, label=f"Finishing {len(processes)} Pages") as bar_finishing:
        for process in bar_finishing:
            process.join()

    toc = time.perf_counter()
    log.info(f" Finished merging in {toc - tic:0.4f} seconds")
    log.info(f" Pages have been stored at {str(opt_obj.dest_folder)}")


if __name__ == '__main__':
    line2page_cli()
