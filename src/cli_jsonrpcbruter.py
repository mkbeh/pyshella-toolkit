# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.extra import utils
from src.toolkit.jsonrpcbruter import JSONRPCBruter


default_mongo_uri = 'mongodb://root:toor@localhost:27017'

cli_desc = 'Bitcoin/fork JSON-RPC bruter.'
mongo_uri = f'MongoDB URI. Default: {default_mongo_uri}'
logins = 'Single login or file with logins.'
passwords = 'Single password or file with passwords.'
brute_order = """
The order in which the brute force process will occur. Where H - hosts,
L - logins, P - passwords. Default: HLP. Examples: HLP, LPH, PHL, etc. 
"""
threads = 'The number of coroutines that will be asynchronous in bruteforce process. Default: 1 thread.'
read_timeout_help = 'Time to wait for a response from the server after sending the request. Default: 100ms.'
cycle_timeout_help = 'Timeout between getting new data for brute. Default: 30 seconds.'
epilog = """
----------------------------------------------------------------------------------------------
Usage example: pyshella-jsonrpc-bruter -n Bitcoin -t 20 -l <logins_file> -p <pwds_file> -b HLP

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


utils.setup_logger('toolkit.log')


def _run_jsonrpc_bruter(**kwargs):
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(JSONRPCBruter(**kwargs).run_bruteforce())


def cli():
    parser = argparse.ArgumentParser(prog='pyshella-jsonrpc-bruter', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--coin-name', metavar='NAME', required=True, type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', metavar='URI', type=str, default=default_mongo_uri, help=mongo_uri)
    parser.add_argument('-l', '--logins', metavar='SINGLE/FILE', required=True, type=str, help=logins)
    parser.add_argument('-p', '--passwords', metavar='SINGLE/FILE', required=True, type=str, help=passwords)
    parser.add_argument('-b', '--brute-order', metavar='ORDER', type=list, default=['H', 'L', 'P'], help=brute_order)
    parser.add_argument('-t', '--threads', metavar='NUM', type=int, default=1, help=threads)
    parser.add_argument('-rT', '--read-timeout', metavar='SECS', type=float, default=.1, help=read_timeout_help)
    parser.add_argument('-cT', '--cycle-timeout', metavar='SECS', type=float, default=30, help=cycle_timeout_help)

    _run_jsonrpc_bruter(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()

