from blackberry.shared.Timer import Timer
from time import sleep
import unittest

class Timer_test(unittest.TestCase):
    def repeat_callback(self):
        print('exec callback')
        self._repeat_i += 1
    
    def test_repeat(self):
        self._repeat_i = 0
        tmr = Timer(0.3, self.repeat_callback)
        tmr.start()
        sleep(1.3)
        tmr.stop()
        self.assertGreaterEqual(self._repeat_i, 3, "should have been called at least 3 times")
        
    def test_stop(self):
        self._repeat_i = 0
        tmr = Timer(0.3, self.repeat_callback)
        tmr.start()
        sleep(0.4)
        ct = self._repeat_i
        tmr.stop()
        sleep(2)
        self.assertLessEqual(self._repeat_i, 2, "should have been called at least 3 times")
        self.assertEqual(ct, self._repeat_i, "should not have recorded any hits since stopping the timer")
        