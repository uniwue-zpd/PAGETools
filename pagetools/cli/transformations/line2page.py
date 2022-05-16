from pagetools.src.line2page.Line2Page import Line2Page

from pathlib import Path
import click
import time
import multiprocessing
from multiprocessing import Semaphore


@click.command("line2page", help="Merges line images and text to combined image with PAGE XML annotation")
@click.option('-c', '--creator', default='user', help='Creator tag for PAGE XML')
@click.option('-s', '--source-folder', required=True, help='Path to images and GT')
@click.option('-i', '--image-folder', default='', help='Path to images')
@click.option('-gt', '--gt-folder', default='', help='Path to GT')
@click.option('-d', '--dest-folder', default=Path(Path.cwd(), 'merged'), help='Path to merge objects')
@click.option('-e', '--ext', default='.bin.png', help='Image extension')
@click.option('-p', '--pred', default=False, type=bool, help='Set flag to also store .pred.txt')
@click.option('-l', '--lines', default=20, type=click.IntRange(min=0,clamp=True), help='Lines per page')
@click.option('-ls', '--line-spacing', default=5, type=click.IntRange(min=0,clamp=True), help='Line spacing in pixel; (top, bottom, left, right)')
@click.option('-b', '--border', nargs=4, default=(10, 10, 10, 10), type=click.IntRange(min=0,clamp=True), help='Border (in pixel)')
@click.option('--debug', default=False, type=bool, help='Prints debug XML')
@click.option('--threads', default=16, type=click.IntRange(min=1,clamp=True), help='Thread count to be used')
@click.option('--xml-schema', default='19', type=click.Choice(['17', '19']), help='Sets the year of the xml-Schema to be used')
def line2page_cli(creator, source_folder, image_folder, gt_folder, dest_folder, ext, pred, lines, line_spacing, border,
                  debug, threads, xml_schema):
    image_path = source_folder if not image_folder else image_folder
    gt_path = source_folder if not gt_folder else gt_folder

    tic = time.perf_counter()
    opt_obj = Line2Page(creator, source_folder, image_path, gt_path, dest_folder, ext, pred, lines, line_spacing,
                        border, debug, threads, xml_schema)
    opt_obj.match_files()
    pages = list(opt_obj.chunks(opt_obj.matches, opt_obj.lines))
    pages = opt_obj.name_pages(pages)

    i = 0
    processes = []
    concurrency = opt_obj.threads
    click.echo(f"Currently using {str(concurrency)} Thread(s)")
    sema = Semaphore(concurrency)
    for page in pages:
        sema.acquire()
        opt_obj.progress(i + 1, len(pages) * 2, f"Processing page {str(i + 1)} of {str(len(pages))}")
        process = multiprocessing.Process(target=opt_obj.make_page, args=(page, sema,))
        processes.append(process)
        process.start()
        i += 1

    for process in processes:
        opt_obj.progress(i + 1, len(pages) * 2, f"Finishing page {str((i + 1) - len(pages))} of {str(len(pages))}")
        process.join()
        i += 1
    toc = time.perf_counter()
    click.echo(f"\nFinished merging in {toc - tic:0.4f} seconds")
    click.echo(f"\nPages have been stored at {str(opt_obj.dest_folder)}")


if __name__ == '__main__':
    line2page_cli()
