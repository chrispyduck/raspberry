from blackberry.data import data
from blackberry.components import PowerMonitor
from blackberry.components import Bluetooth
import os, sys
import logging

if __name__ == "__main__":
    logging.basicConfig(filename='raspberry.log', level=logging.DEBUG, format='%(asctime)s %(name)s %(level)s: %(message)s')
    logging.info('Starting raspberry!')
    
    bluetooth = Bluetooth()
    
    power = PowerMonitor()
    power.startup += bluetooth.start
    power.shutdown += bluetooth.stop
    
    data_manager = blackberry.data.data.data_manager()
    data_manager.add_data_provider(power.get_dataset)
    data_manager.add_data_provider(bluetooth.get_dataset)
    
    if os.fork():
        sys.exit()