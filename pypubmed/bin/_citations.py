import os
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

@click.command(name='citations',
               epilog=__epilog__,
               short_help='generate citations for given pmids',
               help='Citations Tools')
@click.option('-m', '--manual', help='cite with manual citations, default with ncbi citations', default=False, is_flag=True)
@click.option('-f', '--fmt', help='the format of citation', type=click.Choice('ama mla apa nlm'.split()), default='ama')
@click.option('-k', '--api-key', help='the API_KEY of NCIB', envvar='NCBI_API_KEY')
@click.argument('pmids', nargs=-1)
def citations_cli(pmids, manual, fmt, api_key):
    if not pmids:
        click.secho('please supply pmids or a file', fg='green')
        exit(1)

    if os.path.isfile(pmids[0]):
        pmid_list = open(pmids[0]).read().strip().split()
    else:
        pmid_list = pmids
    
    if manual:
        e = Eutils(api_key=api_key)
        articles = e.efetch(pmid_list)
        for article in articles:
            citation = manual_citations(article, fmt=fmt)
            click.secho(citation, fg='yellow')
    else:
        for pmid in pmid_list:
            citation = ncbi_citations(pmid, fmt=fmt)
            click.secho(json.dumps(citation, indent=2), fg='green')
    

if __name__ == '__main__':
    citations()
