from pagetools.src.Page import Page

from collections import Counter
import string
import json
import csv
from typing import Union

import click
from lxml import etree


@click.command("get_codec", help="Retrieves codec of PAGE XML files.")
@click.argument("files", nargs=-1, required=True)
@click.option("-l", "--level", type=click.Choice(["region", "line", "word", "glyph"]), default="line")
@click.option("-idx", "--index", default=None, type=int,
              help="Considers only text from TextEquiv elements with a certain index.")
@click.option("-mc", "--most-common", default=None, type=int,
              help="Only prints n most common entries. Shows all by default.")
@click.option("-o", "--output", help="File to which results are written.")
@click.option("-rw", "--remove-whitespace", is_flag=True, default=False)
@click.option("-of", "--output-format", type=click.Choice(["json", "csv", "txt"]), default="json",
              help="Available result formats.")
@click.option("-freq", "--frequencies", is_flag=True, default=False, help="Outputs character frequencies.")
@click.option("--text-output-newline", is_flag=True, default=False,
              help="Inserts new line after every character in txt output. Only applies when frequencies aren't output.")
@click.option("--verbose/--silent", default=True, help="Choose between verbose or silent output.")
def get_codec_cli(files, level, index, most_common, output, remove_whitespace, output_format, frequencies,
                  text_output_newline, verbose):
    codec = Counter()

    xpath = build_xpath(level, index)

    with click.progressbar(files) as _files:
        for file in _files:
            try:
                page = Page(file)
            except etree.XMLSyntaxError:
                click.echo(f"{file}: Not a valid XML file. Skipping…", err=True)
                continue
            except etree.ParseError:
                click.echo(f"{file}: XML can't be parsed. Skipping…", err=True)
                continue

            tree = page.tree.getroot()
            for text_equiv in tree.findall(xpath, namespaces=page.get_ns()):
                text_content = "".join(text_equiv.itertext())
                codec.update(clean_text(text_content, remove_whitespace))

    codec_dict = {k: v for k, v in codec.most_common(most_common)}

    if verbose:
        for value, count in codec_dict.items():
            if frequencies:
                print(value, count)
            else:
                print(value)

    if output:
        serialize(codec_dict, output, output_format, frequencies, text_output_newline)


def build_xpath(level: str, index: Union[None, int]) -> str:
    element_names = {
        "region": "TextRegion",
        "line": "TextLine",
        "word": "Word",
        "glyph": "Glyph"
    }

    elem_name = element_names[level]

    xpath = f".//page:{elem_name}/page:TextEquiv" if not index else f".//page:{elem_name}/page:TextEquiv[@index={index}]"
    return xpath


def clean_text(text: str, remove_whitespace: bool) -> str:
    if remove_whitespace:
        text = text.translate(str.maketrans('', '', string.whitespace))
    return text


def serialize(codec: dict, output, out_format: str, freq: bool, text_output_newline: bool):
    if out_format == "json":
        json_dicts = []

        for key, value in codec.items():
            json_dicts.append({"character": key, "frequency": value})

        with open(output, "w", encoding="utf-8") as outfile:
            json.dump(json_dicts, outfile, indent=4)
    elif out_format == "csv":
        header = ["character", "frequency"]

        with open(output, "w") as outfile:
            csv_writer = csv.writer(outfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            csv_writer.writerow(header)
            for row in codec:
                csv_writer.writerow([row, codec[row]])

    elif out_format == "txt":
        with open(output, "w", encoding="utf-8") as outfile:
            sep = "\n" if not text_output_newline else ""
            if freq:
                outfile.write("\n".join([f"{k} {v}" for k, v in codec.items()]))
            else:
                outfile.write(f"{sep}".join(codec.keys()))


if __name__ == "__main__":
    get_codec_cli()
