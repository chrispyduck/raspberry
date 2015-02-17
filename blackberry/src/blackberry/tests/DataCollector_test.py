'''
Created on Feb 4, 2015

@author: CCarlson
'''
import unittest
from blackberry.data.DataCollector import DataCollector
from blackberry.data.DataSeries import DataSeries
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.components.DataCollectorComponent import DataCollectorComponent
import blackberry.shared 

class Expected1(DataCollectorComponent):
    def GetData(self):
        series = DataSeries(source=10)
        series.add(1, 0.5)
        series.add(2, 0.2215)
        series.add(3, 33.452)
        return series

class Expected2(DataCollectorComponent):
    def GetData(self):
        series = DataSeries(source=11)
        series.add(1, 1.5)
        series.add(2, 1.2215)
        series.add(3, 23.452)
        return series
    
class Empty(DataCollectorComponent):
    def GetData(self):
        series = DataSeries(source=4)
        return series

class Null(DataCollectorComponent):
    def GetData(self):
        return None
            
class DataCollector_test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DataCollector_test, self).__init__(*args, **kwargs)
        CurrentConfig.data.storage_backend = 'blackberry.data.TestBackend.TestBackend'
        
    def test_expectedBehavior(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Expected1"
        ]
        collector = DataCollector()
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Expected1",
            "blackberry.tests.DataCollector_test.Expected2"
        ]
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 2)
        
    def test_emptyResultSet(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Empty"
        ]
        collector = DataCollector()
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._collectors), 1)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Expected1",
            "blackberry.tests.DataCollector_test.Empty"
        ]
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        self.assertEqual(len(collector._collectors), 2)
        
    def test_nullResultSet(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Null"
        ]
        collector = DataCollector()
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._collectors), 1)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Null",
            "blackberry.tests.DataCollector_test.Expected1"
        ]
        collector.init()
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        self.assertEqual(len(collector._collectors), 2)
        
    def test_timerCallback(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.components.TestDataCollector.TestDataCollector"
        ]
        collector = DataCollector()
        collector.init()
        data = collector.queryProviders()
        datadict = blackberry.shared.todict(data)
        print(datadict)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ConfigurationTests.loadConfig']
    unittest.main()