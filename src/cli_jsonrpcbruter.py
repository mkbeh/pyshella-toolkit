# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.jsonrpcbruter import Bruter


default_mongo_uri = 'mongodb://root:toor@localhost:27017'

cli_desc = 'Bitcoin/fork JSON-RPC bruter.'
mongo_uri = f'MongoDB URI. Default: {default_mongo_uri}'
users = 'Single user or file with users.'
passwords = 'Single password or file with passwords.'
threads = 'The number of coroutines that will be asynchronous in bruteforce process.'
epilog = """
-----------------------------------------------------
Usage example: [TO DO]

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_jsonrpc_bruter(**kwargs):
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Bruter(**kwargs).run_bruteforce())


def cli():
    parser = argparse.ArgumentParser(prog='pyshella-jsonrpc-bruter', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--coin-name', metavar='NAME', required=True, type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', metavar='URI', type=str, default=default_mongo_uri, help=mongo_uri)
    parser.add_argument('-u', '--users', metavar='SINGLE/FILE', required=True, type=str, help=users)
    parser.add_argument('-p', '--passwords', metavar='SINGLE/FILE', required=True, type=str, help=passwords)
    parser.add_argument('-b', '--brute-order', metavar='NUMS', type=list, default=['H', 'U', 'P'], help=threads)
    parser.add_argument('-t', '--threads', metavar='NUM', type=int, default=1, help=threads)

    from secret import args_lst3
    _run_jsonrpc_bruter(**vars(parser.parse_args(args_lst3)))


if __name__ == '__main__':
    cli()

