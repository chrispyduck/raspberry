from blackberry.configuration._ConfigType import _ConfigType
class _ConfigBluetooth(_ConfigType):
    def __init__(self):
        super(_ConfigType, self).__init__()
        self.autodiscover = True
        self.pin = 1123
        self.tetheringDevices = ["2C:44:01:CF:73:FE"]