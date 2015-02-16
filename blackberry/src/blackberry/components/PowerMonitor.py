from __future__ import print_function
import logging, time, os.path, signal
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
        self._vBatt_change(self.vBatt.value)
        self._vAcc_change(self.vAcc.value)
        
        signal.signal(signal.SIGUSR1, self.OnSignal)
        signal.signal(signal.SIGUSR2, self.OnSignal)
        
        self._logger.debug('PowerMonitor(): initialization complete')        
        
    def OnSignal(self, sig, frame):
        if sig == signal.SIGUSR1:
            self._logger.warn('Manually activating due to SIGUSR1')
            self._activate()
        elif sig == signal.SIGUSR2:
            self._logger.warn('Manually deactivating due to SIGUSR2')
            self._deactivate()
        
    def _vAcc_change(self, value):
        self._logger.info('vAcc power %s', 'on' if value else 'off')
        self._activate() if value else self._deactivate()
    
    def _vBatt_change(self, value):
        self._logger.info('vBatt power %s', 'on' if value else 'off')
    
    def _activate(self):
        if os.path.isfile(CurrentConfig.paths.usb_power):
            self._logger.info('Activating USB hub power')
            with open(CurrentConfig.paths.usb_power, 'w') as powerfile:
                print('0x1', file=powerfile)
        time.sleep(5)
        self.startup.fire()
    
    def _deactivate(self):
        self.shutdown.fire()
        time.sleep(5)
        if os.path.isfile(CurrentConfig.paths.usb_power):
            self._logger.info('Deactivating USB hub power')
            with open(CurrentConfig.paths.usb_power, 'w') as powerfile:
                print('0x0', file=powerfile)
        time.sleep(5)