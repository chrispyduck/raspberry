import unittest, obd
from blackberry.components.Obd import Obd
from blackberry.configuration.ConfigData import CurrentConfig

class Obd_test(unittest.TestCase):
    def test_obd(self):
        # force python-OBD to write debugging info to console
        obd.debug.console = True
        
        CurrentConfig.data.collector_configuration['Obd'] = {
                "sensors": [
                    'RPM',
                    'COOLANT_TEMP',
                    'FUEL_STATUS',
                    'FUEL_PRESSURE',
                    'INTAKE_PRESSURE',
                    'INTAKE_TEMP',
                    'SPEED',
                    'THROTTLE_POS'
                ],
                "baudrate": 38400,
                "port": None # automatically detect obdsim
            }
        obdCollector = Obd()
        self.assertEqual(len(obdCollector._counters), len(CurrentConfig.data.collector_configuration['Obd']['sensors']), 'the list of sensors should have been loaded as provided')
        
        series = obdCollector.GetData()
        for item in series.points:
            print("{0}: {1}".format(item.counter, item.value))
        self.assertEqual(len(series.points), len(CurrentConfig.data.collector_configuration['Obd']['sensors']), 'Some data should have been collected')
        