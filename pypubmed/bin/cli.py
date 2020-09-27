import os
import sys
import click


from pypubmed.core.search import search, advance_search
from pypubmed.core.citations import citations
from pypubmed import __version__, __author__, __author_email__, __doc__


PY3 = sys.version_info.major == 3
if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf-8')



__epilog__ = click.style('''
contact: {__author__} <{__author_email__}>
'''.format(**locals()), fg='bright_black')

@click.group(epilog=__epilog__, help=click.style(__doc__, fg='bright_blue', bold=True))
@click.option('-d', '--debug', help='logging in debug mode', default=False, is_flag=True)
@click.version_option(version=__version__, prog_name='pypubmed')
def cli(debug):
    if debug:
        os.putenv('DEBUG', True)


def main():
    cli.add_command(search)
    cli.add_command(advance_search)
    cli.add_command(citations)
    cli()


if __name__ == '__main__':
    main()
