import datetime,json
class Settings:
    dataBaseUrl="sqlite:///data/databases/current/myshop.db"
    configFileUrl="./data/configs/config.json"
    mode="DEBUG" #[DEBUG|PROD]
    
    @staticmethod
    def logFile():
        sessionLogDir=f"./data/logs/sessionLogs/"
        dTimeObj=datetime.datetime.now()
        return f'{sessionLogDir}logFile_{dTimeObj.year}|{dTimeObj.month}|{dTimeObj.date}_at{dTimeObj.hour}|{dTimeObj.minute}.txt'
    
    @staticmethod
    def tillId():
        """f=open(Settings.configFileUrl,'r')
        data=f.readlines()
        f.close()
        jData=json.loads(str(data))
        return jData["tillId"]"""
        return "MainStore"