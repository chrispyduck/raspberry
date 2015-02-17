import unittest
from blackberry.data.DataCollector import DataCollector
from blackberry.components.TestDataCollector import TestDataCollector
from blackberry.shared import todict

class DataCollector_test(unittest.TestCase):
    def test_serialization(self):
        coll = TestDataCollector()
        series = [coll.GetData()]
        result = todict(series)
        print(result)