import os
import sys
import logging

import click

from ._search import search, advance_search
from ._citations import citations_cli
from pypubmed import version_info
from pypubmed.core.eutils import Eutils


log_level_maps = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}

__epilog__ = click.style('contact: {author} <{author_email}>'.format(**version_info), fg='bright_black')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS, epilog=__epilog__, help=click.style(version_info['desc'], fg='bright_blue', bold=True))
@click.option('-l', '--log-level', help='the mode of loggging',
              show_default=True, default='debug',
              type=click.Choice(log_level_maps.keys()))
@click.option('-k', '--api-key', help='the api_key of NCBI Pubmed, NCBI_API_KEY environment is available',
              envvar='NCBI_API_KEY', show_envvar=True)
@click.option('-u', '--url', help='the service url of google translate', default='translate.google.cn', show_default=True)
@click.version_option(version=version_info['version'], prog_name='pypubmed')
@click.pass_context
def cli(ctx, **kwargs):

    kwargs['log_level'] = log_level_maps[kwargs['log_level']]
    e = Eutils(api_key=kwargs['api_key'], service_url=kwargs['url'])
    e.logger.level = int(kwargs['log_level'])
    ctx.obj = {
        'eutils': e
    }


def main():
    cli.add_command(search)
    cli.add_command(advance_search)
    cli.add_command(citations_cli)
    cli()


if __name__ == '__main__':
    main()
