# -*- coding: utf-8 -*-
import re
import time
import asyncio
import urllib.parse

from src.extra.aiomotor import AIOMotor
from src.extra import utils, decorators


class PeersDataPreparation:
    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._hosts_block_size = kwargs.get('hS')
        self.ports_block_size = kwargs.get('pS')

        self._motor = AIOMotor(db_name='peers', uri=kwargs.get('mongo_uri'))

    @property
    async def _non_scanned_peers(self):
        return await self._motor.find_many(
            data={'scan status': False},
            collection=self._coin_name,
            to_list=False,
            cursor_length=self._hosts_block_size
        )

    @property
    async def hosts_data_block(self):
        return map(
            lambda x: f'http://{x["uri"].split(":")[0]}', await self._non_scanned_peers
        )


class JSONRPCSearcher(PeersDataPreparation):
    _last_port_num = 65535

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cycle_timeout = kwargs.get('cT', .1)
        self._read_timeout = kwargs.get('rT', .1)

    async def _get_http_headers(self, *args):
        pass

    async def jsonrpc_searcher_handler(self, host, ports):
        time.sleep(self._cycle_timeout)
        await asyncio.gather(
            *(self._get_http_headers(host, port) for port in ports)
        )

    async def run_jsonrpc_searcher(self):
        while True:
            for i in range(1, self._last_port_num, self.ports_block_size):
                if i + self.ports_block_size < self._last_port_num:
                    ports = utils.range_to_nums((i, i + self.ports_block_size))
                else:
                    ports = utils.range_to_nums((i, self._last_port_num))

                await asyncio.gather(
                    *(self.jsonrpc_searcher_handler(host, ports) for host in await self.hosts_data_block)
                )

            break
