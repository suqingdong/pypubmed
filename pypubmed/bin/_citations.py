import os
import sys
import json

import click

from pypubmed.core.eutils import Eutils
from pypubmed.core.citations import ncbi_citations, manual_citations


__epilog__ = '''
examples:\n
    citations 1 2 3\n
    citations 1 2 3 -f nlm\n
    citations 1 2 3 -m -f apa\n
'''

@click.command(name='citations', epilog=__epilog__, help=click.style('generate citations for given pmids', bold=True, fg='magenta'), no_args_is_help=True)
@click.option('-m', '--manual', help='cite with manual citations, default with ncbi citations', default=False, is_flag=True)
@click.option('-f', '--fmt', help='the format of citation', type=click.Choice('ama mla apa nlm'.split()), default='ama')
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.argument('pmids', nargs=-1)
@click.pass_obj
def citations_cli(obj, **kwargs):
    pmids = kwargs['pmids']
    if not pmids:
        click.secho('please supply pmids or a file', fg='green')
        exit(1)

    if os.path.isfile(pmids[0]):
        pmid_list = open(pmids[0]).read().strip().split()
    else:
        pmid_list = pmids
    
    out = open(kwargs['outfile'], 'w') if kwargs['outfile'] else sys.stdout
    with out:
        if kwargs['manual']:
            e = Eutils(api_key=obj['api_key'])
            articles = e.efetch(pmid_list)

            click.echo('\n', err=True)

            for article in articles:
                citation = manual_citations(article, fmt=kwargs['fmt'])
                out.write('{}\t{}\n'.format(article.pmid, citation))
        else:
            for pmid in pmid_list:
                citation = ncbi_citations(pmid, fmt=kwargs['fmt'])['orig']
                out.write('{}\t{}\n'.format(pmid, citation))
