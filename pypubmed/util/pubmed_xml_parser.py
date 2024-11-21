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


def parse_abstract(AbstractTexts):
    """
        - 1 no AbstractText
        - 2 sigle AbstractText
        - 3 multiple AbstractTexts with Labels
        
        * remove tags
        * repalce entities
        * repalce special chars
    """
    if not AbstractTexts:
        abstract = '.'
    elif len(AbstractTexts) == 1:
        abstract = ''.join(AbstractTexts[0].itertext()) or '.'
    else:
        abstracts = []
        for each in AbstractTexts:
            label = each.attrib.get('Label')
            text = ''.join(each.itertext())
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
    
    if tree.find('PubmedArticle') is None:
        yield None
    else:
        for PubmedArticle in tree.iterfind('PubmedArticle'):
            context = {}
            MedlineCitation = PubmedArticle.find('MedlineCitation')
            Article = MedlineCitation.find('Article')

            context['pmid'] = int(MedlineCitation.findtext('PMID'))

            context['e_issn'] = Article.findtext('Journal/ISSN[@IssnType="Electronic"]')
            context['issn'] = Article.findtext('Journal/ISSN[@IssnType="Print"]') or MedlineCitation.findtext('MedlineJournalInfo/ISSNLinking')

            context['journal'] = Article.findtext('Journal/Title')
            context['iso_abbr'] = Article.findtext('Journal/ISOAbbreviation')

            context['med_abbr'] = MedlineCitation.findtext('MedlineJournalInfo/MedlineTA')

            context['pubdate'] = ' '.join(Article.xpath('Journal/JournalIssue/PubDate/*/text()'))

            pubmed_pubdate = year = ''
            for status in ('pubmed', 'entrez', 'medline'):
                ymd = PubmedArticle.xpath('PubmedData/History/PubMedPubDate[@PubStatus="{}"]/*/text()'.format(status))
                if ymd:
                    pubmed_pubdate = datetime.datetime(*map(int, ymd))
                    year = pubmed_pubdate.year
                    pubmed_pubdate = pubmed_pubdate.strftime('%Y/%m/%d')
                    break

            context['year'] = year
            context['pubmed_pubdate'] = pubmed_pubdate

            context['pagination'] = Article.findtext('Pagination/MedlinePgn')
            context['volume'] = Article.findtext('Journal/JournalIssue/Volume')
            context['issue'] = Article.findtext('Journal/JournalIssue/Issue')
            context['title'] = ''.join(Article.find('ArticleTitle').itertext())
            context['keywords'] = MedlineCitation.xpath('KeywordList/Keyword/text()')
            context['pub_status'] = PubmedArticle.findtext('PubmedData/PublicationStatus')

            context['abstract'] = parse_abstract(Article.xpath('Abstract/AbstractText'))
            
            author_mail = []

            author_list = []
            affiliation_author_map = defaultdict(list)
            for author in Article.xpath('AuthorList/Author'):

                last_name = author.findtext('LastName')
                fore_name = author.findtext('ForeName')
                # Initials = author.findtext('Initials')

                author_name = ' '.join(name for name in [fore_name, last_name] if name)
        
                author_list.append(author_name)

                for aff in author.xpath('AffiliationInfo/Affiliation/text()'):
                    affiliation_author_map[aff].append(author_name)

                affiliation_info = '\n'.join(author.xpath('AffiliationInfo/Affiliation/text()'))
                mail = re.findall(r'([^\s]+?@.+)\.', str(affiliation_info))
                if mail:
                    mail = '{}: {}'.format(author_name, mail[0])
                    author_mail.append(mail)

            context['author_mail'] = '\n'.join(author_mail) or '.'
            authors = Article.xpath('AuthorList/Author/AffiliationInfo/Affiliation/text()')
            context['author_first'] = context['author_last'] = '.'
            if authors:
                context['author_first'] = authors[0]
                if len(authors) > 1:
                    context['author_last'] = authors[-1]

            context['authors'] = '\n'.join(author_list)

            # affiliation list
            affiliations = Article.xpath('AuthorList/Author/AffiliationInfo/Affiliation/text()')

            affiliation_unique_list = []
            for aff in affiliations:
                if aff not in affiliation_unique_list:
                    affiliation_unique_list.append(aff)

            context['affiliations'] = '\n'.join((
                f'{n}. {aff} - {affiliation_author_map.get(aff)}' 
                for n, aff in enumerate(affiliation_unique_list, 1)
            ))

            context['pub_types'] = Article.xpath('PublicationTypeList/PublicationType/text()')
            context['doi'] = PubmedArticle.findtext('PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')
            context['pmc'] = PubmedArticle.findtext('PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]')

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
