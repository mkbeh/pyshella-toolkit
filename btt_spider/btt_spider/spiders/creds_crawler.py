# -*- coding: utf-8 -*-
import os
import sys
import re
import time

import scrapy

from loguru import logger


logger.add(sys.stdout, format="{time:DD-MM-YYYY-MM-DD at HH:mm:ss} | {message}", level='INFO')


def get_work_dir():
    return os.path.join(
        os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share")), 'wordlists'
    )


def get_paths(workdir, *args):
    return (
        os.path.join(workdir, arg) for arg in args
    )


def get_credentials_files():
    if os.environ.get('USER') == 'root':
        return get_paths('/pyshella-toolkit/wordlists', 'pyshella-rpcusers.lst', 'pyshella-rpcpasswords.lst')

    return get_paths(get_work_dir(), 'pyshella-rpcusers.lst', 'pyshella-rpcpasswords.lst')


class CredsCrawler(scrapy.Spider):
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
    def _prepare_creds(*args):
        return [
            cred[0].split('=')[1] for cred in args
        ]

    def _write_creds(self, raw_rpcuser, raw_rpcpwd):
        rpcuser, rpcpwd = self._prepare_creds(raw_rpcuser, raw_rpcpwd)

        with open('default_rpcusers.lst', 'a') as ru, open('default_rpcpasswords.lst', 'a') as rp:
            ru.write(f'{rpcuser}\n')
            rp.write(f'{rpcpwd}\n')

        logger.debug(f'Found next credentials: RPCUSER={rpcuser} RPCPASSWORD={rpcpwd}.')

    def _search_creds(self, response):
        body = response.xpath('//body').get()
        rpcuser = re.findall(self._rpcuser_pattern, body)
        rpcpwd = re.findall(self._rpcpwd_pattern, body)

        if rpcuser and rpcpwd:
            self._write_creds(rpcuser, rpcpwd)

    def _get_topic_urls(self, response):
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

    def parse(self, response):
        if not self._last_page_num:
            self._help_msg()
            self._set_last_page_num(response)

        for url in self._get_topic_urls(response):
            yield scrapy.Request(url, callback=self._search_creds)

        self._page_num += 40

        if self._page_num <= self._last_page_num:
            yield scrapy.Request(self._next_page_url_pattern.format(self._page_num), callback=self.parse)
