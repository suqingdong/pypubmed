# -*- coding=utf-8 -*-
import os
import re
import datetime
from collections import defaultdict

try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.cElementTree as ET

from w3lib import html


SPECIAL_CHARS = {
    u'\u2009': ' ',
    u'\u202f': ' ',
    u'\u2217': '*',
}


def parse_abstract(abstracts):
    """
        - 1 no AbstractText
        - 2 sigle AbstractText
        - 3 multiple abstracts with Labels
        
        * remove tags
        * repalce entities
        * repalce special chars
    """
    if not abstracts:
        abstract = '.'
    elif len(abstracts) == 1:
        abstract = ''.join(abstracts[0].itertext()) or '.'
        abstract = abstract.replace('\n', ' ')
    else:
        for item in abstracts:
            if item.find('sec') is not None:
                real_abstract = item
                break
    
        abstracts = []
        for part in real_abstract.findall('sec'):
            label = part.findtext('title')
            text = ''.join(part.itertext())
            if label:
                abstracts.append('{}: {}'.format(label, text))
            else:
                abstracts.append(text)
        abstract = '\n'.join(abstracts)

    # ===========
    # remove tags
    # ===========
    abstract = html.remove_tags(abstract)

    # ===============
    # repalce entities
    # ===============
    n = 0
    while re.search(r'&.{1,7};', abstract):
        abstract = html.replace_entities(abstract)
        n += 1
        if n > 4:
            print('entities levels > 5')
            print(re.findall(r'&.{1,7};', abstract))
            break

    # =====================
    # replace special chars
    # =====================
    for special, replace in SPECIAL_CHARS.items():
        abstract = abstract.replace(special, replace)

    return abstract


def parse(xml):

    if os.path.isfile(xml):
        tree = ET.parse(xml)
    else:
        tree = ET.fromstring(xml)
    
    if tree.find('article') is None:
        yield None
    else:
        for article in tree.iterfind('article'):
            context = {}

            front = article.find('front')
            article_meta = front.find('article-meta')

            issn = front.find('journal-meta/issn')
            context['e_issn'] = issn.text
            context['issn'] = issn.text
            context['title'] = article_meta.findtext('title-group/article-title').replace('\n', ' ')

            context['journal'] = front.findtext('journal-meta/journal-title-group/journal-title')
            context['iso_abbr'] = front.findtext('journal-meta/journal-id[@journal-id-type="iso-abbrev"]')
            context['med_abbr'] = front.findtext('journal-meta/journal-id[@journal-id-type="nlm-ta"]')

            pubdate = front.find('article-meta/pub-date[@pub-type="epub"]')
            year = pubdate.findtext('year')
            month = pubdate.findtext('month')
            day = pubdate.findtext('day')

            context['year'] = year
            context['pubdate'] = datetime.datetime(int(year), int(month), int(day)).strftime('%Y/%m/%d')
            context['pubmed_pubdate'] = context['pubdate']

            context['pagination'] = article_meta.findtext('elocation-id')
            context['volume'] = article_meta.findtext('volume')
            context['issue'] = article_meta.findtext('issue')

            context['keywords'] = article_meta.xpath('kwd-group/kwd/text()')
            context['pub_status'] = issn.attrib.get('pub-type')

            context['abstract'] = parse_abstract(article_meta.findall('abstract'))

            context['pub_types'] = []  # do not know which field to use

            context['pmc'] = 'PMC' + article_meta.findtext('article-id[@pub-id-type="pmc"]')
            context['doi'] = article_meta.findtext('article-id[@pub-id-type="doi"]')

            # author emails
            cor_email_map = {}
            cor_list = article_meta.findall('author-notes/corresp')
            for cor in cor_list:
                cor_id = cor.attrib['id']
                email = cor.findtext('email')
                cor_email_map[cor_id] = email

            # authors
            author_list = []
            author_mail = []
            aff_author_map = defaultdict(list)
            for author in article_meta.findall('contrib-group/contrib[@contrib-type="author"]'):
                last_name = author.findtext('name/surname')
                fore_name = author.findtext('name/given-names')
                author_name = ' '.join(name for name in [fore_name, last_name] if name)
                author_list.append(author_name)

                for aff in author.findall('xref[@ref-type="aff"]'):
                    aff_id = aff.attrib['rid']
                    aff_author_map[aff_id].append(author_name)

                for cor in author.findall('xref[@ref-type="other"]'):
                    cor_id = cor.attrib['rid']
                    email = cor_email_map.get(cor_id)
                    if email:
                        mail = '{}: {}'.format(author_name, email)
                        author_mail.append(mail)

            context['authors'] = '\n'.join(author_list)
            context['author_mail'] = '\n'.join(author_mail) or '.'

            context['author_first'] = context['author_last'] = '.'
            if authors:
                context['author_first'] = authors[0]
                if len(authors) > 1:
                    context['author_last'] = authors[-1]

            # affiliations
            aff_list = []
            for n, aff in enumerate(article_meta.findall('contrib-group/aff'), 1):
                aff_text = ''.join(aff.itertext()).replace('\n', ' ')[1:]
                aff_authors = aff_author_map.get(aff.attrib['id'])
                aff_list.append(f'{n}. {aff_text} - {aff_authors}')
            context['affiliations'] = '\n'.join(aff_list)

            yield context


if __name__ == '__main__':
    import json
    from webrequests import WebRequest
    
    pmid = '17284678,9997'
    pmid = '28143587'
    pmid = '33577981'
    
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml'
    resp = WebRequest.get_response(url)
    for context in parse(resp.text):
        print(json.dumps(context, indent=2))
