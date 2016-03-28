#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs
from setuptools import setup

__author__ = "Igor R. Dejanović <igor DOT dejanovic AT gmail DOT com>"
__version__ = "0.1-dev"

NAME = 'bibreport'
DESC = 'A tool for making a reports out of bibtex files'
VERSION = __version__
AUTHOR = 'Igor R. Dejanovic'
AUTHOR_EMAIL = 'igor DOT dejanovic AT gmail DOT com'
LICENSE = 'MIT'
URL = 'https://github.com/igordejanovic/bibreport'
DOWNLOAD_URL = 'https://github.com/igordejanovic/bibreport/archive/v%s.tar.gz' % VERSION
README = codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'),
                     'r', encoding='utf-8').read()

setup(
    name = NAME,
    version = VERSION,
    description = DESC,
    long_description = README,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = LICENSE,
    url = URL,
    download_url = DOWNLOAD_URL,
    packages = ["bibreport"],
    install_requires = ["Arpeggio", "jinja2"],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'bibreport = bibreport.console:main'
        ]
    }
)
