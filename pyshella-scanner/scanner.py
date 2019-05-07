# -*- coding: utf-8 -*-
# TODO
#   1. добавить логгирование при добавлении новых пиров и количество.
#   3. создать отдельную папку в директории пользователя и туда класть файлы и логи
#   4. добавить cli интерфейс
import time
import asyncio
import uvloop

from aiobitcoin.grambitcoin import GramBitcoin
from extra import decorators


url = 'http://bitcoinrpc:80d3fa20b89f12225a4d3d54634601c7@46.160.199.52:18332'
ban_time = 14 * 86400
interval = 60


async def _get_ip_from_addr(addr):
    return addr.split(':')[0]


@decorators.log('peers.lst')
async def _add_new_peers():
    async with GramBitcoin(url=url) as gram:
        for count, peer_info in enumerate(await gram.get_peer_info(to_list=False)):
            if count < 2:
                continue

            ip, addr, subver = await _get_ip_from_addr(peer_info["addr"]), peer_info["addr"], peer_info["subver"]
            await gram.set_ban(ip, bantime=ban_time)

            yield f'{addr}:{subver}\n'


async def scanner():
    while True:
        await _add_new_peers()
        # time.sleep(interval)
        break


def main():
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(scanner())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    main()
