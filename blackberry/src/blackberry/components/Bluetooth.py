from subprocess import call
import logging
import dbus  
import dbus.mainloop.glib
from blackberry.shared.EventHook import EventHook
from blackberry.configuration.ConfigData import CurrentConfig

class Bluetooth(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.debug('bluetooth_manager(): initializing')
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self._sysbus = dbus.SystemBus()
        self._devices = {}
        self._adapters = {}
        
        self.connected = EventHook()
        """Arguments: devicesConnected, networkInterface"""
        self.disconnected = EventHook()
        
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
        
        self.refreshData()
        
        for path in self._adapters:
            adapter = dbus.Interface(self._sysbus.get_object('org.bluez', path), 'org.bluez.Adapter1')
            adapter.StartDiscovery()
        
        self._logger.debug('bluetooth_manager(): initialization complete')
        
    def refreshData(self):
        bluez_root = self._sysbus.get_object('org.bluez', '/')
        om = dbus.Interface(bluez_root, 'org.freedesktop.DBus.ObjectManager')
        objects = om.GetManagedObjects()
        for path in objects:
            interfaces = objects[path]
            self._interfacesAdded(path, interfaces)
            if 'org.bluez.Adapter1' in interfaces:
                self._logger.info('Found adapter: %s', path)
                self._adapters[path] = interfaces
            elif 'org.bluez.Device1' in interfaces:
                self._logDevice(interfaces['org.bluez.Device1'])
                self._devices[path] = interfaces
                
    def _getInterfaces(self, d):
        interfaces = []
        for k in d:
            interfaces.append(k)
        return interfaces
        
    def _interfacesAdded(self, path, interfaces):
        self._logger.debug("Interfaces added at %s\n\%s", path, "\n\t".join(self._getInterfaces(interfaces)))

        if 'org.bluez.Device1' in interfaces:
            collection = self._devices
            properties = interfaces['org.bluez.Device1']
            if path in collection:
                collection[path] = dict(collection[path].items() + properties.items())
            else:
                collection[path] = properties
            self._logDevice(collection[path])
            
        elif 'org.bluez.Adapter1' in interfaces:
            collection = self._adapters
            properties = interfaces['org.bluez.Adapter1']
        
    def _interfacesRemoved(self, path, interfaces):
        if 'org.bluez.Device1' in interfaces:
            self._logger.warn('Device %s removed', path)
            self._devices.pop(path)
        elif 'org.bluez.Adapter1' in interfaces:
            self._logger.warn('Adapter %s removed', path)
            self._adapters.pop(path)
        else:
            self._logger.warn("Interface removed at %s: \n\t%s", path, "\n\t".join(self._getInterfaces(interfaces)))
        
    def _propertiesChanged(self, interface, changed, invalidated, path):
        if interface != "org.bluez.Device1":
            return
    
        if path in self._devices:
            self.devices[path] = dict(self.devices[path].items() + changed.items())
        else:
            self.devices[path] = changed
    
        self._logDevice(self.devices[path])
        
    def _adapterPropertyChanged(self, name, value):
        self._logger.debug("Adapter property '%s' changed to '%s'", name, value)
    
    def _logDevice(self, properties, isUpdate=False):
        self._logger.info('%s device %s: %s (%s, %s)',
                          'Found' if not isUpdate else 'Updated',
                          properties['Address'],
                          properties['Name'],
                          'Paired' if properties['Paired'] == 1 else 'Not paired',
                          'Connected' if properties['Connected'] == 1 else 'Not connected')

    def connectDevices(self, activateTethering=True):
        connected = []
        tetheringDevice = None
        for path in self._devices:
            self._logger.debug('Attempting to connect to device %s', path)
            try:
                dev = self._sysbus.get_object('org.bluez', path)
                devif = dbus.Interface(dev, 'org.bluez.Device1')
                devif.Connect()
                connected.append(path)
            except dbus.exceptions.DBusException as dbe:
                self._logger.warn('Unable to connect to device %s: %s', path, dbe)
        
        if activateTethering:
            tetheringDevice = self.startTethering()
        
        self.refreshData()        
        self.connected.fire(connected, tetheringDevice)
        
    def disconnectDevices(self):
        for path in self._devices:
            if self._devices[path]['org.bluez.Device1']['Connected'] == False:
                continue
            
            self._logger.info('Attempting to disconnect from device %s', path)
            try:
                obj = self._sysbus.get_object('org.bluez', path)
                dbus.Interface(obj, 'org.bluez.Device1').Disconnect()
            except dbus.exceptions.DBusException as dbe:
                self._logger.warn('Unable to disconnect from device %s: %s', path, dbe)
        
        self.refreshData()
        self.disconnected.fire()
        
    def start(self):
        self.connectDevices()
        self.started.fire()
        
    def stop(self):
        self.disconnectDevices()
        self.stopped.fire()
    
    def _getDefaultAdapterPath(self):
        "Returns the path to the first available Bluetooth adapter"
        for path in self._adapters:
            return path
    
    def startTethering(self):
        "Attempts to establish tethering with the first available preferred device"
        self._logger.debug('Starting bluetooth tethering')
        interface = None
        for device in CurrentConfig.bluetooth.tetheringDevices:
            try:
                devicePath = '%s/dev_%s'.format(
                    self._getDefaultAdapterPath(),
                     device.replace(':', '_')
                     )
                if self._devices[devicePath]['org.bluez.Device1']['Connected'] == False:
                    self._logger.info('Preferred tethering device %s is not connected. Skipping.', device)
                    continue
                
                dev = self._sysbus.get_object('org.bluez', devicePath)
                netif = dbus.Interface(dev, 'org.bluez.Network1')
                interface = netif.Connect('nap')
                break
            except dbus.exceptions.DBusException as dbe:
                self._logger.warn('Unable to begin tethering with %s: %s', device, dbe)
                raise
            
        if interface:
            self._logger.info('Starting dhcpcd on %s', netif)
            ret = call(['dhcpcd', '-t 10 {0}'.format(netif)])
            if ret == 1:
                self._logger.warn('Unable to obtain IP address from bluetooth adapter')
                self.internet_connected = False
                netif.Disconnect()
            else:
                self._logger.info('Internet connection established')
                self.internet_connected = True
        else:
            self._logger.warn('Unable to establish bluetooth tethering with any preferred devices')
                
        self.refreshData()        
#dbus-send --system --type=method_call --dest=org.bluez /org/bluez/hci0/dev_2C_44_01_CF_73_FE org.bluez.Network1.Connect string:'nap'