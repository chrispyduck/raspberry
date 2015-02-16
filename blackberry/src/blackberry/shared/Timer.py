from threading import Thread
from multiprocessing.synchronize import Event

class Timer(object):
    def __init__(self, interval, callback):
        self._thread = Thread(target=self.run)
        self._trigger = Event()
        self._interval = interval
        self._callback = callback
        
    def start(self):
        self._thread.start()
        
    def stop(self):
        self._trigger.set()
        self._thread.join(1)
        
    def run(self):
        while not self._trigger.wait(self._interval):
            self._callback()
        