# -*- coding: utf-8 -*-
import scrapy


class CredsCrawler(scrapy.Spider):
    _iter_count = 0
    _page_num = 0
    _next_page_url_pattern = 'https://bitcointalk.org/index.php?board=159.{}'
    _last_page_num = None

    name = 'creds_crawler'
    start_urls = [
        f'https://bitcointalk.org/index.php?board=159.{_page_num}'
    ]

    def search_creds(self, response):
        pass

    def get_topic_urls(self, response):
        required_table_num = 8 if self._iter_count == 0 else 7
        self._iter_count += 1
        href_xpath = 'td[position() = 3]/span/a/@href'

        return response.xpath('//table')[required_table_num].xpath('tr')[1:].xpath(href_xpath).getall()

    def _set_last_page_num(self, response):
        self._last_page_num = \
            int(response.xpath('//table')[9].xpath('//a/@href')[-13].extract().split('.')[-1])

    def parse(self, response):
        if not self._last_page_num:
            self._set_last_page_num(response)

        for url in self.get_topic_urls(response):
            yield scrapy.Request(url, callback=self.search_creds)

        self._page_num += 40

        if self._page_num <= self._last_page_num:
            yield scrapy.Request(self._next_page_url_pattern.format(self._page_num), callback=self.parse)
