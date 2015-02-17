import signal, logging
import blackberry.shared
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.Daemon import Daemon
from blackberry.components.PowerMonitor import PowerMonitor
from blackberry.components.Obd import Obd
from blackberry.data.DataCollector import DataCollector
from blackberry.components.Bluetooth import Bluetooth
import multiprocessing
from blackberry.data.DataBackend import DataBackend
from blackberry.shared.Gpio import GpioSimpleOutput

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

class Controller(Daemon):
    def __init__(self):
        super(Controller, self).__init__(CurrentConfig.args.pid)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Starting daemon controller')
        self._lock = multiprocessing.Event()
        self._powerStatus = False
        self.CollectDataIndicator = GpioSimpleOutput("Collect Data Indicator", CurrentConfig.gpio.CollectDataIndicator, 0)
        self.vAccIndicator = GpioSimpleOutput("vAcc Indicator", CurrentConfig.gpio.vAccIndicator, 0)
        pass        
        
    def OnBeforeCollection(self):
        self.CollectDataIndicator.value = 1
        
    def OnAfterCollection(self):
        self.CollectDataIndicator.value = 0
        
    def run(self):
        self._logger.debug('Testing local data connectivity')
        dbTest = DataBackend.GetConfiguredBackend()
        if not dbTest.isActive:
            self._logger.fatal('Unable to open communication with local MongoDB instance')
            return
        dbTest = None
        
        self._logger.debug('Initializing PowerMonitor')
        self.power = PowerMonitor()
        self.power.startup += self.powerOn
        self.power.shutdown += self.powerOff

        self._logger.debug('Initializing DataCollector')
        self.dataCollector = DataCollector()
        
        self._logger.debug('Starting main loop')
        while not self._lock.is_set():
            if self._powerStatus:
                self.dataCollector.collect()
                self._lock.wait(CurrentConfig.data.capture_interval)
            else:
                # no power - flash LEDs
                self.CollectDataIndicator.value = 1
                self.vAccIndicator.value = 1
                self._lock.wait(0.03)
                self.CollectDataIndicator.value = 0
                self.vAccIndicator.value = 0
                self._lock.wait(CurrentConfig.gpio.PowerOffToggleDelay)
                
        self._logger.debug('lock wait finished')
        
    def powerOn(self):
        "start all counters and attempt to gain internet access using bluetooth"
        if self._powerStatus:
            self._logger.warn('Received powerOff event while power was on. Ignoring.')
            return
        
        self.vAccIndicator.value = 1
        
        self.dataCollector.init()
        self._powerStatus = True
        
        try:
            self.bluetooth = Bluetooth()
            self.bluetooth.connected += self.onNetConnected
            self.bluetooth.disconnected += self.onNetDisconnected
        except Exception as e:
            self._logger.error('Error initializing Bluetooth: %r', e)        
    
    def powerOff(self):
        if not self._powerStatus:
            self._logger.warn('Received powerOff event while power was off. Ignoring.')
            return
        
        self._powerStatus = False
        
        if hasattr(self, 'bluetooth'):
            self.bluetooth = None
        
        self.CollectDataIndicator.value = 0
        self.vAccIndicator.value = 0
        
    def onNetConnected(self):
        "start a timer to periodically upload mongo data"
        pass
    
    def onNetDisconnected(self):
        "stop mongo timer"
        pass