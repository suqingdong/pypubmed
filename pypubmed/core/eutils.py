"""
    https://www.ncbi.nlm.nih.gov/books/NBK25497/
"""
import os
import sys
import json
import time
import textwrap
import datetime

import click
import prettytable

from dateutil.parser import parse as date_parse

from impact_factor import ImpactFactor
from simple_googletrans import GoogleTrans
from simple_loggers import SimpleLogger
from webrequests import WebRequest


from pypubmed.util import xml_parser
from pypubmed.core.article import Article


class Eutils(object):
    """
        params:
            db          database name
            api_key     api_key or NCBI_API_KEY in environment

        optional params:
            term        term for esearch
            id          id(s) for efetch
            field       field for esearch
    """
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    logger = SimpleLogger('Eutils')
    IF = ImpactFactor()

    def __init__(self, db='pubmed', service_url='translate.google.cn', api_key=None, **kwargs):
        self.db = db
        self.api_key = api_key
        self.validate_api_key()
        self.TR = GoogleTrans(service_url=service_url)

    def parse_params(self, **kwargs):
        """
            - add default db
            - add api_key if available
        """
        params = {'db': self.db}
        if self.api_key:
            params['api_key'] = self.api_key
        params.update(kwargs)
        
        if 'api_key' in params and params['api_key'] is None:
            del params['api_key']

        return params

    def esearch(self, term, retstart=0, retmax=250, head=False, limit=None, **kwargs):
        """
            https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

            > -search from a database from given term
            >> - esearch.cgi?db=pubmed&term=ngs
            >> - esearch.cgi?db=pubmed&term=ngs&retmode=xml&field=TIAB
            >> - esearch.cgi?db=pubmed&term=ngs[Title/Abstract]&retmode=xml
        """
        url = self.base_url + 'esearch.fcgi'
        params = self.parse_params(term=term, retmode='json', retstart=retstart, retmax=retmax, **kwargs)
        result = WebRequest.get_response(url, params=params).json()['esearchresult']

        if head:
            return result

        self.logger.info('{count} articles found with term: {querytranslation}'.format(**result))
        idlist = result['idlist']

        while int(result['retstart']) + int(result['retmax']) < int(result['count']):
            if limit and int(result['retstart']) + int(result['retmax']) > limit:
                break
            retstart = int(result['retstart']) + int(result['retmax'])
            params = self.parse_params(term=term, retmode='json', retstart=retstart, retmax=retmax, **kwargs)
            result = WebRequest.get_response(url, params=params).json()['esearchresult']
            idlist += result['idlist']

        if idlist:
            self.logger.info('idlist: {} ...'.format(', '.join(idlist[:10])))
        else:
            self.logger.warning('no result for term: {}'.format(term))
        return idlist

    def efetch(self, ids, batch_size=5, show_process=False, **kwargs):
        """
            https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch

            > - fetch from a database for given ids
            >> efetch.cgi?db=pubmed&id=1,2,3
        """
        url = self.base_url + 'efetch.fcgi'

        self.logger.info('fetching start: total {}, batch_size: {}'.format(len(ids), batch_size))

        with click.progressbar(length=len(ids), show_percent=True, empty_char=' ', fill_char='>') as pbar:
            for n in range(0, len(ids), batch_size):
                _id = ','.join(ids[n:n+batch_size])
                if show_process:
                    end =  n + batch_size if n + batch_size <= len(ids) else len(ids)
                    pbar.label = 'Fetching {}-{}'.format(n+1, end)
                    pbar.update(batch_size)
                n += batch_size

                params = self.parse_params(id=_id, retmode='xml')

                xml = WebRequest.get_response(url, params=params).text
                
                for context in xml_parser.parse(xml):
                    article = Article(**context)
                    yield article

    def einfo(self, **kwargs):
        """
            https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EInfo

            > - show all database list
            >> einfo.fcgi?db=
            > - show dbinfo for given database
            >> einfo.fcgi?db=pubmed
        """
        url = self.base_url + 'einfo.fcgi'
        params = self.parse_params(retmode='json', **kwargs)
        info = WebRequest.get_response(url, params=params, allowed_codes=[200, 400]).json()
        return info

    def elink(self, ids, dbfrom='pubmed', cmd='neighbor', **kwargs):
        """
            https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink

            > - get cited (`{"linkname": "pubmed_pubmed_citedin"}`)
            >> elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor&retmode=json
            > - get pdf url
            >> elink.fcgi?dbfrom=pubmed&db=pubmed&cmd=prlinks&id=10210801

            cmds:
                - neighbor (default)
                - neighbor_score
                - neighbor_history
                - acheck
                - ncheck
                - lcheck
                - llinks
                - llinkslib
                - prlinks
        """
        url = self.base_url + 'elink.fcgi'
        params = self.parse_params(retmode='json', id=ids, dbfrom=dbfrom, cmd=cmd,  **kwargs)
        result = WebRequest.get_response(url, params=params).json()
        return result

    def get_cited(self, _id, dbfrom='pubmed', cmd='neighbor'):
        """
            get the cited pmids for given pmid
        """
        linksetdbs = self.elink(_id, dbfrom=dbfrom, cmd=cmd)['linksets'][0]['linksetdbs']
        links = [
            linkset['links'] for linkset in linksetdbs
            if linkset['linkname'] == 'pubmed_pubmed_citedin'
        ]
        
        citedin = links[0] if links else []
        return {'count': len(citedin), 'links': citedin}

    def get_pdf_url(self, _id, dbfrom='pubmed', cmd='prlinks'):
        """
            get the pdf url for given pmid
        """
        idurllist = self.elink(_id, dbfrom=dbfrom, cmd=cmd)['linksets'][0]['idurllist']
 
        result = {each['id']: each['objurls'][0]['url']['value'] for each in idurllist}

        return result

    def validate_fields(self, **kwargs):
        """
            Show all fields for given database
        """
        fieldlist = self.einfo(**kwargs)['einforesult']['dbinfo'][0]['fieldlist']

        fieldlist = sorted(fieldlist, key=lambda x: x.get('fullname'))

        fields = {}
        table = prettytable.PrettyTable(field_names=['Number', 'Name', 'FullName', 'Description'])
        for n, each in enumerate(fieldlist, 1):
            # print('{n}\t{name}\t{fullname}\t{description}'.format(n=n, **each))
            fields[n] = [each['name'], each['fullname'], each['description']]
            table.add_row([n, each['name'], each['fullname'], each['description']])

        table.align['FullName'] = 'l'
        table.align['Description'] = 'l'
        click.secho(str(table), fg='bright_blue')

        return fields

    def validate_api_key(self):
        """
            Description: https://www.ncbi.nlm.nih.gov/account/settings/#accountSettingsApiKeyManagement
                - E-utils users are allowed 3 requests/second without an API key.
                - Create an API key to increase your e-utils limit to 10 requests/second.
        """
        configfile = os.path.join(os.path.expanduser('~'), '.pypubmed.cfg')

        if not self.api_key:
            if os.path.isfile(configfile):
                self.api_key = open(configfile).read().strip()
            if not self.api_key:
                msg = textwrap.dedent('''
                    API_KEY not found! Use eutils with a api_key is a good idea!
                    You can create one from: https://www.ncbi.nlm.nih.gov/account/settings/#accountSettingsApiKeyManagement
                    If you already have one, you can add it to your environment: export NCBI_API_KEY=xxxx''')
                self.logger.warning(msg)
                return

        res = self.einfo()
        if 'error' in res:
            self.logger.warning('invalid api_key, please check: {}'.format(self.api_key))
            self.api_key = None
        else:
            self.logger.info('Valid api_key: {}'.format(self.api_key))
            with open(configfile, 'w') as out:
                out.write(self.api_key)

    def search(self, term, cited=True, translate=True, impact_factor=True, limit=None, **kwargs):
        """
            term:
                - string, eg. 'ngs AND disease'
                - pmid, eg. 1,2,3
                - file with pmid
        """
        if os.path.isfile(term):
            idlist = open(term).read().strip().split()
        elif all(each.isdigit() for each in term.split(',')):
            idlist = term.split(',')
        else:
            idlist = self.esearch(term, limit=limit)

        # print(kwargs);exit()

        articles = self.efetch(idlist, **kwargs)
        for article in articles:
            if impact_factor:
                res = self.IF.search(article.issn) or self.IF.search(article.e_issn)
                article.impact_factor = res['factor'] if res else '.'

            if cited:
                article.cited = self.get_cited(article.pmid)
                
            if translate:
                article.abstract_cn = 'translate failed'
                n = 0
                while n < 5:
                    n += 1
                    try:
                        article.abstract_cn = self.TR.translate(article.abstract)
                        break
                    except Exception as e:
                        print(e)
                        time.sleep(3)
            yield article
