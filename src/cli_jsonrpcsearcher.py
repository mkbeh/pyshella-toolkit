# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from loguru import logger

from src.extra import utils
from src.toolkit.jsonrpcsearcher import JSONRPCSearcher


default_mongo_uri = 'mongodb://root:toor@localhost:27017'
cli_desc = 'Scanner which discovers Bitcoin/forks JSON-RPC on peers.'
mongo_uri_help = f'MongoDB URI. Default: {default_mongo_uri}'
read_timeout_help = 'Time to wait for a response from the server after sending the request.'
hosts_block_size_help = 'The number of hosts that will be processed simultaneously.'
ports_block_size_help = 'The number of ports that will be processed simultaneously for each host.'
verbose_help = 'Activate verbose mode. Will show all found headers.'
epilog = """
-----------------------------------------------------
Usage example: pyshella-jsonrpc-searcher -n Bitcoin -bT 1 -hS 1 -pS 200 -v True

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


utils.setup_logger('toolkit.log')
logger_exc = logger.bind(util='cli-exception')


def _run_jsonrpc_searcher(**kwargs):
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(JSONRPCSearcher(**kwargs).run_jsonrpc_searcher())


@logger_exc.catch()
def cli():
    parser = argparse.ArgumentParser(prog='pyshella-jsonrpc-searcher', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--coin-name', metavar='NAME', required=True, type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', metavar='URI', type=str, default=default_mongo_uri, help=mongo_uri_help)
    parser.add_argument('-cT', metavar='SECS', type=float, default=.1, help='Timeout between hosts block cycles.')
    parser.add_argument('-rT', metavar='SECS', type=float, default=.1, help=read_timeout_help)
    parser.add_argument('-bT', metavar='SECS', type=float, default=5*60, help='Delay between block cycles.')
    parser.add_argument('-hS', metavar='NUM', type=int, default=35, help=hosts_block_size_help)
    parser.add_argument('-pS', metavar='NUM', type=int, default=20, help=ports_block_size_help)
    parser.add_argument('-v', metavar='BOOL', default=False, type=bool, help=verbose_help)

    _run_jsonrpc_searcher(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
