from pathlib import Path
import zipfile
import time
from typing import List, Dict, Iterator
import glob

import click


def get_file_base(path: Path) -> Path:
    """Removes all extensions (as in everything after the first dot in the filename) from a Path

    :param path: Original Path obj
    :return: Path obj without any extensions
    """
    return Path(path.parent, path.name.split(".")[0])


def get_file_basename(path: Path) -> str:
    """Extracts filename w/o any extensions (as in everything after the first dot in the filename) from a Path

    :param path: Original Path obj
    :return: String representation of bare filename w/o extensions as
    """
    return get_file_base(path).name


def get_suffix(path: Path) -> str:
    """Extracts full extension (as in everything after the first dot in the filename) from Path

    :param path: Original Path obj
    :return: String representation of full filename extension
    """
    return f".{'.'.join(path.name.split('.')[1:])}"


def collect_cullable_files(files: List[str], xml_extension: List[str]) -> Dict[Path, List[Path]]:
    # TODO: Finish cull
    cullable_files = []

    for file in files:
        pass


def parse_file_input(files: List[str]) -> List[Path]:
    collected_files = []

    for file in files:
        if Path(file).is_file():
            collected_files.append(Path(file))
        else:
            globbed_files = glob.glob(file)
            for _file in globbed_files:
                collected_files.append(Path(_file))
    return collected_files


def collect_files(xml_files: Iterator[Path], img_extension: str) -> Dict[Path, List[Path]]:
    """Collects files for region extraction

    :param xml_files:
    :param img_extension:
    :return:
    """
    file_dict = {}

    for xml in xml_files:
        if xml.is_file():
            file_dict[xml] = [image for image in xml.parent.glob("*") if
                              (get_file_basename(xml) == get_file_basename(image) and str(image).endswith(img_extension))]
        else:
            globbed_files = glob.glob(xml)
            for _file in globbed_files:
                file_dict[xml] = [image for image in _file.parent.glob("*") if
                                  (get_file_basename(xml) == get_file_basename(image) and str(image).endswith(
                                      img_extension))]
    return file_dict


def write_text_file(text: str, filename: Path):
    """

    :param text:
    :param filename:
    :return:
    """
    with filename.open("w") as textfile:
        textfile.write(text)


def zip_files(files: List[Path]):
    """

    :param files:
    :param archive:
    :return:
    """
    filename = f"{time.strftime('%Y%m%d-%H%M%S')}.zip"

    with zipfile.ZipFile(filename, "w") as _zip:
        click.echo("Archiving output…")
        with click.progressbar(iterable=files, fill_char=click.style("█", dim=True)) as _files:
            for file in _files:
                _zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        click.echo(f"Output successfully archived as {filename}")
