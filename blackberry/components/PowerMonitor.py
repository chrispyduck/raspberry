import logging
import time
from blackberry.shared import EventHook
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.GpioInputMonitor import GpioInputMonitor

class PowerMonitor(object):
    def __init__(self):
        logging.debug('power_manager(): initializing')
        CurrentConfig
        self.vAcc = GpioInputMonitor("vAcc", CurrentConfig.gpio.vAcc, self._vAcc_change)
        self.vBatt = GpioInputMonitor("vBatt", CurrentConfig.gpio.vBatt, self._vBatt_change)
        self.startup = EventHook()
        self.shutdown = EventHook()
        logging.debug('power_manager(): initialization complete')
        
    def _vAcc_change(self, value):
        logging.info('vAcc power %s', 'on' if value else 'off')
        self._activate() if value else self._deactivate()
    
    def _vBatt_change(self, value):
        logging.info('vBatt power %s', 'on' if value else 'off')
    
    def _activate(self):
        logging.info('Activating USB hub power')
        print('0x1', file=CurrentConfig.paths.usb_power)
        time.sleep(5)
        self.startup.fire()
    
    def _deactivate(self):
        self.shutdown.fire()
        time.sleep(5)
        logging.info('Deactivating USB hub power')
        print('0x0', file=CurrentConfig.paths.usb_power)
        time.sleep(5)
        
    def get_dataset(self):
        #dataset = data.dataset()
        #dataset.add_point