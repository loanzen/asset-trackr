#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    "requests",
    "arrow",
    "attrdict"
]

setup(
    name='asset_trackr',
    version='0.1.0',
    description="",
    long_description='',
    author="Kshitij Mittal",
    author_email='kshitij@loanzen.in',
    url='https://github.com/loanzen/asset-trackr',
    packages=[
        'asset_trackr',
    ],
    package_dir={'asset_trackr':
                 'asset_trackr'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
