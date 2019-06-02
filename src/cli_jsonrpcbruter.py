# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.jsonrpcbruter import Bruter


default_mongo_uri = 'mongodb://root:toor@localhost:27017'

cli_desc = 'Bitcoin/fork JSON-RPC bruter.'
mongo_uri_help = f'MongoDB URI. Default: {default_mongo_uri}'
passwords_help = 'Single password or file with passwords.'
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
    loop.run_until_complete(Bruter(**kwargs).start_bruteforce())


def cli():
    parser = argparse.ArgumentParser(prog='pyshella-jsonrpc-searcher', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--coin-name', metavar='NAME', required=True, type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', metavar='URI', type=str, default=default_mongo_uri, help=mongo_uri_help)
    parser.add_argument('-u', '--users', metavar='SINGLE/FILE', type=str, help='Single user or file with users.')
    parser.add_argument('-p', '--passwords', metavar='SINGLE/FILE', type=str, help=passwords_help)

    _run_jsonrpc_bruter(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()

