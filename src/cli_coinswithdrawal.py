# -*- coding-utf-8 -*-
import argparse
import asyncio
import uvloop

from loguru import logger

from src.extra import utils
from src.toolkit.coinswithdrawal import CoinsWithdrawal


cli_description = 'Utility which withdrawal crypto currency from bruted JSON-RPC.'
cli_interval_help = 'Timeout after coins withdrawal from all the peers that were collected in the database ' \
                    'at the moment. By default 3 min.'
cli_withdrawal_help = 'The address to which the coins will be sent.'
cli_epilog = """
-----------------------------------------------------------------------------------------------------------------------
Usage example: pyshella-coins-withdrawal -n Bitcoin -mU mongodb://root:toor@localhost:27017 -a <withdrawal_addr> -i 300

|-----------------|
|Created by @mkbeh|
|-----------------|
"""


utils.setup_logger('toolkit.log')
logger_exc = logger.bind(util='cli-exception')


def _run_coins_withdrawal(**kwargs):
    uvloop.install()
    asyncio.run(
        CoinsWithdrawal(**kwargs).coins_withdrawal()
    )


@logger_exc.catch()
def cli():
    parser = argparse.ArgumentParser(prog='pyshella-coins-withdrawal', description=cli_description, epilog=cli_epilog,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-n', '--coin-name', required=True, metavar='NAME', type=str, help='Name of cryptocurrency.')
    parser.add_argument('-mU', '--mongo-uri', required=True, metavar='URI', type=str, help='MongoDB uri.')
    parser.add_argument('-a', '--withdrawal-address', required=True, metavar='ADDR', type=str, help=cli_withdrawal_help)
    parser.add_argument('-i', '--interval', metavar='SECS', default=3*60, type=int, help=cli_interval_help)

    _run_coins_withdrawal(**vars(parser.parse_args()))


if __name__ == '__main__':
    cli()
