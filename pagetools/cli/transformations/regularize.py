from pagetools.src.regularization.Regularizer import Regularizer
from pagetools.src.regularization.Rules import Ruleset
from pagetools.src.utils.filesystem import get_suffix

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import json
from typing import List
from pathlib import Path
import shutil

import click


default_rulesets = ["default", "ligatures_consonantal", "ligatures_vocal", "punctuation", "quotes", "roman_digits",
                   "spaces", "uvius", "various"]


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
@click.option("-s/-us", "--safe/--unsafe", default=True,
              help="Creates backups of original files before overwriting.")
def regularize_cli(xmls: List[str], remove_default: List[str], add_default: List[str], no_default: bool,
                   rules: List[str], safe: bool):
    xmls = list(map(Path, xmls))
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
            regularizer = Regularizer(xml, ruleset)
            regularizer.regularize()

            if safe:
                shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
            regularizer.export(xml)


def collect_default_rulesets(remove_default: List[str], add_default: List[str], no_default: bool):
    _default_rulesets = [] if no_default else default_rulesets.copy()
    rules = []

    for ruleset in remove_default:
        _default_rulesets.remove(ruleset)
    for ruleset in add_default:
        _default_rulesets.append(ruleset)

    for ruleset in set(_default_rulesets):
        with pkg_resources.path("pagetools.resources.rulesets", f"{ruleset}.json") as json_file:
            _json = json.loads(json_file.read_text())
        r = Ruleset()
        r.from_json(_json)
        rules.append(r)

    return rules

