# -*- coding: utf-8 -*-
import asyncio
import linecache

from collections import namedtuple

from src.extra import utils
from src.extra.pymongodb import PyMongoDB


class BruterBase:
    _DataCount = namedtuple('DataCount', ['count', 'data'])

    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._brute_order = kwargs.get('brute_order')
        self._num_threads = kwargs.get('threads')
        self._unordered_data = {
            'H': PyMongoDB(db_name='jsonrpc', uri=kwargs.get('mongo_uri')),
            'U': kwargs.get('users'),
            'P': kwargs.get('passwords'),
        }

    @staticmethod
    def _prepare_data_from_db(docs):
        return (
            f'{document["peer"]}:{document["jsonrpc"]}'
            for document in docs
        )

    def _get_data_from_db(self, data, skip, limit):
        documents = data.find_many(
            data={'jsonrpc': {'$gt': 0}},
            collection=self._coin_name,
            skip=skip,
            limit=limit,
            to_list=False
        )

        return self._prepare_data_from_db(documents)

    @staticmethod
    def _get_data_from_file(data, start, end):
        start = 1 if start == 0 else start
        return (
            utils.clear_string(linecache.getline(data, line))
            for line in range(start, end)
        )

    def _get_single_data_from_db(self, data, point):
        params = {
            'data': {'jsonrpc': {'$gt': 0}},
            'collection': self._coin_name,
            'skip': point
        }

        document = data.find_one(**params)
        return f'{document["peer"]}:{document["jsonrpc"]}'

    @staticmethod
    def _get_single_data_from_file(data, point):
        return utils.clear_string(
            linecache.getline(data, point)
        )

    def _get_data_block_by_point(self, data, point):
        start, end = point, point + self._num_threads

        if isinstance(data, str):
            genexpr = self._get_data_from_file(data, start, end)
        else:
            genexpr = self._get_data_from_db(data, start, end)

        return genexpr

    def _get_data_by_point(self, data, point):
        if isinstance(data, str):
            return self._get_single_data_from_file(data, point + 1)
        else:
            return self._get_single_data_from_db(data, point)

    @property
    def _sorted_brute_order_data(self):
        return [
            self._unordered_data.get(val) for val in self._brute_order
        ]

    def _els_amount_in_data(self, data):
        try:
            count = data.count(
                collection=self._coin_name,
                filter_={'jsonrpc': {'$gt': 0}}
            )
        except TypeError:
            count = utils.count_lines(data)

        return self._DataCount(count, data)

    @property
    def _data_counts(self):
        return [
            self._els_amount_in_data(data)
            for data in self._sorted_brute_order_data
        ]

    @property
    def brute_data(self):
        first, second, third = self._data_counts

        for i in range(first.count):
            first_val = self._get_data_by_point(first.data, i)

            for j in range(second.count):
                second_val = self._get_data_by_point(second.data, j)

                for k in range(0, third.count, self._num_threads):
                    third_range = self._get_data_block_by_point(third.data, k)
                    yield first_val, second_val, third_range


class JSONRPCBruter(BruterBase):
    def __init__(self, **kwargs):
        super(JSONRPCBruter, self).__init__(**kwargs)

    async def bruteforce(self):
        pass

    async def bruteforce_handler(self):
        pass

    async def run_bruteforce(self):
        for data in self.brute_data:
            pass
