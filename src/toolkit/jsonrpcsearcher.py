# -*- coding: utf-8 -*-
import re
import time
import asyncio
import urllib.parse

from src.extra import utils, decorators
from src.extra.aiomotor import AIOMotor


class DataPreparation:
    _motor = AIOMotor(db_name='peers', uri='mongodb://root:toor@localhost:27017')

    def __init__(self, **kwargs):
        self._hosts_block_size = kwargs.get('hS')
        self._ports_block_size = kwargs.get('pS')


class JSONRPCSearcher(DataPreparation):
    def __init__(self, **kwargs):
        print(kwargs)
        super().__init__(**kwargs)
        self._timeout = kwargs.get('timeout', .1)
        self._read_timeout = kwargs.get('read_timeout', .1)

    async def run_jsonrpc_searcher(self):
        pass
