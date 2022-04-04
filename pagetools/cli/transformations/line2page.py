from pagetools.src.line2page.Line2Page import Line2Page

from pathlib import Path

import click


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

    option_object = Line2Page(creator, source_folder, image_path, gt_path, dest_folder, ext, pred, lines, line_spacing,
                              border, debug, threads)
    option_object.match_files()


if __name__ == '__main__':
    line2page_cli()
