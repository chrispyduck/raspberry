from blackberry.configuration._ConfigType import _ConfigType
from blackberry.configuration._ConfigDataType import _ConfigDataType

class _ConfigData(_ConfigType):
    def __init__(self):
        super(_ConfigType, self).__init__()
        self.remote_db = _ConfigDataType()
        self.local_db = _ConfigDataType()
        self.capture_interval = 0.3
        self.enabled_collectors = ['TestDataCollector']
        self.collector_configuration = {}
        self.storage_backend = 'blackberry.data.DataStorage'