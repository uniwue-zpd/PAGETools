from pagetools.src.utils import filesystem

from pagetools.src.regularization.Regularizer import Regularizer
from pagetools.src.regularization.Rules import Ruleset
from pagetools.src.utils.filesystem import get_suffix

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import json
from typing import List, Union
from pathlib import Path
import shutil

import click
from lxml import etree


default_rulesets = ["various", "quotes", "ligatures_consonantal", "ligatures_vocal", "roman_digits", "uvius",
                    "punctuation", "spaces"]


@click.command("regularize",
               help="Regularize the text content of PAGE XML files using custom rulesets.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("--remove-default", multiple=True, type=click.Choice(default_rulesets),
              help="Removes specified default ruleset.")
@click.option("--add-default", multiple=True, type=click.Choice(default_rulesets),
              help="Adds specified default ruleset. Overrides all other default options.")
@click.option("-nd", "--no-default", is_flag=True, default=False,
              help="Disables all default rulesets.")
@click.option("-r", "--rules", type=click.Path(), multiple=True,
              help="File(s) which contains serialized ruleset.")
@click.option("-nu", "--normalize-unicode", type=click.Choice(["NFC", "NFD", "NFKC", "NFKD"]), default=None,
              help="Normalize unicode for both rules and PAGE XML tests.")
@click.option("-s/-us", "--safe/--unsafe", default=True,
              help="Creates backups of original files before overwriting.")
def regularize_cli(xmls: List[str], remove_default: List[str], add_default: List[str], no_default: bool,
                   rules: List[str], normalize_unicode: Union[None, str], safe: bool):
    xmls = filesystem.parse_file_input(xmls)
    rules = list(map(Path, rules))
    rulesets: List[Ruleset] = []

    rulesets.extend(collect_default_rulesets(remove_default, add_default, no_default))

    if rules:
        for rules_file in rules:
            if get_suffix(rules_file).endswith(".json"):
                try:
                    r = Ruleset()
                    r.from_json(rules_file)
                    rulesets.append(r)
                except:
                    click.echo("Couldn't parse ruleset. Skipping…", err=True)
                    continue
            else:
                click.echo("Ruleset format not yet supported. Skipping…", err=True)
                continue

    ruleset = sum(rulesets, Ruleset())

    with click.progressbar(iterable=xmls, fill_char=click.style("█", dim=True),
                           label="Regularising text…") as _xmls:
        for xml in _xmls:
            try:
                regularizer = Regularizer(xml, ruleset, normalize_unicode)
            except etree.XMLSyntaxError:
                click.echo(f"{xml}: Image couldn't get parsed.")
                continue
            regularizer.regularize()

            if safe:
                shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
            regularizer.export(xml)


def collect_default_rulesets(remove_default: List[str], add_default: List[str], no_default: bool,
                             normalize_unicode: Union[None, str] = None):
    _default_rulesets = [] if no_default else default_rulesets.copy()
    rules = []

    for ruleset in remove_default:
        _default_rulesets.remove(ruleset)
    for ruleset in add_default:
        _default_rulesets.append(ruleset)

    for ruleset in list(dict.fromkeys(_default_rulesets)):
        with pkg_resources.path("pagetools.resources.rulesets", f"{ruleset}.json") as json_file:
            _json = json.loads(json_file.read_text())
        r = Ruleset(normalize_unicode=normalize_unicode)
        r.from_json(_json)
        rules.append(r)

    return rules


if __name__ == "__main__":
    regularize_cli()
