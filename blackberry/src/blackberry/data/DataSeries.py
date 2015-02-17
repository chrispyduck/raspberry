from blackberry.data.DataPoint import DataPoint

class DataSeries(object):
    """describes a set of data points from a particular data source"""
    def __init__(self, source):
        self.points = []
        self.source = source
    
    def add(self, counter, value):
        self.points.append(DataPoint(counter, value))
        
    def serialize(self):
        p = []
        for point in self.points:
            p.append(point.__dict__)
        
        d = {
             "source": self.source,
             "points": p
             }
                
        return d