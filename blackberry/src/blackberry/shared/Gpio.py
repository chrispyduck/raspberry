import os, logging

if os.uname()[4][:3] == 'arm':
	rpi = True
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
else:
	rpi = False
	logging.warn('You do not appear to be running this on a Raspberry Pi. GPIO functionality has been disabled.')

class _GpioBaseObject(object):
	def __init__(self, name, channel):
		self._logger = logging.getLogger(self.__class__.__name__)
		self._channel = channel
		self._name = name

	@property
	def name(self):
		"""Gets the given display name of the input pin"""
		return self._name

	@property
	def channel(self):
		"""Gets the pin number"""
		return self._channel
	
class GpioInputMonitor(_GpioBaseObject):
	def __init__(self, name, channel, callback):
		super(_GpioBaseObject, self).__init__(name, channel)
		self._callback = callback
		if rpi:
			GPIO.setup(self._channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
			self._last_value = GPIO.input(self._channel)
			GPIO.add_event_detect(self._channel, GPIO.BOTH, callback=self._change, bouncetime=250)
		else:
			self._last_value = False
		self._logger.debug('Registering GPIO pin %d as input for "%s"; value=%r', self._channel, self._name, self._last_value)
	
	@property
	def value(self):
		"""Gets the current value of the input pin"""
		if rpi:
			return GPIO.input(self._channel)
		else:
			return False
		
	def _change(self, channel):
		if channel != self._channel:
			pass

		if rpi:		
			value = GPIO.input(self._channel)
		else:
			value = False

		if (value == self._last_value):
			pass
		
		self._logger.debug('Detected GPIO event for "%s"; value=%r', self.name, value)
		self._last_value = value
		self._callback(value)

class GpioSimpleOutput(_GpioBaseObject):
	def __init__(self, name, channel, value=0):
		super(_GpioBaseObject, self).__init__(name, channel)
		if rpi:
			GPIO.setup(self._channel, GPIO.OUT)
		self.value = value
		self._logger.debug('Registering GPIO pin %d as output for "%s"; value=%r', self._channel, self._name, self._last_value)
		
	@property
	def value(self):
		if rpi:
			return GPIO.input(self._channel)
		else:
			return self._value
		
	@value.setter
	def value(self, val):
		if rpi:
			GPIO.output(self._channel, val)
		else:
			self._value = val