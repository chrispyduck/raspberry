import time
from blackberry.shared.Daemon import Daemon
from blackberry.components.PowerMonitor import PowerMonitor
from blackberry.components.Obd import Obd
from blackberry.data.DataCollector import DataCollector
from blackberry.components.Bluetooth import Bluetooth

class Controller(Daemon):
    def __init__(self):
        pass
        
    def run(self):
        self.power = PowerMonitor()
        self.power.startup += self.powerOn
        self.power.shutdown += self.powerOff
        
        while True:
            time.sleep(1)        
        
    def powerOn(self):
        "start all counters and attempt to gain internet access"
        self.dataCollector = DataCollector()
        
        self.obd = Obd()
        self.dataCollector.registerDataProvider(self.obd)
        
        self.bluetooth = Bluetooth()
        self.bluetooth.connected += self.onNetConnected
        self.bluetooth.disconnected += self.onNetDisconnected
        
        self.dataCollector.start()
    
    def powerOff(self):
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