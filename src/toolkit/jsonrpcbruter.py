# -*- coding: utf-8 -*-
import asyncio
import linecache

from collections import namedtuple

from src.extra import utils
from src.extra.aiomotor import AIOMotor


class BruteBase:
    _DataCount = namedtuple('DataCount', ['count', 'data'])

    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._brute_order = kwargs.get('brute_order')
        self._unordered_data = {
            'H': AIOMotor(db_name='jsonrpc', uri=kwargs.get('mongo_uri')),
            'U': kwargs.get('users'),
            'P': kwargs.get('passwords'),
        }

    @property
    def _sorted_brute_order_data(self):
        return [self._unordered_data.get(val) for val in self._unordered_data]

    async def els_in_data(self, data):
        try:
            count = await data.count_docs(self._coin_name)
        except AttributeError:
            count = utils.count_lines(data)

        return self._DataCount(count, data)

    @property
    async def _data_counts(self):
        return [
            await self.els_in_data(data)
            for data in self._sorted_brute_order_data
        ]

    @property
    async def brute_data(self):
        first, second, third = await self._data_counts

        for i in range(first.count):
            for j in range(second.count):
                for k in range(third.count):
                    yield


class Bruter(BruteBase):
    def __init__(self, **kwargs):
        super(Bruter, self).__init__(**kwargs)

    async def bruteforce(self):
        pass

    async def bruteforce_handler(self):
        pass

    async def run_bruteforce(self):
        async for data in self.brute_data:
            print(data)
