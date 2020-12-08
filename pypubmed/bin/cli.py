import os
import sys

import click
import colorama

from ._search import search, advance_search
from ._citations import citations_cli
from pypubmed import version_info, __doc__


PY2 = sys.version_info.major == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


colorama.init()


__epilog__ = click.style('''
contact: {author} <{author_email}>
'''.format(**version_info), fg='bright_black')

@click.group(epilog=__epilog__, help=click.style(__doc__, fg='bright_blue', bold=True))
@click.option('-d', '--debug', help='logging in debug mode', default=False, is_flag=True)
@click.version_option(version=version_info['version'], prog_name='pypubmed')
def cli(debug):
    if debug:
        os.putenv('DEBUG', True)


def main():
    cli.add_command(search)
    cli.add_command(advance_search)
    cli.add_command(citations_cli)
    cli()


if __name__ == '__main__':
    main()
