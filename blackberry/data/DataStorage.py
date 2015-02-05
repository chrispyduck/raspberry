from blackberry.configuration.ConfigData import CurrentConfig
from pymongo import MongoClient

class DataStorage(object):
    def __init__(self):
        self._mongo_client = MongoClient(CurrentConfig.data.local_db.db)
        self._db = self._mongo_client.get_default_database()
        self._collection = self._db[CurrentConfig.data.local_db.collection]