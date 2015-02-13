import RPi.GPIO as GPIO
import logging

class GpioInputMonitor(object):
	def __init__(self, name, channel, callback):
		self._channel = channel
		self._callback = callback
		self._name = name
		GPIO.setup(self._channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self._last_value = GPIO.input(self._channel)
		GPIO.add_event_detect(self._channel, GPIO.BOTH, callback=self._change, bouncetime=250)
		logging.debug('Registering GPIO pin %d as input for "%s"; value=%r', self._channel, self._name, self._last_value)
	
	@property
	def name(self):
		"""Gets the given display name of the input pin"""
		return self._name

	@property
	def channel(self):
		"""Gets the pin number"""
		return self._channel
	
	@property
	def value(self):
		"""Gets the current value of the input pin"""
		return GPIO.input(self._channel)
		
	
	def _change(self, channel):
		if channel != self._channel:
			pass
		
		value = GPIO.input(self._channel)
		if (value == self._last_value):
			pass
		
		logging.debug('Detected GPIO event for "%s"; value=%r', self.name, value)
		self._last_value = value
		self._callback(value)