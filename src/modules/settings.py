import datetime,json

class Settings:
    dataBaseUrl="sqlite:///data/databases/current/myshop.db"
    configFileUrl="./data/configs/config.json"
    mode="DEBUG" #[DEBUG|PROD]
    
    @staticmethod
    def getDataBaseUrl():
        if(Settings.mode!='DEBUG'):
            Settings.dataBaseUrl="sqlite:///data/databases/prod/myshop.db"
        return "sqlite:///data/databases/debug/myshop.db"
    @staticmethod
    def logFile():
        sessionLogDir=f"./data/logs/sessionLogs/"
        dTimeObj=datetime.datetime.now()
        return f'{sessionLogDir}logFile_{dTimeObj.year}_{dTimeObj.month}_{dTimeObj.day}_at{dTimeObj.hour}_{dTimeObj.minute}.txt'
    
    @staticmethod
    def tillId():
        return "ErrorSettingTillId"