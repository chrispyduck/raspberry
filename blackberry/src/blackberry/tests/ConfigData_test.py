'''
Created on Feb 4, 2015

@author: CCarlson
'''
import unittest
import json
from blackberry.configuration.ConfigData import ConfigData


class ConfigData_tests(unittest.TestCase):

    
    def setUp(self):
        self.rawdata = json.loads("""
{
  "bluetooth": {
    "autodiscover": true,
    "pin": 1123,
    "tetheringDevices": [
      "2C:44:01:CF:73:FE"
    ]
  },
  "data": {
    "capture_interval": 0.3,
    "enabled_collectors": [
      "blackberry.components.TestDataCollector.TestDataCollector"
    ],
    "collector_configuration": {
      "Obd": {
          "sensors": [
              "RPM",
            "COOLANT_TEMP",
            "FUEL_STATUS"
          ],
          "baudrate": 38400,
          "port": "COM4"
      }
    },
    "storage_backend": "blackberry.data.MongoBackend.MongoBackend",
    "local_db": {
      "collection": "data",
      "db": "mongodb://blackberry:blackberry@localhost/blackberry"
    },
    "remote_db": {
      "collection": "raspberry",
      "db": "mongodb://user:pass@hostname:port/db"
    }
  },
  "gpio": {
    "vAcc": 50,
    "vBatt": 200,
    "vAccIndicator": 12,
    "CollectDataIndicator": 16
  }
}""")
        pass


    def tearDown(self):
        pass


    def test_loadConfig(self):
        self.config = ConfigData()
        self.config._init(self.rawdata)
        self.assertEqual(self.config.gpio.vAcc, 50)
        self.assertEqual(self.config.gpio.vBatt, 200)
        self.assertEqual(self.config.data.remote_db.collection, 'raspberry')
        self.assertEqual(self.config.data.local_db.collection, 'data')
        self.assertTrue(self.config.data.collector_configuration.__contains__('Obd'))
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ConfigurationTests.loadConfig']
    unittest.main()