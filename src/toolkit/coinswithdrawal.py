# -*- coding: utf-8 -*-
import time

from loguru import logger

from aiobitcoin.grambitcoin import GramBitcoin
from aiobitcoin.wallet import Wallet

from src.extra.pymongodb import PyMongoDB


logger_cw = logger.bind(util='coins-withdrawal')


class CoinsWithdrawal:
    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._interval = kwargs.get('interval')
        self._withdrawal_addr = kwargs.get('withdrawal_address')

        self._mongo_withdrawal = PyMongoDB(db_name='withdrawal', uri=kwargs.get('mongo_uri'))
        self._mongo_credentials = PyMongoDB(db_name='credentials', uri=kwargs.get('mongo_uri'))

    def _update_withdrawal_status(self, uri, status):
        self._mongo_credentials.update_one(
            find_data={'uri': uri},
            update_data={'withdrawal': status},
            collection=self._coin_name
        )

    def _write_data(self, **kwargs):
        self._mongo_withdrawal.insert_one(
            document=kwargs,
            collection=self._coin_name
        )

    @staticmethod
    def _prepare_data(data):
        return (
            el['uri'] for el in data
        )

    @property
    def _peers_with_creds(self):
        documents = self._mongo_credentials.find_many(
            data={'withdrawal': False},
            collection=self._coin_name,
            limit=100,
            to_list=False
        )

        return self._prepare_data(documents)

    async def _actions_with_positive_balance(self, wallet, balance, uri):
        await wallet.send_to_address(self._withdrawal_addr, balance)

        self._write_data(uri=uri, amount=balance, recipient=self._withdrawal_addr)
        self._update_withdrawal_status(uri, True)
        logger_cw.info(f'Successfully transferred coins from {uri} to {self._withdrawal_addr}. Amount: {balance}.')

    @logger_cw.catch()
    async def coins_withdrawal(self):
        while True:
            gram = GramBitcoin(session_required=True)

            for uri in self._peers_with_creds:
                wallet = Wallet(url=uri, gram=gram, read_timeout=10)
                balance = await wallet.get_balance()

                if balance > 0:
                    await self._actions_with_positive_balance(wallet, balance, uri)
                    continue

                self._update_withdrawal_status(uri, 'ZeroBalance')

            await gram.close_session()
            time.sleep(self._interval)
