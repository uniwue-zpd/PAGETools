from pagetools.src.utils import filesystem
from pagetools.src.extraction.Extractor import Extractor
from pagetools.src.utils.constants import extractable_regions

import click
from pathlib import Path

available_regions = extractable_regions.copy()
available_regions.append("*")


@click.command("extract", help="Extract elements as image (optionally with text) files.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("--include", multiple=True, type=click.Choice(available_regions, case_sensitive=False),
              help="PAGE XML element types to extract (highest priority).")
@click.option("--exclude", multiple=True, type=click.Choice(available_regions, case_sensitive=False),
              help="PAGE XML element types to exclude from extraction (lowest priority).")
@click.option("--no-text", is_flag=True, type=bool, default=False, help="Suppresses text extraction.")
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
@click.option("-ad", "--auto-deskew", is_flag=True, help="Automatically deskew extracted line images using a custom "
                                                         "algorithm (Experimental!).")
@click.option("-d", "--deskew", default=0.0, type=float, help="Angle for manual clockwise rotation of the line images.")
@click.option("-gt", "--gt-index", type=int, default=0, help="Index of the TextEquiv elements containing ground truth.")
@click.option("-pred", "--pred-index", type=int, default=1, help="Index of the TextEquiv elements containing predicted "
                                                                 "text.")
def extract_cli(xmls, include, exclude, no_text, image_extension, output, enumerate_output, background_color,
                background_mode, padding, zip_output, gt_index, pred_index, auto_deskew, deskew):
    file_dict = filesystem.collect_files(map(Path, xmls), image_extension)

    if not file_dict:
        click.echo(click.style("No XML files found.\nAborting…", fg='red'))
        return

    if background_mode:
        bg = ("calculate", background_mode)
    else:
        bg = ("color", background_color)

    enumerator = [1]
    click.echo(f"Found {len(file_dict)} PAGE XML files…")

    with click.progressbar(iterable=file_dict.items(), fill_char=click.style("█", dim=True),
                           label="Extracting text lines…") as files:
        for page_idx, (xml, images) in enumerate(files):
            extractor = Extractor(xml, images, include, exclude, no_text, output, enumerate_output, bg, padding, auto_deskew,
                                  deskew, gt_index, pred_index)
            extractor.extract(enumerator)

    click.echo(click.style("Text line extraction finished successfully.", fg='green'))

    if zip_output:
        filesystem.zip_files(files)


if __name__ == "__main__":
    extract_cli()

