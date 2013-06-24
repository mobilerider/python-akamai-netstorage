#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os
import sys


init_py = open('netstorage/__init__.py').read()
author = re.search("__author__ = ['\"]([^'\"]+)['\"]", init_py).group(1)
version = re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

setup(
    name='python-akamai-netstorage',
    version=version,
    description="Python client for Akamai's Netstorage API.",
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='akamai,api,netstorage',
    author=author,
    author_email='julio@mobilerider.com',
    url='https://github.com/mobilerider/python-akamai-netstorage',
    license='MIT',
    packages=[
        'netstorage',
    ],
    include_package_data=True,
    install_requires=[
        'lxml',
        'requests',
    ],
    zip_safe=False,
)
