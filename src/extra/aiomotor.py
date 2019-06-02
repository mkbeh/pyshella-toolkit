# -*- coding: utf-8 -*-
import logging

from pymongo import errors
from motor import motor_asyncio


logging.basicConfig(level=logging.INFO)


class AIOMotor:
    def __init__(self, db_name: str, uri: str, loop=None):
        try:
            if loop:
                cxn = motor_asyncio.AsyncIOMotorClient(uri, io_loop=loop)
            else:
                cxn = motor_asyncio.AsyncIOMotorClient(uri)
        except errors.AutoReconnect:
            raise RuntimeError()

        self._db = cxn[db_name]

    async def insert_one(self, document: dict, collection: str,
                         index: str = None, unique: bool = False):
        if unique:
            self._db[collection].create_index(index, unique=True)

        try:
            await self._db[collection].insert_one(document)
        except errors.DuplicateKeyError:
            pass

    async def insert_many(self, data: list, collection: str):
        await self._db[collection].insert_many(data)

    async def find_one(self, data: dict, collection: str) -> dict:
        return await self._db[collection].find_one(data)

    async def find_many(self, data: dict, collection: str, skip: int = 0,
                        cursor_length: int = 10_000, to_list: bool = True) -> list or not list:
        cursor = self._db[collection].find(data).skip(skip)

        if to_list:
            return await cursor.to_list(length=cursor_length)

        return (
            document for document in await cursor.to_list(length=cursor_length)
        )

    async def update_one(self, find_data: dict, update_data: dict, collection: str):
        await self._db[collection].update_one(find_data, {'$set': update_data})

    async def update_many(self, find_data: dict, update_data: dict, collection: str):
        await self._db[collection].update_many(find_data, {'$set': update_data})

    async def count_docs(self, collection: str, filter_=None):
        filter_ = filter_ if filter_ else {}
        return await self._db[collection].count_documents(filter_)
