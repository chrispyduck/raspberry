import time, signal, logging, sys, threading
from blackberry.configuration.ConfigData import CurrentConfig
from blackberry.shared.Daemon import Daemon
from blackberry.components.PowerMonitor import PowerMonitor
from blackberry.components.Obd import Obd
from blackberry.data.DataCollector import DataCollector
from blackberry.components.Bluetooth import Bluetooth
from multiprocessing.synchronize import Event

SIGNALS_TO_NAMES_DICT = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

class Controller(Daemon):
    def __init__(self):
        super(Controller, self).__init__(CurrentConfig.args.pid)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info('Starting daemon controller')
        signal.signal(signal.SIGINT, self.OnSignal)
        signal.signal(signal.SIGTERM, self.OnSignal)
        signal.signal(signal.SIGHUP, self.OnSignal)
        self._lock = Event()
        self._powerStatus = False
        pass
    
    def OnSignal(self, sig, frame):
        if sig == signal.SIGINT or sig == signal.SIGTERM:
            self._logger.error('Received %s; exiting', SIGNALS_TO_NAMES_DICT[sig])
            self.reset()
            sys.exit(1)
            
        elif sig == signal.SIGHUP:
            self._logger.warn('Received %s; reloading configuration', SIGNALS_TO_NAMES_DICT[sig])
            CurrentConfig.reload()
    
    def StartWithArgs(self):
        if CurrentConfig.args.debug:
            self.run()
        else:
            self.start()        
        
    def reset(self):
        self._lock.set()
        if self._powerStatus:
            self.powerOff()
        self.power = None
        
    def run(self):
        self.power = PowerMonitor()
        self.power.startup += self.powerOn
        self.power.shutdown += self.powerOff
        
        self._logger.debug('lock wait started')
        while not self._lock.is_set():
            self._lock.wait(1)
            self._logger.debug('lock wait sleep')
        self._logger.debug('lock wait finished')
        
    def powerOn(self):
        "start all counters and attempt to gain internet access using bluetooth"
        self._
        self._powerStatus = True
        self.dataCollector = DataCollector()
        
        self.obd = Obd()
        self.dataCollector.registerDataProvider(self.obd)
        
        self.bluetooth = Bluetooth()
        self.bluetooth.connected += self.onNetConnected
        self.bluetooth.disconnected += self.onNetDisconnected
        
        self.dataCollector.start()
    
    def powerOff(self):
        self._powerStatus = False
        self.dataCollector.stop()
        self.dataCollector = None
        self.obd = None
        self.bluetooth = None
        pass
        
    def onNetConnected(self):
        "start a timer to periodically upload mongo data"
        pass
    
    def onNetDisconnected(self):
        "stop mongo timer"
        pass