from blackberry.configuration._ConfigType import _ConfigType

'''
@summary: Provides default values for GPIO settings
@author: chrispyduck
'''
class _ConfigGpio(_ConfigType):
    def __init__(self):
        super(_ConfigType, self).__init__()
        self.vAcc = 19
        self.vBatt = 13
        self.vAccIndicator = 12
        self.CollectDataIndicator = 16
        self.PowerOffToggleDelay = 5