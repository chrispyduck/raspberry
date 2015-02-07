from subprocess import call
import psutil
import dbus  
import logging
from blackberry.shared import EventHook
from blackberry.configuration.ConfigData import CurrentConfig

class Bluetooth(object):
    def __init__(self):
        logging.debug('bluetooth_manager(): initializing')
        self._sysbus = dbus.SystemBus()
        self._devices = {}
        self._adapters = {}
        
        self._sysbus.add_signal_receiver(self._interfacesAdded,
            dbus_interface = "org.freedesktop.DBus.ObjectManager",
            signal_name = "InterfacesAdded")

        self._sysbus.add_signal_receiver(self._interfacesRemoved,
            dbus_interface = "org.freedesktop.DBus.ObjectManager",
            signal_name = "InterfacesRemoved")
    
        self._sysbus.add_signal_receiver(self._propertiesChanged,
            dbus_interface = "org.freedesktop.DBus.Properties",
            signal_name = "PropertiesChanged",
            arg0 = "org.bluez.Device1",
            path_keyword = "path")
    
        self._sysbus.add_signal_receiver(self._adapterPropertyChanged,
            dbus_interface = "org.bluez.Adapter1",
            signal_name = "PropertyChanged")
        
        bluez_root = self._sysbus.get_object('org.bluez', '/')
        om = dbus.Interface(bluez_root, 'org.freedesktop.DBus.ObjectManager')
        objects = om.GetManagedObjects()
        for path in objects:
            interfaces = objects[path]
            self._interfacesAdded(path, interfaces)
            if 'org.bluez.Adapter1' in interfaces:
                logging.info('Found adapter: %s', path)
                self._adapters[path] = interfaces
            elif 'org.bluez.Device1' in interfaces:
                logging.info('Found device: %s', path)
                self._devices[path] = interfaces
        
        for path in self._adapters:
            adapter = dbus.Interface(self._sysbus.get_object('org.bluez', path), 'org.bluez.Adapter1')
            adapter.StartDiscovery()
        
    def _interfacesAdded(self, path, interfaces):
        logging.debug("Interfaces added at %s: %r", path, interfaces)

        if 'org.bluez.Device1' in interfaces:
            collection = self._devices
            properties = interfaces['org.bluez.Device1']
            iftpye = 'device'
        elif 'org.bluez.Adapter1' in interfaces:
            collection = self._adapters
            properties = interfaces['org.bluez.Adapter1']
            iftpye = 'adapter'
        else:
            return
        
        if path in collection:
            collection[path] = dict(collection[path].items() + properties.items())
        else:
            collection[path] = properties

        if iftpye == 'device':
            if "Address" in collection[path]:
                address = properties["Address"]
            else:
                address = "<unknown>"
            self._logDevice(address, collection[path])
        
    def _interfacesRemoved(self, path, interfaces):
        if 'org.bluez.Device1' in interfaces:
            logging.warn('Device %s removed', path)
            self._devices.pop(path)
        elif 'org.bluez.Adapter1' in interfaces:
            logging.warn('Adapter %s removed', path)
            self._adapters.pop(path)
        logging.warn("Interface removed at %s: %r", path, interfaces)
        
    def _propertiesChanged(self, interface, changed, invalidated, path):
        if interface != "org.bluez.Device1":
            return
    
        if path in self._devices:
            self.devices[path] = dict(self.devices[path].items() + changed.items())
        else:
            self.devices[path] = changed
            
        if "Address" in self.devices[path]:
            address = self.devices[path]["Address"]
        else:
            address = "<unknown>"
    
        self._logDevice(address, self.devices[path])
        
    def _adapterPropertyChanged(self, name, value):
        logging.debug("Adapter property '%s' changed to '%s'", name, value)
    
    def _logDevice(self, address, properties):
        #if 'Logged' in properties:
        #    return
        logging.debug("Device " + address + " :")

        for key in properties.keys():
            value = properties[key]
            if type(value) is dbus.String:
                value = unicode(value).encode('ascii', 'replace')
            if (key == "Class"):
                logging.debug("    %s = 0x%06x" % (key, value))
            else:
                logging.debug("    %s = %s" % (key, value))
    
        properties["Logged"] = True
    
    def oldinit(self):
        self._device_path = '/org/bluez/' + CurrentConfig.bluetooth.adapter #/dev_' + CurrentConfig.bluetooth.mac.replace(':', '_')
        self._bluez_network = dbus.Interface(self._bluez_device_root, 'org.bluez.Network1')
        self._bluez_ = dbus.Interface(self._bluez_device_root, 'org.bluez.Device1')
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
            self._bluez_device.Connect()
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