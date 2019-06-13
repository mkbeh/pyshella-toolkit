# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.peersscanner import peers_scanner


cli_desc = 'Scanner which parse Bitcoin or forks peers and writes them into MongoDB.'
uri_help_text = 'BTC/fork node URI.'
ban_time_help_text = 'The time which will be banned each peer (by default 30 days).'
interval_help_text = 'Interval between call cycles for getting new peers (by default 60 secs).'
epilog = """
-----------------------------------------------------------------------------------
Usage example: pyshella-peers-scanner -nU <node_uri> -mU <mongo_uri> -n <coin_name>

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_peers_scanner(**kwargs):
    uvloop.install()
    asyncio.run(peers_scanner(kwargs))


def cli():
    parser = argparse.ArgumentParser(prog='pyshella-peers-scanner', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-nU', '--node-uri', required=True, metavar='URI', dest='uri', type=str, help=uri_help_text)
    parser.add_argument('-b', '--ban-time', metavar='SECS', default=30 * 86400, type=int, help=ban_time_help_text)
    parser.add_argument('-i', '--interval', metavar='SECS', default=60, type=int, help=interval_help_text)
    parser.add_argument('-mU', '--mongo-uri', required=True, metavar='URI', type=str, help='MongoDB uri.')
    parser.add_argument('-n', '--coin-name', required=True, metavar='NAME', type=str, help='Name of cryptocurrency.')

    _run_peers_scanner(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
