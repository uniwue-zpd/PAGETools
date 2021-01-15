# TODO
# from pagetools.src.Page import Page
#
# from collections import Counter
# import string
# import json
# import csv
#
# import click
#
#
# @click.command()
# @click.argument("files", nargs=-1, required=True)
# @click.option("-o", "--output", help="File to which results are written.")
# @click.option("-rw", "--remove-whitespace", is_flag=True, default=False)
# @click.option("-of", "--output-format", type=click.option(["json", "csv", "txt"]), default="txt", help="Available result formats.")
# @click.option("-mc", "--most-common", default=None, type=int, help="Only prints n most common entries. Shows all by default.")
# @click.option("-freq", "--frequencies", is_flag=True, default=False, help="Outputs character frequencies.")
# def main(files, output, output_format, most_common, frequencies, remove_whitespace):
#     codec = Counter()
#
#     with click.progressbar(files) as _files:
#         for file in _files:
#             page = Page(file)
#
#             for line in page.get_text_lines_data():
#                 for text in line["text_equivs"]:
#                     codec.update(clean_text(text["content"], remove_whitespace))
#
#     for value, count in codec.most_common(most_common):
#         if frequencies:
#             print(value, count)
#         else:
#             print(value)
#
#     if output:
#         serialize(codec, output, output_format, frequencies)
#
#
# def clean_text(text: str, remove_whitespace: bool) -> str:
#     if remove_whitespace:
#         text = text.translate(str.maketrans('', '', string.whitespace))
#     return text
#
#
# def serialize(codec: Counter, output, out_format: str, freq: bool):
#     if out_format == "json":
#         with open(output, "w", encoding="unicode") as outfile:
#             json.dump(dict(), outfile, indent=4)
#     elif out_format == "csv":
#         pass
#     elif out_format == "txt":
#         pass
#
#
# if __name__ == "__main__":
#     main()
