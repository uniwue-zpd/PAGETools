from pagetools.src.Regularizer import Regularizer
from pagetools.src.Rules import Ruleset
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


@click.command("regularize", help="Regularize the text content of PAGE XML files using custom rulesets.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-r", "--rules", type=click.Path(), multiple=True, help="File(s) which contains serialized ruleset.")
@click.option("-s/-us", "--safe/--unsafe", default=True, help="Creates backups of original files before overwriting.")
def regularize_cli(xmls: List[str], rules: List[str], safe: bool):
    xmls = list(map(Path, xmls))
    rules = list(map(Path, rules))
    rulesets: List[Ruleset] = []

    if rules:
        for rules_file in rules:
            if get_suffix(rules_file).endswith(".json"):
                try:
                    r = Ruleset()
                    r.from_json(rules_file)
                    rulesets.append(r)
                except:
                    click.echo("Couldn't parse ruleset", err=True)
            # TODO add further input formats
            else:
                click.echo("Ruleset format not yet supported", err=True)
    else:
        with pkg_resources.path("pagetools.resources", "default_ruleset.json") as json_file:
            _json = json.loads(json_file.read_text())
        r = Ruleset()
        r.from_json(_json)
        rulesets.append(r)

    ruleset = sum(rulesets, Ruleset())

    with click.progressbar(iterable=xmls, fill_char=click.style("█", dim=True),
                           label="Regularising text…") as _xmls:
        for xml in _xmls:
            regularizer = Regularizer(xml, ruleset)
            regularizer.regularize()

            if safe:
                shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
            regularizer.export(xml)
