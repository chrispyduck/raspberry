from blackberry.configuration._ConfigType import _ConfigType

class _ConfigPaths(_ConfigType):
    def __init__(self):
        super(_ConfigType, self).__init__()
        self.usb_power = "/sys/devices/platform/bcm2708_usb/buspower"