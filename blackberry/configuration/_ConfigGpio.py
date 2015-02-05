from blackberry.configuration._ConfigType import _ConfigType

'''
@summary: Provides default values for GPIO settings
@author: chrispyduck
'''
class _ConfigGpio(_ConfigType):
    def __init__(self):
        self.vAcc = 19
        self.vBatt = 13