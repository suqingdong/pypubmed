import os
import re
import click
import datetime

from dateutil.parser import parse as date_parse

from pypubmed.core.export import Export

search_examples = click.style('''
examples:

    pypubmed search ngs -l 5 -o ngs.xlsx

    pypubmed search 'NGS[Title] AND Disease[Title/Abstract]' -o ngs_disease.xlsx

    pypubmed search 1,2,3,4

    pypubmed search pmid_list.txt
''', fg='yellow')
@click.command(help=click.style('search with pmid or a term', bold=True, fg='green'), epilog=search_examples, no_args_is_help=True)
@click.option('-c', '--cited', help='get cited information', default=False, is_flag=True)
@click.option('-n', '--no-translate', help='do not translate the abstract', default=False, is_flag=True)
@click.option('-b', '--batch-size', help='the batch size for efetch', default=10, type=int, show_default=True)
@click.option('-min', '--min-factor', help='filter with IF', type=float)
@click.option('-l', '--limit', help='limit the count of output', type=int)
@click.option('-f', '--fields', help='the fields to export')
@click.option('-o', '--outfile', help='the output filename', default='pubmed.xlsx', show_default=True)
@click.argument('term', nargs=1)
@click.pass_obj
def search(obj, **kwargs):
    
    articles = obj['eutils'].search(translate=not kwargs['no_translate'], **kwargs)

    data = []
    for n, article in enumerate(articles, 1):
        obj['eutils'].logger.debug('{}. {}'.format(n, article))

        # filter impact factor
        if kwargs['min_factor'] and (article.impact_factor != '.' and article.impact_factor < kwargs['min_factor']):
            continue

        data.append(article.to_dict())
        if kwargs['limit'] and n >= kwargs['limit']:
            break

    if kwargs['min_factor']:
        obj['eutils'].logger.info('A total of {} articles were found, {} remaining after filtering IF>={}'.format(n, len(data), kwargs['min_factor']))

    Export(data, **kwargs).export()


@click.command(help=click.style('generate advance search string', bold=True, fg='cyan'))
@click.pass_obj
def advance_search(obj, **kwargs):
    fields = obj['eutils'].validate_fields()

    query_box = ''
    while True:
        number = click.prompt('>>> please choose a number of field', type=int, default=48)
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

        if click.confirm('input finish?'):
            break

    click.secho('final query box: {}'.format(query_box), fg='bright_cyan')
    res = obj['eutils'].esearch(query_box, retmax=1, head=True)

    if res['count']:
        details = []
        for each in res['translationstack']:
            if isinstance(each, dict):
                details += ['{term}:{count}'.format(**each)]
        click.secho('count:\t{count}\nquery:\t{querytranslation}\ndetail:\t{detail}'.format(detail=', '.join(details), **res), fg='yellow')

        if click.confirm('search with this query box?'):
            outfile = re.sub(r'[\'"\(\)\[\]/ ]+', '_', query_box).strip('_') + '.xlsx'
            outfile = click.prompt('output filename', default=outfile, show_default=True)
            os.system('pypubmed search "{}" -o {}'.format(query_box, outfile))
    else:
        click.echo(res)
