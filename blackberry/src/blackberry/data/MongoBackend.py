from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.data.DataBackend import DataBackend
from pymongo import MongoClient
import logging
from pymongo.errors import AutoReconnect

class MongoBackend(DataBackend):
    def __init__(self, configuration=CurrentConfig.data.local_db):
        super(MongoBackend, self).__init__(configuration)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Connecting to MongoDB instance at %s', configuration.db)
        self._mongo_client = MongoClient(configuration.db)

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = self._mongo_client.get_default_database()
        return self._db

    @property
    def collection(self):
        if not hasattr(self, '_collection'):
            self._collection = self.db[self.configuration.collection]
        return self._collection
        
    @property
    def isActive(self):
        return self._mongo_client.admin.command('ping')
        
    def commit(self, data):
        if isinstance(data, list):
            for row in data:
                self.commit(row)
        else:
            tries = 0
            while tries < 5:
                try:
                    self.collection.insert(data.copy())
                except AutoReconnect as ar:
                    self._logger.warn('Failed to transmit data to MongoDB: %r', ar)
                    tries += 1
                
            if tries == 5:
                self._logger.error('Failed to log data series. See previous exceptions.')
        
