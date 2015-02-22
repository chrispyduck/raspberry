from blackberry.data.DataBackend import DataBackend
from blackberry.configuration.ConfigData import CurrentConfig
import logging

class TestBackend(DataBackend):
    def __init__(self, configuration=CurrentConfig.data.local_db):
        super(TestBackend, self).__init__(configuration)
        self.data = []
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def commit(self, point):
        self._logger.info('Recorded data point: ' + repr(point))
        self.data.append(point)