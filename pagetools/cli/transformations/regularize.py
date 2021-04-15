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


@click.command("regularize",
               help="Regularize the text content of PAGE XML files using custom rulesets.")
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-dr/-ndr", "--default-rules/--no-default-rules", default=True,
              help="Loads default ruleset.")
@click.option("-dp/-ndp", "--default-punctuation/--no-default-punctuation", default=True,
              help="Loads default punctuation ruleset.")
@click.option("-ds/-nds", "--default-spaces/--no-default-spaces", default=True,
              help="Loads default spaces ruleset.")
@click.option("-nd", "--no-default", is_flag=True,
              help="Disables all default rulesets. Overrides all other --default-* options.")
@click.option("-r", "--rules", type=click.Path(), multiple=True,
              help="File(s) which contains serialized ruleset.")
@click.option("-s/-us", "--safe/--unsafe", default=True,
              help="Creates backups of original files before overwriting.")
def regularize_cli(xmls: List[str], default_rules: bool, default_punctuation: bool, default_spaces: bool, no_default: bool,
                   rules: List[str], safe: bool):
    xmls = list(map(Path, xmls))
    rules = list(map(Path, rules))
    rulesets: List[Ruleset] = []

    if not no_default:
        if default_rules:
            with pkg_resources.path("pagetools.resources.rulesets", "default.json") as json_file:
                _json = json.loads(json_file.read_text())
            r = Ruleset()
            r.from_json(_json)
            rulesets.append(r)
        if default_punctuation:
            with pkg_resources.path("pagetools.resources.rulesets", "punctuation.json") as json_file:
                _json = json.loads(json_file.read_text())
            r = Ruleset()
            r.from_json(_json)
            rulesets.append(r)
        if default_spaces:
            with pkg_resources.path("pagetools.resources.rulesets", "spaces.json") as json_file:
                _json = json.loads(json_file.read_text())
            r = Ruleset()
            r.from_json(_json)
            rulesets.append(r)

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
