from blackberry.configuration._ConfigType import _ConfigType

class _ConfigDataType(_ConfigType):
    def __init__(self):
        super(_ConfigType, self).__init__()
        self.db = "mongodb://..."
        self.collection = "trips"