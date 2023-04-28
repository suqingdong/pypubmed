# NCBI Pubmed Toolkits

## Requirements
- Python3.6+

## Installation
```bash
pip3 isntall -U pypubmed
```

## Usage
### `search`
> search Pubmed with term
```bash
pypubmed search --help

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
