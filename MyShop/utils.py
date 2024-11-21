import datetime,os

class FormatTime:
    @staticmethod
    def now():
        timestamp=datetime.datetime.timestamp(datetime.datetime.now())
        return timestamp
    @staticmethod
    def toTimeStamp(year,month,day,hour,minute,second):
        dTime=datetime.datetime(year,month,day,hour,minute,second)
        timestamp=datetime.datetime.timestamp(dTime)
        return timestamp

    @staticmethod
    def getDateTime(timestamp):
        return datetime.datetime.fromtimestamp(timestamp)
    
    @staticmethod
    def nowStandardTime():
        date=datetime.datetime.now()
        year=date.year
        month=date.month
        day=date.day
        hour=date.hour
        minute=date.minute
        seconds=date.second
        return f'{day}/{month}/{year} {hour}:{minute}:{seconds}'
        

class Logging:
    @staticmethod
    def consoleLog(color,message):
        colors={'err':'','succ':'','warn':'','norm':''}
        print(message)

    @staticmethod
    def logToFile(type,message):
        time=FormatTime.nowStandardTime()
        line=f'{type}| {time}| {message}\n'
        File.writeToFile()
class JsonFile:
    @staticmethod
    def readJsonFile(filePath):
        pass

class File:
    @staticmethod
    def fileExists(filePath):
        if(os.path.isfile(filePath)):
            return True
        return False

    @staticmethod
    def writeToFile(filePath,data):
        if(File.fileExists(filePath)):
            with open(filePath,'w') as f:
                f.write(data)
                f.close()
                return True
        else:
            return False
    @staticmethod
    def createFile(filePath):
        if File.fileExists(filePath):
            return False
        else:
            f=open(filePath,'w')
            f.close()
            return True

    @staticmethod
    def readFromFile(filePath):
        if(File.fileExists(filePath)):
            f=open(filePath,'r')
            data=f.readlines()
            f.close()
            return True,data
        else:
            return False,'File does not exist'
        
class CSV:
    pass