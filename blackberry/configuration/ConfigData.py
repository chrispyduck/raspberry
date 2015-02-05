from blackberry.configuration._ConfigPaths import _ConfigPaths
from blackberry.configuration._ConfigGpio import _ConfigGpio
from blackberry.configuration._ConfigBluetooth import _ConfigBluetooth
from blackberry.configuration._ConfigData import _ConfigData
import logging, json

class ConfigData(object):

    def __init__(self, **entries): 
        self.gpio = _ConfigGpio()
        self.paths = _ConfigPaths()
        self.bluetooth = _ConfigBluetooth()
        self.data = _ConfigData()
    
    def init(self, configFile = "config.json"):
        # load raw data from file
        logging.info('Loading configuration from file: %s', configFile)
        with open(configFile) as file:
            rawdata = json.load(file)
        self._init(rawdata)
            
    def _init(self, rawdata):
        for key in rawdata:
            if key in self.__dict__:
                logging.debug('Loading config data for: %s', key)
                self.__dict__[key].load(rawdata[key])
            else:
                logging.warning('Found unknown config entry: %s', key)

CurrentConfig = ConfigData()