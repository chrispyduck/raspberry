from threading import Thread
from multiprocessing.synchronize import Event

class Timer(Thread):
    def __init__(self, interval, callback):
        self._trigger = Event()
        self._interval = interval
        self._callback = callback
        
    def stop(self):
        self._trigger.set()
        
    def run(self):
        while not self._trigger.wait(self._interval):
            self._callback()
        