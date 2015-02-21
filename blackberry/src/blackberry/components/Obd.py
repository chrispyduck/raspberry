from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.data.DataSeries import DataSeries
import obd, logging
from blackberry.configuration.ConfigData import CurrentConfig

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
        series = DataSeries('obd')
        conn = self.connection
        for counter in self._counters:
            series.add(counter, conn.query(counter))
        return series
