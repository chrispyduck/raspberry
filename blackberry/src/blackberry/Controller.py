import signal, logging, multiprocessing
import blackberry.shared
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.Daemon import Daemon
from blackberry.components.PowerMonitor import PowerMonitor
from blackberry.components.Obd import Obd
from blackberry.data.DataCollector import DataCollector
from blackberry.components.Bluetooth import Bluetooth
from blackberry.data.DataBackend import DataBackend
from blackberry.shared.Gpio import GpioSimpleOutput, GpioInputMonitor

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

class Controller(Daemon):
    def __init__(self):
        super(Controller, self).__init__(CurrentConfig.args.pid)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Starting daemon controller')
        self._lock = multiprocessing.Event()
        self._powerStatus = False
        self.vAcc = GpioInputMonitor("vAcc", CurrentConfig.gpio.vAcc, self.noop())
        self.vBatt = GpioInputMonitor("vBatt", CurrentConfig.gpio.vBatt, self.noop())
        self.CollectDataIndicator = GpioSimpleOutput("Collect Data Indicator", CurrentConfig.gpio.CollectDataIndicator, 0)
        self.vAccIndicator = GpioSimpleOutput("vAcc Indicator", CurrentConfig.gpio.vAccIndicator, 0)

    def noop(self, unused):
        pass

    def run(self):
        self._logger.debug('Initializing DataCollector')
        self.dataCollector = DataCollector()
        
        self._logger.debug('Starting main loop')
        lastvAcc = self.vAcc.value
        while not self._lock.is_set():
            vAccValue = self.vAcc.value
            if vAccValue != lastvAcc:
                if vAccValue:
                    self.powerOn()
                else:
                    self.powerOff()
                lastvAcc = vAccValue
            
            if vAccValue:
                self.CollectDataIndicator.value = 1
                self.dataCollector.collect()
                self.CollectDataIndicator.value = 0
                self._lock.wait(CurrentConfig.data.capture_interval)
            else:
                # no power - flash LEDs
                self.CollectDataIndicator.value = 1
                self.vAccIndicator.value = 1
                self._lock.wait(0.03)
                self.CollectDataIndicator.value = 0
                self.vAccIndicator.value = 0
                self._lock.wait(CurrentConfig.gpio.PowerOffToggleDelay)
                
        self._logger.debug('Exited main loop')
        
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