from blackberry.components.DataCollectorComponent import DataCollectorComponent
from blackberry.data.DataSeries import DataSeries
import obd, logging

class Obd(DataCollectorComponent):
    def __init__(self):
        self._connection = obd.OBD()
        self._logger = logging.getLogger(self.__class__.__name__)
            
    def GetData(self):
        series = DataSeries('obd')
        counters = [
                    obd.commands.RPM,
                    obd.commands.COOLANT_TEMP,
                    obd.commands.FUEL_STATUS,
                    obd.commands.FUEL_PRESSURE,
                    obd.commands.INTAKE_PRESSURE,
                    obd.commands.SPEED,
                    obd.commands.INTAKE_TEMP,
                    obd.commands.THROTTLE_POS,
                    obd.commands.FUEL_LEVEL,
                    obd.commands.BAROMETRIC_PRESSURE,
                    obd.commands.EVAP_VAPOR_PRESSURE,
                    obd.commands.AMBIENT_AIR_TEMP,
                    obd.commands.OIL_TEMP,
                    obd.commands.FUEL_RATE
                    ]
        for counter in counters:
            series.addPoint(counter, self._connection.query(counter))
        return series
    
    