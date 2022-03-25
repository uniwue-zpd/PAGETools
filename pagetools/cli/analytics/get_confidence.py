from pagetools.src.utils import filesystem
from pagetools.src.Page import Page

from typing import List
import csv
from pathlib import Path
from statistics import mean

import click


@click.command("get-confidence", help="Returns the average prediction confidence of a set of PAGE XML files")
@click.argument("files", nargs=-1, required=True)
@click.option("-e", "--element", type=click.Choice(["TextRegion", "TextLine", "Word", "Glyph"]), default="Glyph")
@click.option("-i", "--index", type=int, default=1)
@click.option("-o", "--output", type=str, default="confidence_map.csv", help="Output directory for stats csv file.")
def get_confidence_cli(files: List[str], element: str, index: int, output=str):
    # TODO: Needs refactoring. Was implemented fast for a urgent use case.
    collected_files = filesystem.parse_file_input(files)
    confidence_map = {}

    for file in collected_files:
        page_confidences = []

        page = Page(file)
        root = page.get_tree(root=True)

        if root is None:
            continue
        if index == "None":
            xpath = f".//page:{element}/page:TextEquiv[not(@index)]"
        else:
            xpath = f'.//page:{element}/page:TextEquiv[@index="{index}"]'
        hits = root.xpath(xpath, namespaces=page.get_ns())

        for hit in hits:
            page_confidences.append(float(hit.get("conf")))

        confidence_map[file] = mean(page_confidences) if len(page_confidences) > 0 else 0

    with Path(output).open("w") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerow(["File", "Average Confidence"])
        for file, conf in confidence_map.items():
            csv_writer.writerow([file, conf])





