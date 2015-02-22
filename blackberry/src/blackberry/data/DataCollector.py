import logging
import blackberry.shared
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.data.DataBackend import DataBackend

class DataCollector(object):
    ""
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._collectors = []
        self._storage = DataBackend.GetConfiguredBackend() 
        
    def init(self):
        self._collectors = []
        for name in CurrentConfig.data.enabled_collectors:
            self._logger.info('Configuring data collector "%s"', name)
            try:
                collector = blackberry.shared.getClassInstanceFromName(name)
                self._collectors.append(collector)
            except Exception as e:
                self._logger.error('Failed to initialize data collector "%s": %r', name, e)
        
    def queryProviders(self):
        "Evaluates each data provider function and stores the result"
        for collector in self._collectors:
            points = collector.GetData()
            if points:
                for point in points:
                    if point:
                        yield point
                    
    def collect(self):
        for point in self.queryProviders():
            self._storage.commit(point)