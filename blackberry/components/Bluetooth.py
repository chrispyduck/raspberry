from subprocess import call
import psutil
import dbus  
import logging
from blackberry.shared import EventHook
from blackberry.configuration.ConfigData import CurrentConfig

class Bluetooth(object):
    def __init__(self):
        logging.debug('bluetooth_manager(): initializing')
        self._device_path = '/org/bluez/hci0/dev_' + CurrentConfig.bluetooth.mac.replace(':', '_')
        self._sysbus = dbus.SystemBus()
        self._bluez_network = self._sysbus.get_object('org.bluez.Network1', self._device_path)
        self._bluez_device = self._sysbus.get_object('org.bluez.Device1', self._device_path)
        self.phone_connected = False
        self.internet_connected = False
        self.started = EventHook()
        self.start_failed = EventHook()
        self.stopped = EventHook()
        logging.debug('bluetooth_manager(): initialization complete')
        
    def start(self):
        self._connect_phone()
        self.started.fire()
        
    def stop(self):
        if self.phone_connected:
            self._disconnect_phone()
        self.stopped.fire()
    
    def _connect_phone(self):
        logging.debug('Starting pulseaudio daemon')
        call(["sudo", "-u pulse pulseaudio -D --start"])
        
        logging.debug('Connecting to phone using bluetooth')
        try:
            self._bluez_device.connect()
            self.phone_connected = True
        except dbus.exceptions.DBusException:
            self.phone_connected = False
            raise
        
        logging.debug('Starting bluetooth tethering')
        try:
            self._bluez_network.connect('nap')
        except dbus.exceptions.DBusException:
            raise
        
        logging.debug('Starting dhcpcd on bnep0')
        ret = call(['dhcpcd', '-t 10 bnep0'])
        if ret == 1:
            logging.warn('Unable to obtain IP address from bluetooth adapter')
            self.internet_connected = False
        else:
            logging.info('Internet connection established')
            self.internet_connected = True
        
    def _disconnect_phone(self):
        if self.internet_connected:
            call(['ifconfig', 'bnep0 down'])
        
        logging.debug('Disconnecting phone')
        self._bluez_device.disconnect()
    
        for proc in psutil.process_iter():
            if proc.name == 'pulseaudio':
                logging.debug('Stopping pulseaudio daemon on pid %d', proc.pid)
                proc.kill()
                pass
        logging.warn('Could not find plseaudio instance to stop')
                
                
#dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_2C_44_01_CF_73_FE org.bluez.Network1.Connect string:'nap'