import logging

class _ConfigType(object):
    
    def load(self, rawdata):
        for key in rawdata:
            if key in self.__dict__:
                currentValue = self.__dict__[key]
                providedValue = rawdata[key]
                if issubclass(currentValue.__class__, _ConfigType):
                    currentValue.load(providedValue)
                else:
                    self.__dict__[key] = providedValue
            else:
                logging.warning('Unrecognized configuration key "%s" on object of type "%s"', key, self.__class__.__name__)