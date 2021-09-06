import click

from pagetools.cli.analytics.get_text_count import get_text_count_cli
from pagetools.cli.analytics.get_codec import get_codec_cli

from pagetools.cli.transformations.extract import extract_cli
from pagetools.cli.transformations.regularize import regularize_cli
from pagetools.cli.transformations.change_index import change_index_cli


@click.group()
@click.version_option()
def cli(**kwargs):
    """
    CLI entrypoint for PAGETools CLI
    """


cli.add_command(get_text_count_cli)
cli.add_command(get_codec_cli)
cli.add_command(extract_cli)
cli.add_command(regularize_cli)
cli.add_command(change_index_cli)