# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.scanner import scanner


cli_desc = 'Scanner which parse Bitcoin or forks peers and writes them into file.'
uri_help_text = 'Node URI.'
ban_time_help_text = 'The time(days) which will be banned each peer (by default 14 days).'
interval_help_text = 'Interval(secs) between call cycles for new peers (by default 60 secs).'
epilog = """
Usage example: pyshella_scanner -u <node_uri>

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_scanner(**kwargs):
    uvloop.install()
    asyncio.run(scanner(kwargs))


def cli():
    parser = argparse.ArgumentParser(prog='pyshella_scanner', description=cli_desc, epilog=epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-nU', '--node-uri', required=True, metavar='', dest='uri', type=str, help=uri_help_text)
    parser.add_argument('-b', '--ban-time', metavar='', default=14 * 86400, type=int, help=ban_time_help_text)
    parser.add_argument('-i', '--interval', metavar='', default=60, type=int, help=interval_help_text)
    parser.add_argument('-mU', '--mongo-uri', required=True, metavar=' ', type=str, help='MongoDB uri.')
    parser.add_argument('-n', '--coin-name', required=True, metavar=' ', type=str, help='Name of cryptocurrency.')

    args = vars(parser.parse_args())
    _run_scanner(**args)


if __name__ == '__main__':
    cli()
