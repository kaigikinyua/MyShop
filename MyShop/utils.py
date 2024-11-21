import datetime
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

class Logging:
    pass

class CSV:
    pass
