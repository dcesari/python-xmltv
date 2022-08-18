#!/usr/bin/env python
from distutils.core import setup

setup(
    name="python-xmltv",
    description="A Python Module for Reading and Writing XMLTV Files",
    version="1.4.3",
    author="James Oakley",
    author_email="jfunk@funktronics.ca",
    url="https://github.com/dcesari/python-xmltv"
    py_modules=['xmltv'],
    long_description=
    """This module provides a simple python API for reading and writing
    XMLTV files. XMLTV is an XML format for storing TV listings.

    More information on XMLTV can be found at http://membled.com/work/apps/xmltv/
    """,
#    long_description=open('README.md').read() + '\n\n' +
#                     open('CHANGELOG.txt').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license="LGPL-3.0+",
)
