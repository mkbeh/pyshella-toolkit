# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import getpass
import warnings

import scrapy

from inline_requests import inline_requests
from loguru import logger

from src.extra import utils


warnings.filterwarnings("ignore")


def get_paths(workdir, *args):
    return (
        os.path.join(workdir, arg) for arg in args
    )


def get_credentials_files():
    if getpass.getuser() == 'root':
        return get_paths('/pyshella-toolkit/shared/wordlists',
                         'pyshella-rpcusers.lst',
                         'pyshella-rpcpasswords.lst')

    return get_paths(utils.get_work_dir('wordlists'), 'pyshella-rpcusers.lst', 'pyshella-rpcpasswords.lst')


class CredsCrawler(scrapy.Spider):
    logger.add(sys.stdout, format="{time:DD-MM-YYYY-MM-DD at HH:mm:ss} | {message}", level='INFO')

    _rpcuser_pattern = re.compile(r'(rpcuser=.+?)<br>')
    _rpcpwd_pattern = re.compile(r'(rpcpassword=.+?)<br>')

    _rpcusers_file, _rpcpasswords_file = get_credentials_files()
    _iter_count = 0
    _page_num = 0
    _next_page_url_pattern = 'https://bitcointalk.org/index.php?board=159.{}'
    _last_page_num = None

    name = 'creds_crawler'
    start_urls = [
        f'https://bitcointalk.org/index.php?board=159.{_page_num}'
    ]

    @staticmethod
    def _clear_str(s):
        pattern = re.compile(r'</?\w+>?')
        pattern1 = re.compile(r'\xa0')
        pattern2 = re.compile(r'[&lt;&gt;]')

        patterns = (pattern, pattern1, pattern2)

        if len(s) < 4 or '.conf' in s:
            return 'dirty_data'

        for pattern in patterns:
            s = re.sub(pattern, '', s)

        s = s.split(' ')
        return s[0] if len(s[0]) > 4 else 'dirty_data'

    def _prepare_creds(self, *args):
        return [
            self._clear_str(cred[0].split('=')[1])
            for cred in args
        ]

    def _write_creds(self, raw_rpcuser, raw_rpcpwd, topic):
        rpcuser, rpcpwd = self._prepare_creds(raw_rpcuser, raw_rpcpwd)

        with open(self._rpcusers_file, 'a') as ru, open(self._rpcpasswords_file, 'a') as rp:
            ru.write(f'{rpcuser}\n')
            rp.write(f'{rpcpwd}\n')

        logger.debug(f'Found next credentials: RPCUSER={rpcuser} RPCPASSWORD={rpcpwd} '
                     f'in topic: {topic}.')

    def _search_creds(self, response):
        body = response.xpath('//body').get()
        rpcuser = re.findall(self._rpcuser_pattern, body)
        rpcpwd = re.findall(self._rpcpwd_pattern, body)

        if rpcuser and rpcpwd:
            self._write_creds(rpcuser, rpcpwd, response.url)

    def _get_topics_urls(self, response):
        required_table_num = 8 if self._iter_count == 0 else 7
        self._iter_count += 1
        href_xpath = 'td[position() = 3]/span/a/@href'

        return response.xpath('//table')[required_table_num].xpath('tr')[1:].xpath(href_xpath).getall()

    def _set_last_page_num(self, response):
        self._last_page_num = \
            int(response.xpath('//table')[9].xpath('//a/@href')[-13].extract().split('.')[-1])

    def _help_msg(self):
        logger.debug(f'Wordlists files are located: {self._rpcusers_file} | {self._rpcpasswords_file}')
        time.sleep(5)

    @inline_requests
    def parse(self, response):
        if not self._last_page_num:
            self._help_msg()
            self._set_last_page_num(response)

        for url in self._get_topics_urls(response):
            topic_url = response.urljoin(url)
            next_resp = yield scrapy.Request(topic_url, dont_filter=True)
            self._search_creds(next_resp)

        self._page_num += 40

        if self._page_num <= self._last_page_num:
            next_page = self._next_page_url_pattern.format(self._page_num)
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
