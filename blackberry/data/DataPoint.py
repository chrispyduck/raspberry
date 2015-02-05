from datetime import datetime 

class DataPoint(object):
    """describes the value of a single counter from a given data source
    
    counter = the specific counter tracked by the module
    value = the raw value of the counter
    """
    def __init__(self, counter, value):
        self.timestamp = datetime.now().isoformat()
        self.counter = counter
        self.value = value