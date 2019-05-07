# -*- coding: utf-8 -*-
import argparse
import asyncio
import uvloop

from pyshella_scanner.scanner import scanner


cli_desc = 'Scanner which parse Bitcoin or forks peers and writes them into file.'
uri_help_text = 'Node URI.'
ban_time_help_text = 'The time(days) which will be banned each peer (by default 14 days).'
interval_help_text = 'Interval(secs) between call cycles for new peers (by default 60 secs).'
epilog = """
|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_scanner(**kwargs):
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(scanner(kwargs))


def cli():
    parser = argparse.ArgumentParser(prog='pyshella_scanner', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=cli_desc, epilog=epilog)
    parser.add_argument('-u', '--uri', nargs=1, required=True, metavar='', dest='uri', type=str, help=uri_help_text)
    parser.add_argument('-b', '--ban-time', nargs=1, metavar='', default=14 * 86400, type=int, help=ban_time_help_text)
    parser.add_argument('-i', '--interval', nargs=1, metavar='', default=60, type=int, help=interval_help_text)

    args = parser.parse_args()
    _run_scanner(uri=args.uri[0], ban_time=args.ban_time, interval=args.interval)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    cli()
