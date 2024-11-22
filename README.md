# NCBI Pubmed Toolkits

## Requirements
- Python3.6+

## Installation
```bash
python3 -m pip install -U pypubmed
```

## Usage
### `search`
> search Pubmed with term
```bash
pypubmed search --help

########## search pubmed ##########
pypubmed search ngs -l 5 -o ngs.xlsx
pypubmed search 'NGS[Title] AND Disease[Title/Abstract]' -o ngs_disease.xlsx
pypubmed search 1,2,3,4
pypubmed search pmid_list.txt

########## search pmc ##########
# parse pmc xml, maybe network error
pypubmed -d pmc search PMC10914497,PMC11572642
pypubmed -d pmc search pmcid_list.txt
pypubmed -d pmc search '(single cell) OR (scrna) OR (scRNA seq)'

# convert pmcid to pmid, then parse pubmed xml, some pmcid may not have pmid
pypubmed -d pmc search '(single cell) OR (scrna) OR (scRNA seq)' --convert-pmc

# do not translate
pypubmed search -l 5 ngs

# translate with a local proxies
pypubmed -p http://127.0.0.1:1081 search ngs -l 5
```

### `advance-search`
> advance search builder
```bash
pypubmed advance-search --help
```
![](https://suqingdong.github.io/pypubmed/src/advance-search.png)

### `citations`
> generate citations for given PMID
```bash
pypubmed citations --help
```

## Todos
- [ ] HTML output
- [ ] PDF downloader
- [ ] GUI application
- [ ] Local paper manager

## Documents
> https://pypubmed.readthedocs.io/en/latest/

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=suqingdong/pypubmed&type=Date)](https://star-history.com/#suqingdong/pypubmed&Date)
