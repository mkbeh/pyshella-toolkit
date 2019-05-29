# -*- coding: utf-8 -*-
import re
import time
import asyncio
import urllib.parse

from src.extra.aiomotor import AIOMotor
from src.extra import utils


class PeersDataPreparation:
    def __init__(self, **kwargs):
        super(PeersDataPreparation, self).__init__(**kwargs)
        self._hosts_block_size = kwargs.get('hS')
        self.coin_name = kwargs.get('coin_name')
        self.ports_block_size = kwargs.get('pS')

        self.motor_peers = AIOMotor(db_name='peers', uri=kwargs.get('mongo_uri'))

    @property
    async def _non_scanned_peers(self):
        return await self.motor_peers.find_many(
            data={'scan status': False},
            collection=self.coin_name,
            to_list=False,
            cursor_length=self._hosts_block_size
        )

    async def get_peers_block(self):
        return map(
            lambda x: f'http://{x["uri"].split(":")[0]}', await self._non_scanned_peers
        )


class HTTPHeadersGetter:
    def __init__(self, **kwargs):
        self._coin_name = kwargs.get('coin_name')
        self._read_timeout = kwargs.get('rT', .1)

        self._motor_jsonrpc = AIOMotor(db_name='jsonrpc', uri=kwargs.get('mongo_uri'))

    async def _write_peer_data(self, **kwargs):
        await self._motor_jsonrpc.insert_one(
            document=kwargs,
            collection=self._coin_name,
        )

    async def _read_headers(self, reader):
        lines = []

        while True:
            line = await asyncio.wait_for(reader.readline(), self._read_timeout)

            if not line:
                break

            line = line.decode('utf-8').rstrip()

            if line:
                lines.append(line)

        return lines if lines else None

    @staticmethod
    async def _write_query(url_path, url_hostname, writer):
        query = (
            f"HEAD {url_path or '/'} HTTP/1.0\r\n"
            f"Host: {url_hostname}\r\n"
            f"\r\n"
        )

        writer.write(query.encode('utf-8'))
        await writer.drain()

    async def _header_reading_handler(self, *args):
        url, writer, reader = args
        await self._write_query(url.path, url.hostname, writer)

        try:
            headers = await self._read_headers(reader)
        except (asyncio.futures.TimeoutError, ConnectionResetError):
            headers = None
        finally:
            writer.close()

        return headers

    async def _open_connection(self, url_hostname, port):
        return await asyncio.wait_for(
                asyncio.open_connection(url_hostname, port), timeout=self._read_timeout
        )

    async def get_peer_http_headers(self, uri, port=None):
        url = urllib.parse.urlsplit(uri)

        try:
            reader, writer = await self._open_connection(url.hostname, port)
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return
        else:
            return await self._header_reading_handler(url, writer, reader)

    async def find_jsonrpc(self, host, port):
        pattern_forbidden_error = re.compile(r'403 Forbidden', re.IGNORECASE)
        pattern_jsonrpc = re.compile(r'jsonrpc|json-rpc|json rpc', re.IGNORECASE)
        headers = await self.get_peer_http_headers(host, port)

        if not headers:
            return

        for header in headers:
            if re.search(pattern_forbidden_error, header):
                await self._write_peer_data(peer=host, port=port, headers=headers, jsonrpc=None)
                break
            elif re.search(pattern_jsonrpc, header):
                await self._write_peer_data(peer=host, port=port, headers=headers, jsonrpc=port)
                break


class JSONRPCSearcher(PeersDataPreparation, HTTPHeadersGetter):
    _last_port_num = 65535

    def __init__(self, **kwargs):
        super(JSONRPCSearcher, self).__init__(**kwargs)
        self._cycle_timeout = kwargs.get('cT', .1)

    async def _update_peers_scan_status(self, peers_block):
        for peer in peers_block:
            await self.motor_peers.update_one(
                find_data={'uri': re.compile(fr'{peer}')},
                update_data={'scan status': True},
                collection=self.coin_name
            )

    async def _jsonrpc_searcher_handler(self, host, ports):
        time.sleep(self._cycle_timeout)
        await asyncio.gather(
            *(self.find_jsonrpc(host, port) for port in ports)
        )

    async def run_jsonrpc_searcher(self):
        while True:
            hosts_block = await self.get_peers_block()

            for i in range(1, self._last_port_num, self.ports_block_size):
                if i + self.ports_block_size < self._last_port_num:
                    ports = utils.range_to_nums((i, i + self.ports_block_size))
                else:
                    ports = utils.range_to_nums((i, self._last_port_num))

                await asyncio.gather(
                    *(self._jsonrpc_searcher_handler(host, ports) for host in hosts_block)
                )

            await self._update_peers_scan_status(hosts_block)
            time.sleep(self._cycle_timeout)
