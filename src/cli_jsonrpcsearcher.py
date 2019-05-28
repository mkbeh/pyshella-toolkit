# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.scanner import scanner


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
    asyncio.run(scanner(kwargs))


def cli():
    parser = argparse.ArgumentParser(prog='pyshella_scanner', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-mU', '--mongo-uri', required=True, metavar=' ', type=str, help='MongoDB uri.')
    parser.add_argument('-n', '--coin-name', required=True, metavar=' ', type=str, help='Name of cryptocurrency.')
    parser.add_argument('-cT', metavar='SECS', type=float, default=.1, help='Timeout between block cycles.')
    parser.add_argument('-rT', metavar='SECS', type=float, default=.1, help=read_timeout_help)
    parser.add_argument('-hS', metavar='NUM', type=int, default=35, help=hosts_block_size_help)
    parser.add_argument('-pS', metavar='NUM', type=int, default=20, help=ports_block_size_help)

    _run_jsonrpc_searcher(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
