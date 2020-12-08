"""
NCBI Citations:
    - https://pubmed.ncbi.nlm.nih.gov/help/#cite
    - Is this limited? IP blocking with too much requests?
    - https://pubmed.ncbi.nlm.nih.gov/{PMID}/citations/

Related Website:
    - https://www.pmid2cite.com/
    - https://www.plagiarism.org/article/citation-styles
    - https://ozzz.org/citation-generator/

Format:
    - AMA: American Medical Association 
    - MLA: Modern Language Association
    - APA: American Psychological Association
    - NLM: National Library of Medicine
"""
import os
import re
import json

import click
from webrequests import WebRequest



def ncbi_citations(pmid, fmt=None):
    url = 'https://pubmed.ncbi.nlm.nih.gov/{}/citations/'.format(pmid)
    data = WebRequest.get_response(url).json()
    if fmt in data:
        return data[fmt]
    return data


def manual_citations(article, fmt='ama'):

    doi = ' doi:{}'.format(article.doi) if article.doi else ''
    issue = '({})'.format(article.issue) if article.issue else ''

    # ========================================
    # # merge the pagination?
    # # - S1-22; quiz S23-4  =>  S1-S24
    # # - 548-554            =>  548-54
    # ========================================
    # pagination_merge = article.pagination

    if fmt == 'ama':
        citation = '{authors}. {title} {med_abbr}. {year};{volume}{issue}:{pagination}.{doi}'
        if len(article.authors) > 5:
            authors = ', '.join('{} {}'.format(author[0], author[2]) for author in article.authors[:3]) + ' et al'
        else:
            authors = ', '.join('{} {}'.format(author[0], author[2]) for author in article.authors)
    elif fmt == 'mla':
        first_author = '{}, {}'.format(*article.authors[0][:2])
        issue = ',{}'.format(article.issue) if article.issue else ''
        citation = '{first_author} et al. \u201c{title}\u201d {journal} vol. {volume}{issue} ({year}): {pagination}.{doi}'
    elif fmt == 'apa':
        doi = ' https://doi.org/{}'.format(article.doi) if article.doi else ''
        author_all = ', '.join('{}, {}.'.format(each[0], '. '.join(each[2])) for each in article.authors[:-1])
        last_author = article.authors[-1]
        if len(last_author) == 1:
            last_author = last_author[0]
        else:
            last_author = '{}, {}.'.format(last_author[0], '. '.join(last_author[2]))
        citation = '{author_all}, & {last_author} ({year}). {title} {journal}, {volume}{issue}, {pagination}.{doi}'
    elif fmt == 'nlm':
        author_list = ', '.join('{} {}'.format(each[0], each[2]) if len(each) >= 3 else ';{}'.format(each[0]) for each in article.authors)
        doi = doi + '. ' if doi else ' '
        citation = '{author_list}. {title} {med_abbr}. {pubdate};{volume}{issue}:{pagination}.{doi}PMID:{pmid}'
        if article.pmc:
            citation += '; PMCID: {pmc}.'

    citation = citation.format(**dict(article.to_dict(), **locals()))

    return citation

