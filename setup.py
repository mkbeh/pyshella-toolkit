# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='pyshella-toolkit',
    version='0.56.33',
    description='Hacking toolkit for BTC/forks peers.',
    author='mkbeh',
    license='MIT',
    platforms='linux',
    install_requires=[
        'aiobitcoin==0.72.3',
        'uvloop==0.12.2',
        'aiofiles==0.4.0',
        'pymongo==3.8.0',
        'motor==2.0.0',
        'loguru==0.2.5',
        'scrapy==1.6.0'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyshella-peers-scanner = src.cli_peersscanner:cli',
            'pyshella-jsonrpc-searcher = src.cli_jsonrpcsearcher:cli',
            'pyshella-jsonrpc-bruter = src.cli_jsonrpcbruter:cli',
            'pyshella-coins-withdrawal = src.cli_coinswithdrawal:cli'
        ],
    },
)
