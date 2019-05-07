# -*- coding: utf-8 -*-
# TODO
#   1. добавить логгирование при добавлении новых пиров и количество.
#   3. создать отдельную папку в директории пользователя и туда класть файлы и логи
import time
import logging


from aiobitcoin.grambitcoin import GramBitcoin
from aiobitcoin.bitcoinerrors import NoConnectionToTheDaemon
from extra import decorators


async def _get_ip_from_addr(addr):
    return addr.split(':')[0]


@decorators.log('peers.lst')
async def _add_new_peers(uri, ban_time):
    async with GramBitcoin(url=uri) as gram:
        for count, peer_info in enumerate(await gram.get_peer_info(to_list=False)):
            if count < 2:
                continue

            ip, addr, subver = await _get_ip_from_addr(peer_info["addr"]), peer_info["addr"], peer_info["subver"]
            await gram.set_ban(ip, bantime=ban_time)

            yield f'{addr}:{subver}\n'


async def scanner(args):
    uri, ban_time, interval = args.values()

    while True:
        try:
            await _add_new_peers(uri, ban_time)
        except NoConnectionToTheDaemon:
            logging.warning('Сonnection to daemon was lost.')
        finally:
            time.sleep(interval)
