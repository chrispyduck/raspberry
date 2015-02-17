from blackberry.data.DataBackend import DataBackend
from blackberry.configuration.ConfigData import CurrentConfig

class TestBackend(DataBackend):
    def __init__(self, configuration=CurrentConfig.data.local_db):
        super(TestBackend, self).__init__(configuration)
        
        
    def commit(self, dataSeries):
        self.collectedData.append(dataSeries)