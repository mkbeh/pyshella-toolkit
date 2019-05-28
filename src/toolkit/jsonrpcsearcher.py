# -*- coding: utf-8 -*-
import re
import time
import asyncio
import urllib.parse

from src.extra import utils, decorators


class HTTPHeadersGetter:
    def __init__(self, **kwargs):
        super(HTTPHeadersGetter, self).__init__(**kwargs)
        self._timeout = kwargs.get('timeout', .1)
        self._read_timeout = kwargs.get('read_timeout', .1)
        self._only_jsonrpc = kwargs.get('only_jsonrpc', False)
