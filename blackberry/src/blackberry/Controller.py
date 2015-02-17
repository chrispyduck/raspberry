import signal, logging
import blackberry.shared
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.Daemon import Daemon
from blackberry.components.PowerMonitor import PowerMonitor
from blackberry.components.Obd import Obd
from blackberry.data.DataCollector import DataCollector
from blackberry.components.Bluetooth import Bluetooth
import multiprocessing
from blackberry.data.DataStorage import DataStorage

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

class Controller(Daemon):
    def __init__(self):
        super(Controller, self).__init__(CurrentConfig.args.pid)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Starting daemon controller')
        self._lock = multiprocessing.Event()
        self._powerStatus = False
        pass        
        
    def run(self):
        self._logger.debug('Testing local MongoDB connectivity')
        dbTest = DataStorage(CurrentConfig.data.local_db)
        if not dbTest.isActive():
            self._logger.fatal('Unable to open communication with local MongoDB instance')
            return
        dbTest = None
        
        self._logger.debug('Initializing PowerMonitor')
        self.power = PowerMonitor()
        self.power.startup += self.powerOn
        self.power.shutdown += self.powerOff
        
        self._logger.debug('lock wait started')
        while not self._lock.is_set():
            self._lock.wait(1)
        self._logger.debug('lock wait finished')
        
    def powerOn(self):
        "start all counters and attempt to gain internet access using bluetooth"
        if self._powerStatus:
            self._logger.warn('Received powerOff event while power was on. Ignoring.')
            return
        
        self._powerStatus = True
        self.dataCollector = DataCollector()

        try:
            self.bluetooth = Bluetooth()
            self.bluetooth.connected += self.onNetConnected
            self.bluetooth.disconnected += self.onNetDisconnected
        except Exception as e:
            self._logger.error('Error initializing Bluetooth: %r', e)
        
        self.dataCollector.start()
    
    def powerOff(self):
        if not self._powerStatus:
            self._logger.warn('Received powerOff event while power was off. Ignoring.')
            return
        
        self._powerStatus = False
        if hasattr(self, 'dataCollector'):
            self.dataCollector.stop()
            self.dataCollector = None
        if hasattr(self, 'bluetooth'):
            self.bluetooth = None
        pass
        
    def onNetConnected(self):
        "start a timer to periodically upload mongo data"
        pass
    
    def onNetDisconnected(self):
        "stop mongo timer"
        pass