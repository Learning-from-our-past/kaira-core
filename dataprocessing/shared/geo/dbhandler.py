# -*- coding: utf-8 -*-
from pymongo import MongoClient, ASCENDING
from bson import ObjectId
import pytz


class DatabaseHandler:
    dbName = 'geonames'  #name of the db where collections are located
    mongoDBAddress = 'localhost'
    mongoPort = 27017


    def __init__(self):
        self.client = MongoClient(self.mongoDBAddress, self.mongoPort)
        self.db = self.client[self.dbName]
        #self.db.authenticate(self.dbUserName, self.dbUserPassword)

    def checkIfCollectionExists(self, name):
        coll = self.db.collection_names()
        if name in coll:
            return True
        else:
            return False

    def storeToDb(self, entry, collectionName):
        self.db[collectionName].insert(entry)

    def getFromDb(self, query, collectionName):
        found = list(self.db[collectionName].find(query, { "score": { "$meta": "textScore" } }).sort([("score", {"$meta": "textScore"})]))
        return found

    def saveToDb(self, entry, collection):
        collection.save(entry)

    def clearCollection(self, collection):
        collection.remove()

    def dropCollection(self, name):
        self.db[name].drop()