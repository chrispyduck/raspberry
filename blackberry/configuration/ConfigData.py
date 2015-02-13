from blackberry.configuration._ConfigPaths import _ConfigPaths
from blackberry.configuration._ConfigGpio import _ConfigGpio
from blackberry.configuration._ConfigBluetooth import _ConfigBluetooth
from blackberry.configuration._ConfigData import _ConfigData
import logging, json, argparse

class ConfigData(object):

    def __init__(self, **entries): 
        self.gpio = _ConfigGpio()
        self.paths = _ConfigPaths()
        self.bluetooth = _ConfigBluetooth()
        self.data = _ConfigData()
        
        self._parser = argparse.ArgumentParser(description='Raspberry Pi-based Vehicle Black Box')
        self._parser.add_argument('-d', '--debug', help='enable debug mode and do not fork', action='store_true')
        self._parser.add_argument('-c', '--config', help='path to configuration file', default='config.json')
        self._parser.add_argument('-l', '--log', help='path to log file', default='raspberry.log')
        self._parser.add_argument('-p', '--pid', help='path to pid file', default='raspberry.pid')
        
    def parseArgs(self):
        self.args = self._parser.parse_args()
        self.init(self.args.config)
        
    def init(self, configFile = "config.json"):
        # load raw data from file
        logging.info('Loading configuration from file: %s', configFile)
        with open(configFile) as fd:
            rawdata = json.load(fd)
        self._init(rawdata)
            
    def _init(self, rawdata):
        for key in rawdata:
            if key in self.__dict__:
                logging.debug('Loading config data for: %s', key)
                self.__dict__[key].load(rawdata[key])
            else:
                logging.warning('Found unknown config entry: %s', key)

CurrentConfig = ConfigData()