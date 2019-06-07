# -*- coding: utf-8 -*-
from aiobitcoin.wallet import Wallet
from src.extra.pymongodb import PyMongoDB


class CoinsWithdrawal:
    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._interval = kwargs.get('interval')

        self.mongo_withdrawal = PyMongoDB(db_name='withdrawal', uri=kwargs.get('mongo_uri'))

    async def coins_withdrawal(self):
        pass
