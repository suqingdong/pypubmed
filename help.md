# **NCBI EUtils**
> https://www.ncbi.nlm.nih.gov/books/NBK25497/

## `einfo`
> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=pubmed

## `esearch`
> https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
>> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=ngs[title]&retmax=5&retstart=0
>> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=ngs&retmax=5&retstart=0&field=title

## `efetch`
> https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
>> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=17284678,9997&retmode=xml


## `elink`
> https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink
> - get cited (`{"linkname": "pubmed_pubmed_citedin"}`)
>> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor_score&retmode=json
> - get pdf url
>> https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&cmd=prlinks&id=10210801



### `retmode` and `rettype`
> https://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly

### `API KEY`
> - E-utils users are allowed 3 requests/second without an API key.
> - Create an API key to increase your e-utils limit to 10 requests/second.
> - use with `api_key=API_KEY `


---
# **Journals**
> https://www.ncbi.nlm.nih.gov/nlmcatalog/journals
> - https://ftp.ncbi.nlm.nih.gov/pubmed/J_Entrez.gz
> - https://ftp.ncbi.nlm.nih.gov/pubmed/J_Medline.gz

---
# **Impact Factor**
> http://www.greensci.net/


- https://dataguide.nlm.nih.gov/eutilities/utilities.html
- https://www.nlm.nih.gov/bsd/licensee/elements_article_source.html
- https://www.nlm.nih.gov/bsd/licensee/elements_alphabetical.html
