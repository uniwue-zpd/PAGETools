from pagetools.src.Regularizer import Regularizer
from pagetools.src.Rules import Ruleset
from pagetools.src.utils.filesystem import get_suffix

from typing import List
from pathlib import Path
import shutil
import pkg_resources

import click


@click.command()
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-r", "--rules", type=click.Path(), multiple=True, help="File which contains serialized ruleset.")
@click.option("-s", "--safe", is_flag=True, default=True, help="Creates backups of original files.")
def main(xmls, rules, safe):
    xmls = map(Path, xmls)
    rules = map(Path, rules)
    rulesets: List[Ruleset] = []

    if rules:
        for rules_file in rules:
            _ruleset = Ruleset()
            if get_suffix(rules_file).endswith(".json"):
                _ruleset.from_json(rules_file)
                rulesets.append(_ruleset)
            # TODO add further input formats
            else:
                click.echo("Ruleset format not supported.", err=True)
                return
    else:
        # TODO
        default_ruleset = pkg_resources.resource_filename("pagetools", "resources/default_ruleset.json")
        _ruleset = Ruleset().from_json(Path(default_ruleset))
        rulesets.append(_ruleset)

    ruleset = sum(rulesets, Ruleset())

    for xml in xmls:
        regularizer = Regularizer(xml, ruleset)
        regularizer.regularize()

        if safe:
            shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
        regularizer.export(xml)


if __name__ == "__main__":
    main()
