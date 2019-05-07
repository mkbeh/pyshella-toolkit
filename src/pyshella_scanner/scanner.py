# -*- coding: utf-8 -*-
import time

from aiobitcoin.grambitcoin import GramBitcoin
from aiobitcoin.bitcoinerrors import NoConnectionToTheDaemon
from src.extra import decorators, utils

peers_file = utils.get_file_path('pyshella', 'peers.lst')
logger = utils.setup_logger(
    logger_name='scanner',
    log_file=utils.get_file_path('pyshella', 'scanner.log')
)


async def _get_ip_from_addr(addr):
    return addr.split(':')[0]


@decorators.write(peers_file)
async def _add_new_peers(uri, ban_time):
    added_peers_num = 0

    async with GramBitcoin(url=uri) as gram:
        for count, peer_info in enumerate(await gram.get_peer_info(to_list=False)):
            if count < 2:
                continue

            ip, addr, subver = await _get_ip_from_addr(peer_info["addr"]), peer_info["addr"], peer_info["subver"]
            await gram.set_ban(ip, bantime=ban_time)

            yield f'{addr}:{subver}\n'
            added_peers_num += 1

    logger.info(f'Successfully added {added_peers_num} peers.')


async def scanner(args):
    uri, ban_time, interval = args.values()

    while True:
        try:
            await _add_new_peers(uri, ban_time)
        except NoConnectionToTheDaemon:
            logger.warning('Сonnection to daemon was lost.')
        finally:
            time.sleep(interval)
