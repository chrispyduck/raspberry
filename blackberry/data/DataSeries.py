from blackberry.data.DataPoint import DataPoint

class DataSeries(object):
    """describes a set of data points from a particular data source"""
    def __init__(self, source):
        self.points = []
        self.source = source
    
    def addPoint(self, counter, value):
        self.points.append(DataPoint(counter, value))
        
    def serialize(self):
        return self.__dict__