import datetime,os,json,bcrypt
import numpy as np


class Settings:
    dataBaseUrl="sqlite:///data/databases/prod/myshop.db"
    configFileUrl="./data/configs/defaultConfig.json"
    serverUrl=None
    serverToken=None
    mode="DEBUG" #[DEBUG|PROD]
    
    @staticmethod
    def getDataBaseUrl():
        if(Settings.mode!='DEBUG'):
            Settings.dataBaseUrl="sqlite:///data/databases/prod/myshop.db"
        return "sqlite:///data/databases/debug/myshop.db"
    
    @staticmethod
    def getServerCredentials():
        if(Settings.serverToken==None and Settings.serverUrl==None):
            configData=JsonFile.readJsonFile(Settings.configFileUrl)
            serverUrl=configData["reportToServer"]["serverUrl"]
            token=Settings.serverUrl=configData["reportToServer"]["token"]
            if(serverUrl!=None and token!=None):
                Settings.serverUrl=configData["reportToServer"]["serverUrl"]
                return serverUrl,token
            else:
                Logging.consoleLog('warn',f'Warning Server url and token not set in {Settings.configFileUrl}')
                return None,None
        else:
            return Settings.serverUrl,Settings.serverToken
    
    
    @staticmethod
    def logFile():
        sessionLogDir=f"./data/logs/sessionLogs/"
        dTimeObj=datetime.datetime.now()
        return f'{sessionLogDir}logFile_{dTimeObj.year}_{dTimeObj.month}_{dTimeObj.day}_at{dTimeObj.hour}_{dTimeObj.minute}.txt'
    
    @staticmethod
    def tillId():
        configData=JsonFile.readJsonFile(Settings.configFileUrl)
        return configData["identity"]["terminalName"],configData["identity"]["terminalTic"]

    
    @staticmethod
    def hashAndsalt(data):
        data=str(data)
        salt=bcrypt.gensalt()
        hashedData=bcrypt.hashpw(data.encode('utf-8'),salt)
        return hashedData
    
    @staticmethod
    def hashCompare(data,hashedData):
        return bcrypt.checkpw(bytes(data,'utf-8'),hashedData)

class FormatTime:
    #Jan:31 Feb Mar:31 Apr:30 May:31 June:30 July:31 Aug:31 Sep:30 Oct Nov:30 Dec:31
    @staticmethod
    def monthsTotalDays(year):
        months={
            'month':'jan','1':31,
            'month':'feb','2':28,
            'month':'mar','3':31,
            'month':'apr','4':30,
            'month':'may','5':31,
            'month':'jun','6':30,
            'month':'jul','7':31,
            'month':'aug','8':31,
            'month':'sep','9':30,
            'month':'oct','10':31,
            'month':'nov','11':30,
            'month':'dec','12':31
        }
        if(year%4==0):
            months['2']=29
        return months

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
    
    @staticmethod
    def dateTimeToStandardTime(timestamp):
        date=datetime.datetime.fromtimestamp(timestamp)
        year=date.year
        month=date.month
        day=date.day
        hour=date.hour
        minute=date.minute
        seconds=date.second
        return f'{day}/{month}/{year} {hour}:{minute}:{seconds}'

    @staticmethod
    def getDateToday():
        date=datetime.datetime.now()
        year=date.year
        month=date.month
        day=date.day
        return f'{day}/{month}/{year}'
    
    @staticmethod
    def getDateTodayTimeStamp():
        date=datetime.datetime.now()
        return FormatTime.toTimeStamp(date.year,date.month,date.day,0,0,0)

    @staticmethod
    def getEndOfDayTimeStamp():
        date=datetime.datetime.now()
        return FormatTime.toTimeStamp(date.year,date.month,date.day,23,59,59)

    @staticmethod
    def getMonthStartTimeStamp(month,year):
        return FormatTime.toTimeStamp(year,month,1,0,0,0)

    @staticmethod
    def getMonthEndTimeStamp(month,year):
        months=FormatTime.monthsTotalDays(year)
        monthNumDays=months[str(month)]
        return FormatTime.toTimeStamp(year,month,monthNumDays,0,0,0)
    
class Logging:
    @staticmethod
    def consoleLog(color,message):
        colors={'err':'','error':'','succ':'','warn':'','norm':'','debug':''}
        if(Settings.mode=='DEBUG'):
            print(message)
        else:
            Logging.logToFile('color',message)

    @staticmethod
    def logToFile(type,message):
        logFilePath=Settings.logFile()
        time=FormatTime.nowStandardTime()
        line=f'\n{type}| {time}| {message}'
        File.writeToFile(logFilePath,line)

class JsonFile:
    @staticmethod
    def readJsonFile(filePath):
        try:
            # Open the file in read mode ('r')
            with open(filePath, 'r') as file:
                # Load the JSON data and convert it to a Python object (dictionary)
                data = json.load(file)
                return data
        except FileNotFoundError:
            Logging.consoleLog('err',f"Error: File {filePath} not found")
        except json.JSONDecodeError as e:
            Logging.consoleLog('err',f"Error: Failed to decode JSON from the file. Details: {e}")
        return []

class File:
    @staticmethod
    def fileExists(filePath):
        if(os.path.isfile(filePath)):
            return True
        return False

    @staticmethod
    def writeToFile(filePath,data):
        if(File.fileExists(filePath)==False):
            File.createFile(filePath)
        file=open(filePath,'a')
        file.write(data)
        file.close()
        return True
            
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
    @staticmethod
    def readCSVFile(pathToFile):
        if(File.fileExists(pathToFile)==False):
            Logging.consoleLog('err',f'Error: File {pathToFile} does not exist')
            return []
        else:
            data=np.genfromtxt(pathToFile,dtype=str,delimiter=',',encoding=None)
            return data
        
    @staticmethod
    def writeCSVFile(pathToFile):
        pass
        #do some reaserch on csv.writer

    @staticmethod
    def removeCSVHeaders(data):
        return data[0],data[1:len(data)-1]

    @staticmethod
    def getColumnByName(headers=None,columnName='',data=[]):
        pass
    
    @staticmethod
    def getRow(data=[],rowIndex=0,removedHeaders=True):
        pass

    @staticmethod
    def createCsv(headers=[],data=[],autoIndexRows=True):
        csvData=[]
        if(autoIndexRows):
            if(len(headers)==len(data[0])):
                headers.insert('Index',0)
            rowIndex=1
            for row in data:
                row.insert(rowIndex,0)
                csvData.append(row)
            csvData.insert(headers,0)
        else:
            csvData.append(headers)
            csvData.append(data)
        return csvData
    

