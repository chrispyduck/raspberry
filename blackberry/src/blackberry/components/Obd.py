from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.configuration.ConfigData import CurrentConfig
import obd, logging

class Obd(DataCollectorComponent):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        
        self._config = CurrentConfig.data.collector_configuration['Obd']
        self._port = self._config['port']
        if not self._port:
            self._port = None
        self._baudrate = self._config['baudrate']
        if not self._baudrate:
            self._baudrate = 38400
        self._counters = []
        for counterName in self._config['sensors']:
            self._counters.append(obd.commands.__getitem__(counterName))
            
    @property
    def connection(self):
        if not hasattr(self, '_connection') or not self._connection.is_connected():
            self._connection = obd.OBD(self._port, baudrate=self._baudrate)
        return self._connection

    def GetData(self):
        conn = self.connection
        for counter in self._counters:
            yield {
                   "src": "obd",
                   "mode": int('0x'+counter.mode, 0),
                   "pid": int('0x'+counter.pid, 0),
                   "value": conn.query(counter).value
                   }
