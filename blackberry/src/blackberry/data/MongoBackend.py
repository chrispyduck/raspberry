from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.data.DataBackend import DataBackend
from blackberry.data.DataSeries import DataSeries
from pymongo import MongoClient
import logging
from pymongo.errors import AutoReconnect
from bson.objectid import ObjectId
from bson.timestamp import Timestamp

class MongoBackend(DataBackend):
    def __init__(self, configuration=CurrentConfig.data.local_db):
        super(MongoBackend, self).__init__(configuration)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Connecting to MongoDB instance at %s', configuration.db)
        self._mongo_client = MongoClient(configuration.db)
        self._currentTrip = None

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
        
    def commit(self, point):
        if not hasattr(self, '_currentTrip'):
            self._trip_start()

        point['ts'] = Timestamp()        
        self._trip_append(point)
    
    @safe_mongocall
    def _trip_start(self):
        self._currentTrip = ObjectId()
        trip = { "_id": self._currentTrip, "data": [] }
        self.collection.insert(trip)
    
    @safe_mongocall
    def _trip_append(self, datasetId):
        return self.trips.update({ "_id": self._currentTrip }, { "$push": { "data": datasetId }})
    
    def safe_mongocall(self, call):
        def _safe_mongocall(*args, **kwargs):
            tries = 0
            while tries < 5:
                try:
                    return call(*args, **kwargs)
                except AutoReconnect as ar:
                    self._logger.warn('Failed to transmit data to MongoDB: %r', ar)
                    tries += 1
        return _safe_mongocall