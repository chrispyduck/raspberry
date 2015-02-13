import logging
from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.shared.Timer import Timer
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.data.DataStorage import DataStorage

class DataCollector(object):
    ""
    def __init__(self):
        self._providers = []
        self._timer = Timer(CurrentConfig.data.capture_interval, self._timerCallback)
        self._storage = DataStorage()
        
    def start(self):
        logging.info('Starting data collector timer')
        self._timer.start()
        
    def stop(self):
        logging.info('Stopping data collector timer')
        self._timer.stop()
        
    def registerDataProvider(self, instance=DataCollectorComponent()):
        "Registers a data provider with the data manager. THe data provider is a function that returns a DataSeries instance"
        logging.debug('Registering data provider: %s', instance.__class__.__name__)
        self._providers.append(instance)
        
    def queryProviders(self):
        "Evaluates each data provider function and stores the result"
        result = []
        
        for provider in self._providers:
            logging.debug('Querying data provider: %s', provider)
            series = provider.GetData()
            if series != None:
                logging.debug('Data provider %s returned %d points', provider, len(series.points))
                if len(series.points) > 0:
                    result.append(series)
                
        return result
    
    def _timerCallback(self):
        data = self.queryProviders()
        self._storage.commit(data)