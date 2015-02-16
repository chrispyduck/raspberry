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
    "gpio": {
        "vAcc": 50,
        "vBatt": 200
    },
    "paths": {
        "usb_power": "/sys/devices/platform/bcm2708_usb/buspower"
    },
    "bluetooth": {
        "tetheringDevices": ["2C:44:01:CF:73:FE"]
    },
    "data": {
        "remote_db": {
            "db": "mongodb://user:pass@sdkjf:41561/blackbox",
            "collection": "remote"
        },
        "local_db": {
            "db": "mongodb://localhost.../blackbox",
            "collection": "local"
        }
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
        self.assertEqual(self.config.data.remote_db.collection, 'remote')
        self.assertEqual(self.config.data.local_db.collection, 'local')
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'ConfigurationTests.loadConfig']
    unittest.main()