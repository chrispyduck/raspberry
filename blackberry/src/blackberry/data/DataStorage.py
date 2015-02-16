from blackberry.configuration.ConfigData import CurrentConfig
from pymongo import MongoClient
import logging

class DataStorage(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Connecting to local MongoDB instance at %s', CurrentConfig.data.local_db.db)
        self._mongo_client = MongoClient(CurrentConfig.data.local_db.db)
        self._db = self._mongo_client.get_default_database()
        self._collection = self._db[CurrentConfig.data.local_db.collection]
        
    def commit(self, data):
        self._collection.insert(data)