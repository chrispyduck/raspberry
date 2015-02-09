from blackberry.components.DataCollectorComponent import DataCollectorComponent

class DataCollectorStub(DataCollectorComponent):
    def __init__(self, fn):
        self._fn = fn
        pass
        
    def GetData(self):
        return self._fn()