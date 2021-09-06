from pagetools.src.Page import Page
from pagetools.src.utils import filesystem

from typing import List

import click
from lxml import etree


@click.command("cull", help="Cull datasets based on different conditions. ")
@click.argument("files", nargs=-1, type=str, required=True)
@click.option("-xml", "--needs-xml", is_flag=True, help="Removes all images without any associated XML.")
@click.option("--xml-extension", type=str, default=".xml", multiple=True,
              help="Extension of XML files which are considered.")
@click.option("--text", "--needs-text", is_flag=True, help="Removes all XML files without any text content.")
@click.option("-text-index", "--needs-text-index", type=int, default=0, multiple=True,
              help="Removes all XML files without any text content without the specified index.")
@click.option("-d", "--dry-run", is_flag=True, help="Only prints cullable files to output.")
def cull_cli(files: List[str], xml: bool, xml_extension: List[str], text: bool, text_index: List[int], dry_run: bool):
    # TODO: finish cull
    files = filesystem.collect_cullable_files(files, xml_extension)

    for file in files:
        try:
            page = Page(file)
        except etree.XMLSyntaxError:
            click.echo(f"{file}: Not a valid XML file. Skipping…", err=True)
            continue
        except etree.ParseError:
            click.echo(f"{file}: XML can't be parsed. Skipping…", err=True)
            continue


if __name__ == "__main__":
    cull_cli()
