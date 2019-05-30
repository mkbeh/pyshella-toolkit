# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='pyshella-toolkit',
    version='0.45.17',
    description='BTC/fork hack toolkit.',
    author='mkbeh',
    license='MIT',
    platforms='any',
    install_requires=[
        'aiobitcoin',
        'uvloop',
        'aiofiles',
        'pymongo',
        'motor',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyshella-peers-scanner = src.cli_peersscanner:cli',
            'pyshella-jsonrpc-searcher = src.cli_jsonrpcsearcher:cli',
            'pyshella-cw = src.cli_cw:test'
        ],
    },
)
