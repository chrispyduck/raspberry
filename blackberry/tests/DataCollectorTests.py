'''
Created on Feb 4, 2015

@author: CCarlson
'''
import unittest
from blackberry.data.DataCollector import DataCollector
from blackberry.data.DataSeries import DataSeries
from blackberry.tests.DataCollectorStub import DataCollectorStub

class DataCollectorTests(unittest.TestCase):

    def fn_expectedBehavior(self):
        series = DataSeries(source=10)
        series.addPoint(1, 0.5)
        series.addPoint(2, 0.2215)
        series.addPoint(3, 33.452)
        return series
    
    def fn_expectedBehavior2(self):
        series = DataSeries(source=11)
        series.addPoint(1, 1.5)
        series.addPoint(2, 1.2215)
        series.addPoint(3, 23.452)
        return series
        
    def test_expectedBehavior(self):
        collector = DataCollector()
        collector.registerDataProvider(DataCollectorStub(self.fn_expectedBehavior))
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        
        collector.registerDataProvider(DataCollectorStub(self.fn_expectedBehavior2))
        result = collector.queryProviders()
        self.assertEqual(len(result), 2)
        
    def fn_emptyResultSet(self):
        series = DataSeries(source=4)
        return series
        
    def test_emptyResultSet(self):
        collector = DataCollector()
        collector.registerDataProvider(DataCollectorStub(self.fn_emptyResultSet))
        result = collector.queryProviders()
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._providers), 1)
        
        collector.registerDataProvider(DataCollectorStub(self.fn_expectedBehavior))
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        self.assertEqual(len(collector._providers), 2)
        
    def fn_nullResultSet(self):
        return None
    
    def test_nullResultSet(self):
        collector = DataCollector()
        collector.registerDataProvider(DataCollectorStub(self.fn_nullResultSet))
        result = collector.queryProviders()
        self.assertEqual(len(result), 0)
        self.assertEqual(len(collector._providers), 1)
        
        collector.registerDataProvider(DataCollectorStub(self.fn_expectedBehavior))
        result = collector.queryProviders()
        self.assertEqual(len(result), 1)
        self.assertEqual(len(collector._providers), 2)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ConfigurationTests.loadConfig']
    unittest.main()