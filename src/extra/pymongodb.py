# -*- coding: utf-8 -*-
from pymongo import MongoClient, errors


class PyMongoDB(object):
    def __init__(self, db_name: str, uri: str):
        try:
            cxn = MongoClient(uri)
        except errors.AutoReconnect:
            raise RuntimeError()

        self._db = cxn[db_name]

    def find_one(self, data: dict, collection: str, skip: int = 0) -> dict:
        return self._db[collection].find_one(data, skip=skip)

    def find_many(self, data: dict, collection: str, skip: int = 0, limit: int = 1, to_list=True) -> list or not list:
        documents = self._db[collection].find(data, skip=skip, limit=limit)
        return documents if to_list else (document for document in documents)

    def count(self, collection: str, filter_=None) -> int:
        filter_ = filter_ if filter_ else {}
        return self._db[collection].count(filter_)

    def update_one(self, find_data: dict, update_data: dict, collection: str):
        self._db[collection].update_one(
            filter=find_data,
            update={'$set': update_data},
        )

    def insert_one(self, document: dict, collection: str):
        self._db[collection].insert_one(document)

    def finish(self):
        self._db.logout()
