from __future__ import print_function
from blackberry.configuration._ConfigGpio import _ConfigGpio
from blackberry.configuration._ConfigBluetooth import _ConfigBluetooth
from blackberry.configuration._ConfigData import _ConfigData
import logging, json, argparse
import blackberry.shared

class ConfigData(object):

    def __init__(self): 
        self._logger = logging.getLogger(self.__class__.__name__)
        self.gpio = _ConfigGpio()
        self.bluetooth = _ConfigBluetooth()
        self.data = _ConfigData()
        
        self._parser = argparse.ArgumentParser(description='Raspberry Pi-based Vehicle Black Box')
        self._parser.add_argument('-d', '--debug', help='enable debug mode and do not fork', action='store_true')
        self._parser.add_argument('-c', '--config', help='path to configuration file', default='config.json')
        self._parser.add_argument('-l', '--log', help='path to log file', default='/tmp/raspberry.log')
        self._parser.add_argument('-p', '--pid', help='path to pid file', default='/tmp/raspberry.pid')
        self._parser.add_argument('-wc', '--writeconfig', help=argparse.SUPPRESS)
        
    def reload(self):
        self._logger.info('Reloading configuration from %s', self.args.config)
        self.init(self.args.config)
        
    def parseArgs(self):
        self.args = self._parser.parse_args()
        self.init(self.args.config)
        
    def init(self, configFile = "config.json"):
        # load raw data from file
        self._logger.info('Loading configuration from file: %s', configFile)
        with open(configFile) as fd:
            rawdata = json.load(fd)
        self._init(rawdata)
            
    def _init(self, rawdata):
        for key in rawdata:
            if key in self.__dict__:
                self._logger.debug('Loading config data for: %s', key)
                self.__dict__[key].load(rawdata[key])
            else:
                self._logger.warning('Found unknown config entry: %s', key)
                
    def save(self, configFile = "config.json"):
        data = blackberry.shared.todict(self)
        datastr = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))
        with open(configFile, 'w') as cf:
            print(datastr, file=cf)
        self._logger.info('Saved configuration to file %s', configFile)

CurrentConfig = ConfigData()