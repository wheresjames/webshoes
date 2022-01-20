#!/usr/bin/python3

import os
from setuptools import setup

def readConfig(fname):
    cfg = {}
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().replace("\t", " ").split(" ")
            k = parts.pop(0).strip()
            cfg[k] = " ".join(parts).strip()
    return cfg

here = os.path.abspath(os.path.dirname(__file__))

# Read in the config
cfg = readConfig(os.path.join(here, 'webshoes', 'PROJECT.txt'))

# Read in the README
long_description = cfg['description']
rmf = os.path.join(here, 'README.md')
if os.path.exists(rmf):
    with open(rmf, encoding='utf-8') as f:
        long_description = f.read()

setup(
    name=cfg['name'],
    version=cfg['version'],
    description=cfg['description'],
    url=cfg['url'],
    author=cfg['author'],
    author_email=cfg['email'],
    license=cfg['license'],
    packages=[cfg['name']],
    include_package_data = True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
            'aiohttp',
            'threadmsg>=0.2.0',
            'propertybag',
            'sparen'
        ],
    dependency_links=[
        ]
)
