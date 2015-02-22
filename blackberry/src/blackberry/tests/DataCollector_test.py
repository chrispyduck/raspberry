'''
Created on Feb 4, 2015

@author: CCarlson
'''
import unittest
from blackberry.data.DataCollector import DataCollector
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.components.DataCollectorComponent import DataCollectorComponent
import blackberry.shared 

class Expected1(DataCollectorComponent):
    def GetData(self):
        yield { 'src': 'Expected1', 'key': 1, 'value': 0.5 }
        yield { 'src': 'Expected1', 'key': 2, 'value': 0.2215 }
        yield { 'src': 'Expected1', 'key': 3, 'value': 33.452 }

class Expected2(DataCollectorComponent):
    def GetData(self):
        yield { 'src': 'Expected1', 'key': 1, 'value': 1.5 }
        yield { 'src': 'Expected1', 'key': 2, 'value': 1.2215 }
        yield { 'src': 'Expected1', 'key': 3, 'value': 23.452 }
    
class Empty(DataCollectorComponent):
    def GetData(self):
        pass

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
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 3)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Expected1",
            "blackberry.tests.DataCollector_test.Expected2"
        ]
        collector.init()
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 6)
        
    def test_emptyResultSet(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Empty"
        ]
        collector = DataCollector()
        collector.init()
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._collectors), 1)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Expected1",
            "blackberry.tests.DataCollector_test.Empty"
        ]
        collector.init()
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 3)
        self.assertEqual(len(collector._collectors), 2)
        
    def test_nullResultSet(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Null"
        ]
        collector = DataCollector()
        collector.init()
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._collectors), 1)
        
        CurrentConfig.data.enabled_collectors = [
            "blackberry.tests.DataCollector_test.Null",
            "blackberry.tests.DataCollector_test.Expected1"
        ]
        collector.init()
        result = list(collector.queryProviders())
        self.assertEqual(len(result), 3)
        self.assertEqual(len(collector._collectors), 2)
        
    def test_timerCallback(self):
        CurrentConfig.data.enabled_collectors = [
            "blackberry.components.TestDataCollector.TestDataCollector"
        ]
        collector = DataCollector()
        collector.init()
        data = list(collector.queryProviders())
        datadict = blackberry.shared.todict(data)
        print(datadict)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ConfigurationTests.loadConfig']
    unittest.main()