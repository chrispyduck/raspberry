import logging

class DataCollector(object):
    ""
    def __init__(self):
        self._providers = []
        
    "Registers a data provider with the data manager. THe data provider is a function that returns a DataSeries instance"
    def registerDataProvider(self, fn):
        logging.debug('Registering data provider: %s', fn)
        self._providers.append(fn)
        
    "Evaluates each data provider function and stores the result"
    def queryProviders(self):
        result = []
        
        for provider in self._providers:
            logging.debug('Querying data provider: %s', provider)
            series = provider()
            if series != None:
                logging.debug('Data provider %s returned %d points', provider, len(series.points))
                if len(series.points) > 0:
                    result.append(series)
                
        return result