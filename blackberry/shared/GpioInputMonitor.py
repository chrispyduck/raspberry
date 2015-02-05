import RPi.GPIO as GPIO
import logging

class GpioInputMonitor(object):
	def __init__(self, name, channel, callback):
		self.channel = channel
		self._callback = callback
		self.name = name
		GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self._last_value = GPIO.input(channel)
		GPIO.add_event_detect(channel, GPIO.BOTH, callback=self._change, bouncetime=250)
		logging.debug('Registering GPIO pin %d as input for "%s"; value=%r', channel, name, self._last_value)
	
	def _change(self, channel):
		if channel != self.channel:
			pass
		
		value = GPIO.input(self.channel)
		if (value == self._last_value):
			pass
		
		logging.debug('Detected GPIO event for "%s"; value=%r', self.name, value)
		self._last_value = value
		self._callback(value)	