import click

from pagetools.cli.transformations.extract import extract_cli
from pagetools.cli.transformations.regularize import regularize_cli

@click.group()
@click.version_option()
def cli(**kwargs):
    """
    CLI entrypoint for PAGETools CLI
    """


cli.add_command(extract_cli)
cli.add_command(regularize_cli)
