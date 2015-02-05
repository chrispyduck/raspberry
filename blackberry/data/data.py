from pymongo import MongoClient
from configuration import configuration
from datetime import datetime
from array import array
import logging

class data_manager(object):
    ""
    def __init__(self):
        self._mongo_client = MongoClient(configuration.data.local_db.db)
        self._db = self._mongo_client.get_default_database()
        self._collection = self._db[configuration.data.local_db.collection]
        self._providers = array()
        
    "Registers a data provider with the data manager. THe data provider is a function that returns a dataset"
    def add_data_provider(self, fn):
        logging.debug('Registering data provider: %s', fn)
        self._providers.append(fn)
        
    "Evaluates each data provider function and stores the result"
    def query_providers(self):
        for provider in self._providers:
            logging.debug('Querying data provider: %s', provider)
            dataset = provider()
            logging.debug('Data provider %s returned %d points', provider, dataset.points.count)
            if dataset.points.count > 0:
                self.store(dataset)
        
    "Commits a single dataset to backend storage"
    def store(self, data = dataset()):
        self._collection.insert(data.serialize())