# -*- coding-utf-8 -*-
import argparse
import asyncio
import uvloop

from src.toolkit.coinswithdrawal import CoinsWithdrawal


cli_description = 'Utility which withdrawal crypto currency from bruted JSON-RPC.'
cli_interval_help = 'Timeout after coins withdrawal from all the peers that were collected in the database ' \
                    'at the moment.'
cli_epilog = """
-----------------------------------------------------------------------------------
Usage example: [TO DO]

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


def _run_coins_withdrawal(**kwargs):
    uvloop.install()
    asyncio.run(
        CoinsWithdrawal(**kwargs).coins_withdrawal()
    )


def cli():
    parser = argparse.ArgumentParser(prog='pyshella-coins-withdrawal', description=cli_description, epilog=cli_epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', '--coin-name', required=True, metavar=' ', type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', required=True, metavar=' ', type=str, help='MongoDB uri.')
    parser.add_argument('-i', '--interval', metavar='', default=3*60, type=int, help=cli_interval_help)

    from secret import args_lst4
    _run_coins_withdrawal(**vars(parser.parse_args(args_lst4)))


if __name__ == '__main__':
    cli()
