import unittest
from blackberry.components.Obd import Obd

class Obd_test(unittest.TestCase):
    def test_obd(self):
        obd = Obd()
        series = obd.GetData()
        self.assertGreater(0, len(series.points), 'Some data should have been collected')