class Settings:
    devMode=True
    logs='./data/logs/'
    dataBase='./data/db/db.sqlite3'
    reports='./data/reports/'
    dbSetUp={
        'table':{'name':'users','fields':[]},
        'table':{'name':'products','fields':[]},
        'table':{'name':'inventory','fields':[]},
        'table':{'name':'counters','fields':[]},
        'table':{'name':'customers','fields':[]},
    }

class Log:
    @staticmethod
    def consoleLog():
        pass

class DataBase:
    @staticmethod
    def read(query):
        pass
    @staticmethod
    def writeToDb(query):
        pass
    @staticmethod
    def setUpDb(query):
        pass
    @staticmethod
    def copyDb():
        pass

class Files:
    pass
