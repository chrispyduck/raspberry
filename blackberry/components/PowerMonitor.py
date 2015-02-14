from __future__ import print_function
import logging, time, os.path
from blackberry.shared.EventHook import EventHook
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.GpioInputMonitor import GpioInputMonitor

class PowerMonitor(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug('PowerMonitor(): initializing')
        self.vAcc = GpioInputMonitor("vAcc", CurrentConfig.gpio.vAcc, self._vAcc_change)
        self.vBatt = GpioInputMonitor("vBatt", CurrentConfig.gpio.vBatt, self._vBatt_change)
        self.startup = EventHook()
        self.shutdown = EventHook()
        self._logger.debug('PowerMonitor(): initialization complete')
        self._vBatt_change(self.vBatt.value)
        self._vAcc_change(self.vAcc.value)        
        
    def _vAcc_change(self, value):
        self._logger.info('vAcc power %s', 'on' if value else 'off')
        self._activate() if value else self._deactivate()
    
    def _vBatt_change(self, value):
        self._logger.info('vBatt power %s', 'on' if value else 'off')
    
    def _activate(self):
        if os.path.isfile(CurrentConfig.paths.usb_power):
            self._logger.info('Activating USB hub power')
            print('0x1', file=CurrentConfig.paths.usb_power)
        time.sleep(5)
        self.startup.fire()
    
    def _deactivate(self):
        self.shutdown.fire()
        time.sleep(5)
        if os.path.isfile(CurrentConfig.paths.usb_power):
            self._logger.info('Deactivating USB hub power')
            print('0x0', file=CurrentConfig.paths.usb_power)
        time.sleep(5)