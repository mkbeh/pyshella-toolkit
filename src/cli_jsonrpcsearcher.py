# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.jsonrpcsearcher import JSONRPCSearcher


default_mongo_uri = 'mongodb://root:toor@localhost:27017'
cli_desc = 'Scanner which discovers JSON-RPC from Bitcoin/forks peers.'
read_timeout_help = 'Time to wait for a response from the server after sending the request.'
hosts_block_size_help = 'The number of hosts that will be processed simultaneously.'
ports_block_size_help = 'The number of ports that will be processed simultaneously for each host.'
epilog = """
Usage example: ..............

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_jsonrpc_searcher(**kwargs):
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(JSONRPCSearcher(**kwargs).run_jsonrpc_searcher())


def cli():
    parser = argparse.ArgumentParser(prog='pyshella_scanner', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-mU', '--mongo-uri', metavar=' ', type=str, default=default_mongo_uri, help='MongoDB URI.')
    parser.add_argument('-n', '--coin-name', required=True, metavar=' ', type=str, help='Name of cryptocurrency.')
    parser.add_argument('-cT', metavar='SECS', type=float, default=.1, help='Timeout between hosts block cycles.')
    parser.add_argument('-rT', metavar='SECS', type=float, default=.1, help=read_timeout_help)
    parser.add_argument('-bT', metavar='SECS', type=float, default=5*60, help='Delay between block cycles.')
    parser.add_argument('-hS', metavar='NUM', type=int, default=35, help=hosts_block_size_help)
    parser.add_argument('-pS', metavar='NUM', type=int, default=20, help=ports_block_size_help)

    _run_jsonrpc_searcher(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
