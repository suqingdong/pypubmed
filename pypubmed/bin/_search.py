import click
import datetime

from dateutil.parser import parse as date_parse

from pypubmed.core.eutils import Eutils
from pypubmed.core.export import Export


@click.command(short_help='search with pmid or a term', help='Search Tools')
@click.option('-k', '--api-key', help='the api_key of NCBI Pubmed, NCBI_API_KEY environment is available', envvar='NCBI_API_KEY')
@click.option('-c', '--cited', help='get cited information', default=False, is_flag=True)
@click.option('-n', '--no-translate', help='do not translate the abstract', default=False, is_flag=True)
@click.option('-p', '--show-process', help='show processing', default=False, is_flag=True)
@click.option('-b', '--batch-size', help='the batch size for efetch', default=10, type=int, show_default=True)
@click.option('-min', '--min-factor', help='filter with IF', type=float)
@click.option('-l', '--limit', help='limit the count of output', type=int)
@click.option('-f', '--fields', help='the fields to export')
@click.option('-o', '--output', help='the output filename', default='out.xlsx')
@click.argument('term', nargs=1)
def search(**kwargs):
    e = Eutils(api_key=kwargs['api_key'])
    articles = e.search(translate=not kwargs['no_translate'], **kwargs)

    data = []
    for n, article in enumerate(articles, 1):
        data.append(article.to_dict())
        if kwargs['limit'] and n >= kwargs['limit']:
            break
    # data = [article.to_dict() for article in articles]
    Export(data, **kwargs).export()


@click.command(short_help='generate advance search string', help='Search Advance')
@click.option('-k', '--api-key', help='the api_key of NCBI Pubmed, NCBI_API_KEY environment is available', envvar='NCBI_API_KEY')
def advance_search(**kwargs):
    e = Eutils(api_key=kwargs['api_key'])
    fields = e.validate_fields()

    query_box = ''
    while True:
        number = click.prompt('>>> please choose a number of field', type=int, default=2)
        field = fields[number][1]
        click.secho('your choice is: {number} - {field}'.format(**locals()), fg='cyan')

        if field.startswith('Date - '):
            start = click.prompt('>>> please enter the start date(YYYY-MM-DD)', value_proc=date_parse).strftime('%Y/%m/%d')
            end = click.prompt('>>> please enter the end date', default='3000', value_proc=date_parse)
            if end != '3000':
                end = end.strftime('%Y/%m/%d')
            term = '("{start}"[{field}] : "{end}"[{field}])'.format(**locals())
        else:
            term = click.prompt('>>> please enter a search term')
            if field == 'All Fields':
                term = '{term}'.format(**locals())
            else:
                term = '"{term}"[{field}]'.format(**locals())

        if not query_box:
            query_box = term
        else:
            logic = click.prompt('>>> please input the logic', type=click.Choice(['and', 'or', 'not']), default='and').upper()
            query_box = '({query_box}) {logic} ({term})'.format(**locals())

        click.secho('query box now: ' + query_box, fg='bright_green')

        finish = click.prompt('input finish?', type=click.Choice('yn'), default='n')
        if finish == 'y':
            break

    click.secho('final query box: {}'.format(query_box), fg='bright_cyan')
    res = e.esearch(query_box, retmax=1, head=True)
    click.secho('{count} articles found with this query box.'.format(**res), fg='yellow')
