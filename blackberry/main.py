import blackberry.components
import blackberry.data  
import os, sys, logging

class Blackberry(object):
    def __init__(self):
        self.power = blackberry.components.PowerMonitor()
        self.power.startup += self.powerOn
        self.power.shutdown += self.powerOff
        
    def powerOn(self):
        "start all counters and attempt to gain internet access"
        self.dataCollector = blackberry.data.DataCollector()
        
        self.obd = blackberry.components.Obd()
        self.dataCollector.registerDataProvider(self.obd)
        
        self.bluetooth = blackberry.components.Bluetooth()
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

if __name__ == "__main__":
    logging.basicConfig(filename='raspberry.log', level=logging.DEBUG, format='%(asctime)s %(module)s.%(funcName)s %(levelname)s: %(message)s')
    logging.info('Starting blackberry!')
    
    instance = Blackberry()
        
    if os.fork():
        sys.exit()