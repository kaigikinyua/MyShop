import datetime,os
from settings import Settings

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
        pass

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
        data=[]
        infile=open(pathToFile)
        reader=CSV.reader(infile)
        for row in reader:
            data.append(row)
        infile.close()
        return data
    
    @staticmethod
    def writeCSVFile(pathToFile):
        pass
        #do some reaserch on csv.writer

    @staticmethod
    def removeCSVHeaders(data):
        return data[0],data[1:len(data)]

    @staticmethod
    def getColumn(headers=None,columnName='',data=[]):
        i=0
        headerIndex=0
        headerString=""
        for header in headers:
            if(header.lower()==columnName.lower()):
                headerIndex=i
                headerString=header
                break
            i=i+1
        columnData=[]
        for row in data:
            columnData.append(row[headerIndex])
        return headerString,columnData
    
    @staticmethod
    def getRow(data=[],rowIndex=0,removedHeaders=True):
        if(removedHeaders==False):
            h,data=CSV.removeHeaders(data)
        if(len(data)<=rowIndex):
            return data[rowIndex]
        else:
            print("Array out of bounds index")
        return None

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