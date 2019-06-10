# -*- coding: utf-8 -*-
import time

from aiobitcoin.network import Network
from aiobitcoin.bitcoinerrors import NoConnectionToTheDaemon

from src.extra import utils
from src.extra.aiomotor import AIOMotor


motor = coin_name = None
logger = utils.setup_logger(
    logger_name='scanner',
    log_file=utils.get_file_path('pyshella-toolkit', 'scanner.log')
)


async def _write_peer(**kwargs):
    kwargs.update({'scan status': False})
    await motor.insert_one(
        document=kwargs,
        collection=coin_name,
        index='uri',
        unique=True
    )


async def _get_ip_from_addr(addr):
    return addr.split(':')[0]


async def _add_new_peers(uri, ban_time):
    added_peers_num = 0

    async with Network(url=uri) as network:
        for count, peer_info in enumerate(await network.get_peer_info(to_list=False)):
            if count < 2:
                continue

            ip = await _get_ip_from_addr(peer_info["addr"])
            addr, subver = peer_info["addr"], peer_info["subver"]
            await network.set_ban(ip, bantime=ban_time)

            await _write_peer(uri=addr, subver=subver)
            added_peers_num += 1

    logger.info(f'Successfully added {added_peers_num} new peers.')


async def peers_scanner(args):
    global motor, coin_name
    node_uri, ban_time, interval, mongo_uri, coin_name = args.values()
    motor = AIOMotor(db_name='peers', uri=mongo_uri)

    while True:
        try:
            await _add_new_peers(node_uri, ban_time)
        except NoConnectionToTheDaemon:
            logger.warning('Сonnection to daemon was lost.')
        finally:
            time.sleep(interval)
