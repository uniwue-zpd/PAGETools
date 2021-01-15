from pagetools.src.utils import filesystem
from pagetools.src.Extractor import TextLineExtractor

import click
from pathlib import Path


@click.command()
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-ie", "--image-extension", default=".png", type=str, help="Extension of image files. Must be in the same"
                                                                         " directory as corresponding XML file.")
@click.option("-o", "--output", type=str, default=Path.cwd(), help="Path where generated files will get saved.")
@click.option("-e", "--enumerate-output", is_flag=True, help="Enumerates output file names instead of using original "
                                                             "names.")
@click.option("-z", "--zip-output", is_flag=True, help="Add generated output to zip archive.")
@click.option("-bg", "--background-color", nargs=3, default=(255, 255, 255), type=int,
              help="RGB color code used to fill up background. Used when padding and / or deskewing.")
@click.option("--background-mode", type=click.Choice(["median", "mean", "dominant"]),
              help="Color calc mode to fill up background (overwrites -bg / --background-color).")
@click.option("-p", "--padding", nargs=4, default=(0, 0, 0, 0), type=int, help="Padding in pixels around the line image"
                                                                               " cutout (top, bottom, left, right).")
@click.option("-ad", "--auto-deskew", is_flag=True, help="Automatically deskew extracted line images (Experimental!).")
@click.option("-d", "--deskew", default=0.0, type=float, help="Angle for manuel clockwise rotation of the line images.")
@click.option("-gt", "--gt-index", type=int, default=0, help="Index of the TextEquiv elements containing ground truth.")
@click.option("-pred", "--pred-index", type=int, default=1, help="Index of the TextEquiv elements containing predicted "
                                                                 "text.")
def main(xmls, image_extension, output, enumerate_output, background_color, background_mode, padding, zip_output,
         gt_index, pred_index, auto_deskew, deskew):
    file_dict = filesystem.collect_files(map(Path, xmls), image_extension)

    if background_mode:
        bg = ("calculate", background_mode)
    else:
        bg = ("color", background_color)

    enumerator = [1]
    click.echo(f"Found {len(file_dict)} PAGE XML files…")

    with click.progressbar(iterable=file_dict.items(), fill_char=click.style("█", dim=True),
                           label="Extracting text lines…") as files:
        for page_idx, (xml, images) in enumerate(files):
            extractor = TextLineExtractor(xml, images, output, enumerate_output, bg, padding, auto_deskew, deskew,
                                          gt_index, pred_index)
            extractor.extract_line_text_pairs(enumerator)

    click.echo(click.style("Text line extraction finished successfully.", fg='green'))

    if zip_output:
        filesystem.zip_files(files)


if __name__ == "__main__":
    main()
