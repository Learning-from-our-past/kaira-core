# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
import pytz

loc_count = 0
mul_count = 0

class DatabaseHandler:
    db_name = 'geonames'  # name of the db where collections are located
    mongo_db_address = 'localhost'
    mongo_port = 27017

    def __init__(self):
        self.client = MongoClient(self.mongo_db_address, self.mongo_port)
        self.db = self.client[self.db_name]

    def check_if_collection_exists(self, name):
        coll = self.db.collection_names()
        if name in coll:
            return True
        else:
            return False

    def store_to_db(self, entry, collection_name):
        self.db[collection_name].insert(entry)

    def get_from_db(self, query, collection_name):
        found = list(self.db[collection_name].find(query, {"score": {"$meta": "textScore"}}).sort([("score", {"$meta": "textScore"})]))
        return found

    def save_to_db(self, entry, collection):
        collection.save(entry)

    def clear_collection(self, collection):
        collection.remove()

    def drop_collection(self, name):
        self.db[name].drop()