from pagetools.src.Regularizer import Regularizer
from pagetools.src.Rules import Ruleset
from pagetools.src.utils.filesystem import get_suffix

from pathlib import Path
import shutil
import pkg_resources

import click


@click.command()
@click.argument("xmls", nargs=-1, required=True, type=click.Path())
@click.option("-r", "--rules", type=click.Path(), multiple=True, help="File which contains serialized ruleset.")
@click.option("-s", "--safe", is_flag=True, default=True, help="Creates backups of original files.")
def main(xmls, rules, safe):
    rules = Path(rules) if rules else None
    xmls = map(Path, xmls)

    ruleset = Ruleset()
    if rules:
        if get_suffix(rules).endswith(".json"):
            ruleset.from_json(rules)
        # TODO add further input formats
        else:
            click.echo("Ruleset format not supported.", err=True)
            return
    else:
        # TODO
        default_ruleset = pkg_resources.resource_filename("pagetools", "resources/default_ruleset.json")
        print(default_ruleset)
        ruleset.from_json(Path(default_ruleset))

    for xml in xmls:
        regularizer = Regularizer(xml, ruleset)
        regularizer.regularize()

        if safe:
            shutil.move(xml, Path(xml.parent, xml.stem).with_suffix(f".old{get_suffix(xml)}"))
        regularizer.export(xml)


if __name__ == "__main__":
    main()
