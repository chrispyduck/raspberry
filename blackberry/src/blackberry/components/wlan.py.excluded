from enum import Enum
import logging

class wlan_mode(Enum):
    Unconfigured = 0
    Client = 1
    AP = 2

class wlan:
    def __init__(self):
        self.mode = wlan_mode.Unconfigured
        logging.info('...')
        
    def set_mode(self, mode=wlan_mode.Unconfigured):
        