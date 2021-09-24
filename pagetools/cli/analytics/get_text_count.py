from pagetools.src.utils import filesystem
from pagetools.src.utils.constants import TEXT_COUNT_SUPPORTED_ELEMS

from pagetools.src.Page import Page

from typing import List
import csv
from pathlib import Path

import click


@click.command("get_text_count",
               help="Returns the amount of text equiv elements in certain elements for certain indices.")
@click.argument("files", nargs=-1, required=True)
@click.option("-e", "--element", multiple=True, type=click.Choice(TEXT_COUNT_SUPPORTED_ELEMS),
              default=TEXT_COUNT_SUPPORTED_ELEMS)
@click.option("-i", "--index", multiple=True, required=True)
@click.option("-so", "--stats-out", help="Output directory for detailed stats csv file.")
def get_text_count_cli(files: List[str], element: List[str], index: List[str], stats_out: str):
    # TODO: Needs refactoring. Was implemented fast for a urgent use case.
    counter = 0
    stats = []

    collected_files = filesystem.parse_file_input(files)
    for file in collected_files:
        page = Page(file)

        root = page.get_tree(True)

        if root is None:
            continue

        for elem in element:
            for idx in index:
                if idx == "None":
                    xpath = f".//page:{elem}/page:TextEquiv[not(@index)]"
                else:
                    xpath = f'.//page:{elem}/page:TextEquiv[@index="{idx}"]'

                hits = len(root.xpath(xpath, namespaces=page.get_ns()))

                counter += hits
                stats.append({"page": file, "element": elem, "index": idx, "hits": hits})
    idx_hits = get_index_hits(index, stats)
    elem_hits = get_elem_hits(element, stats)

    click.echo(click.style(f"Total count: {counter}", bold=True))
    click.echo("-"*20)
    click.echo(click.style("Count per index", bold=True))
    for idx in idx_hits:
        click.echo(click.style(f"{idx[0]}: {idx[1]}"))
    click.echo("-"*20)
    click.echo(click.style("Count per element", bold=True))
    for elem in elem_hits:
        click.echo(click.style(f"{elem[0]}: {elem[1]}"))

    if stats_out:
        with Path(stats_out).open("w") as csvfile:
            stats_writer = csv.writer(csvfile,
                                      delimiter=',',
                                      quotechar='"',
                                      quoting=csv.QUOTE_ALL)
            header = ["page", "element", "index", "count"]
            stats_writer.writerow(header)
            for entry in stats:
                stats_writer.writerow([entry["page"], entry["element"], entry["index"], entry["hits"]])


def get_index_hits(index: List[str], stats: List[dict]) -> List[tuple]:
    idx_hits = []
    for idx in index:
        counter = 0
        for entry in stats:
            if entry["index"] == idx:
                counter += entry["hits"]
        idx_hits.append((idx, counter))
    return idx_hits


def get_elem_hits(elements: List[str], stats: List[dict]) -> List[tuple]:
    elem_hits = []
    for elem in elements:
        counter = 0
        for entry in stats:
            if entry["element"] == elem:
                counter += entry["hits"]
        elem_hits.append((elem, counter))
    return elem_hits


if __name__ == "__main__":
    get_text_count_cli()
