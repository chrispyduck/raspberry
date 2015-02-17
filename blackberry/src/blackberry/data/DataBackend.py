from blackberry.configuration.ConfigData import CurrentConfig
import blackberry.shared

class DataBackend(object):
    def __init__(self, configuration=CurrentConfig.data.local_db):
        self._configuration = configuration
        
    def commit(self, dataSeries):
        raise Exception("Not implemented")
    
    @property
    def isActive(self):
        raise Exception("Not implemented")
    
    @property
    def configuration(self):
        return self._configuration
    
    @configuration.setter
    def configuration(self, value):
        self._configuration = value
        
    @staticmethod
    def GetConfiguredBackend():
        backname = CurrentConfig.data.storage_backend
        return blackberry.shared.getClassInstanceFromName(backname)