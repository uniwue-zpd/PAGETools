from pagetools.src.utils import filesystem
from pagetools.src.utils.filesystem import get_suffix
from pagetools.src.Page import Page

import shutil
from pathlib import Path
from typing import List

import click
from lxml import etree


@click.command("change-index", help="Change index on TextEquiv elements.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.argument("source", required=True, type=str)
@click.argument("target", required=True, type=str)
@click.option("-s/-us", "--safe/--unsafe", default=True,
              help="Creates backups of original files before overwriting.")
def change_index_cli(xmls: List[str], source: str, target: str, safe: bool):
    # TODO: Very basic implementation for immediate use, needs refactoring!
    xmls = filesystem.parse_file_input(xmls)

    with click.progressbar(iterable=xmls, fill_char=click.style("█", dim=True),
                           label="Changing indices…") as _xmls:
        for xml in _xmls:
            try:
                page = Page(xml)
            except etree.XMLSyntaxError:
                click.echo(f"{xml}: Couldn't get parsed.")
                continue

            text_equivs = page.get_text_equivs()

            for text_equiv in text_equivs:
                if text_equiv.get("index") == target:
                    text_equiv.getparent().remove(text_equiv)
                elif (text_equiv.get("index") == source) or (text_equiv.get("index") is None and source == "None"):
                    text_equiv.set("index", target)

            if safe:
                shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
            page.export(xml)


if __name__ == "__main__":
    change_index_cli()
