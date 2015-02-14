import logging
from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.shared.Timer import Timer
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.data.DataStorage import DataStorage
import blackberry.shared

class DataCollector(object):
    ""
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._collectors = []
        self._timer = Timer(CurrentConfig.data.capture_interval, self._timerCallback)
        self._storage = DataStorage()
        
    def start(self):
        for name in CurrentConfig.data.enabled_collectors:
            self._logger.info('Configuring data collector "%s"', name)
            try:
                collector = blackberry.shared.getClassInstanceFromName(name)
                self._collectors.append(collector)
            except Exception as e:
                self._logger.error('Failed to initialize data collector "%s": %r', name, e)
                            
        self._logger.info('Starting data collector timer')
        self._timer.start()
        
    def stop(self):
        self._collectors = []        
        self._logger.info('Stopping data collector timer')
        self._timer.stop()
        
    def queryProviders(self):
        "Evaluates each data provider function and stores the result"
        result = []
        
        for collector in self._collectors:
            self._logger.debug('Querying data collector: %s', collector.__class__.__name__)
            series = collector.GetData()
            if series != None:
                self._logger.debug('Data provider %s returned %d points', collector.__class__.__name__, len(series.points))
                if len(series.points) > 0:
                    result.append(series)
                
        return result
    
    def _timerCallback(self):
        data = self.queryProviders()
        datadict = blackberry.shared.todict(data)
        self._storage.commit(datadict)