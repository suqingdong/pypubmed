"""
    Toolkits for NCBI Pubmed
"""
import os
import json

import colorama

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))


colorama.init()
