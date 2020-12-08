# -*- encoding: utf8 -*-
import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


setup(
    name='pypubmed',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    description='View/Highlight KEGG Pathway',
    long_description=open(os.path.join(BASE_DIR, 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/kegg_viewer',
    license='BSD License',
    install_requires=open(os.path.join(BASE_DIR, 'requirements.txt')).read().split(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'kegg_viewer = kegg_viewer.bin.main:main',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ]
)
