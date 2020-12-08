"""====================\n
NCBI Pubmed ToolKits\n
====================
"""
import os
import json



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

version_file = os.path.join(BASE_DIR, 'version', 'version.json')
with open(version_file) as f:
    version_info = json.load(f)





if __name__ == '__main__':
    print(version_info)
