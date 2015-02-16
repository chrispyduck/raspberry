class DataCollectorComponent(object):
    """Base class for any component that provides data to be logged"""
    def GetData(self):
        raise Exception("Not implemented")