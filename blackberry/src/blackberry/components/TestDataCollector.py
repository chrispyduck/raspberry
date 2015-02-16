import random
from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.data.DataSeries import DataSeries

class TestDataCollector(DataCollectorComponent):
    def GetData(self):
        ds = DataSeries('TestDataCollector')
        for i in range(1,10):
            ds.add(i, random.randint(1, 255))
        return ds