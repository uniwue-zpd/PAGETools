from pagetools.src.line2page.Line2Page import Line2Page

from pathlib import Path
import click
import time
import multiprocessing
from multiprocessing import Semaphore


@click.command("line2page", help="Merges line images and text to combined image with PAGE XML annotation")
@click.option('-c', '--creator', default='user', help='Creator tag for PAGE XML')
@click.option('-s', '--source-folder', default=Path.cwd(), help='Path to images and GT')
@click.option('-i', '--image-folder', default='', help='Path to images')
@click.option('-gt', '--gt-folder', default='', help='Path to GT')
@click.option('-d', '--dest-folder', default=Path(Path.cwd(), 'merged'), help='Path to merge objects')
@click.option('-e', '--ext', default='.bin.png', help='Image extension')
@click.option('-p', '--pred', default=False, type=bool, help='Set flag to also store .pred.txt')
@click.option('-l', '--lines', default=20, type=int, help='Lines per page')
@click.option('-ls', '--line-spacing', default=5, type=int, help='Line spacing (in pixel)')
@click.option('-b', '--border', default=10, type=int, help='Border (in pixel)')
@click.option('--debug', default=False, help='Prints debug XML')
@click.option('--threads', default=16, type=int, help='Thread count to be used')
def line2page_cli(creator, source_folder, image_folder, gt_folder, dest_folder, ext, pred, lines, line_spacing, border,
                  debug, threads):
    image_path = source_folder if not image_folder else image_folder
    gt_path = source_folder if not gt_folder else gt_folder

    tic = time.perf_counter()
    opt_obj = Line2Page(creator, source_folder, image_path, gt_path, dest_folder, ext, pred, lines, line_spacing,
                        border, debug, threads)
    opt_obj.match_files()
    click.echo("object created")
    opt_obj.match_files()
    pages = list(opt_obj.chunks(opt_obj.matches, opt_obj.lines))
    pages = opt_obj.name_pages(pages)

    i = 0
    processes = []
    concurrency = opt_obj.threads
    click.echo("Currently using " + str(concurrency) + " Thread(s)")
    sema = Semaphore(concurrency)
    for page in pages:
        sema.acquire()
        opt_obj.progress(i + 1, len(pages) * 2, "Processing page " + str(i + 1) + " of " + str(len(pages)))
        process = multiprocessing.Process(target=opt_obj.make_page, args=(page, sema,))
        processes.append(process)
        process.start()
        i += 1

    for process in processes:
        opt_obj.progress(i + 1, len(pages) * 2,
                         "Finishing page " + str((i + 1) - len(pages)) + " of " + str(len(pages)))
        process.join()
        i += 1
    toc = time.perf_counter()
    click.echo(f"\nFinished merging in {toc - tic:0.4f} seconds")
    click.echo("\nPages have been stored at ", opt_obj.dest)


if __name__ == '__main__':
    line2page_cli()