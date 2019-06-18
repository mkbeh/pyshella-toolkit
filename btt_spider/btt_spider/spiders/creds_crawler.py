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

    def _set_last_page_num(self, response):
        self._last_page_num = \
            int(response.xpath('//table')[9].xpath('//a/@href')[-13].extract().split('.')[-1])

    def _parse_topics(self, response, table_num):
        href_xpath = 'td[position() = 3]/span/a/@href'

        for topic_url in response.xpath('//table')[table_num].xpath('tr')[1:].xpath(href_xpath):
            print(topic_url.extract())

        self._page_num += 40
        self._iter_count += 1

    def parse(self, response):
        if not self._last_page_num:
            self._set_last_page_num(response)

        required_table_num = 8 if self._iter_count == 0 else 7
        self._parse_topics(response, required_table_num)
        next_page = response.urljoin(self._next_page_url_pattern.format(self._page_num))

        if self._last_page_num >= self._page_num:
            yield scrapy.Request(next_page, callback=self.parse)
