import os
import sys
import logging

import click

from ._search import search, advance_search
from ._citations import citations_cli
from pypubmed import version_info


log_level_maps = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}

__epilog__ = click.style('''
contact: {author} <{author_email}>
'''.format(**version_info), fg='bright_black')

@click.group(epilog=__epilog__, help=click.style(version_info['desc'], fg='bright_blue', bold=True))
@click.option('-l', '--log-level', help='the mode of log',
              show_default=True, default='debug',
              type=click.Choice(log_level_maps.keys()))
@click.option('-k', '--api-key', help='the api_key of NCBI Pubmed, NCBI_API_KEY environment is available',
              envvar='NCBI_API_KEY', show_envvar=True)
@click.version_option(version=version_info['version'], prog_name='pypubmed')
@click.pass_context
def cli(ctx, **kwargs):
    kwargs['log_level'] = log_level_maps[kwargs['log_level']]
    ctx.obj = kwargs


def main():
    cli.add_command(search)
    cli.add_command(advance_search)
    cli.add_command(citations_cli)
    cli()


if __name__ == '__main__':
    main()
