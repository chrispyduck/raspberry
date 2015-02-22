import random
from blackberry.components.DataCollectorComponent import DataCollectorComponent

class TestDataCollector(DataCollectorComponent):
    def GetData(self):
        for i in range(1,10):
            yield { 'key': i, 'value': random.randint(1, 255) }