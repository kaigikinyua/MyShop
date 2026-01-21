import requests,os,shutil,json
from .utils import Logging,Settings
class BackUp:
    @staticmethod
    def runDataBaseBackUp():
        pass
    @staticmethod
    def runLogsBackUp():
        pass

    @staticmethod
    def backUpDirectory(srcDirectory,destFolder):
        directoryContents=os.listdir(srcDirectory)
        state=shutil.copy(srcDirectory,destFolder)

    @staticmethod
    def backUpFile(srcFilePath,destFolder):
        shutil.copy(srcFilePath,destFolder)

class Server:
    @staticmethod
    def postData(subUrl,data):
        serverUrl,token=Settings.getServerCredentials()
        print(f'Server url {serverUrl} token {token} data {data}')
        if(token!=None and serverUrl!=None):
            payload={"token":token,"data":data}
            status=requests.post(f'{serverUrl}/{subUrl}', json=payload)
            if(status.status_code!=201):
                Logging.consoleLog('err',f'Error: Error while posting to server/n server error code {status.status_code}')
            elif(status.status_code==201):
                Logging.consoleLog('succ',f'Success:Posted data to server\nData= {payload}')
                return status.json(),True
        return [],False

    @staticmethod
    def getData(subUrl):
        serverUrl,token=Settings.getServerCredentials()
        status=requests.get(f'{serverUrl}/{subUrl}')
        print(status)
        if(status.status_code!=200):
            Logging.consoleLog('err',f'Error: Error while getting from server/n server error code {status.status_code}')
        elif(status.status_code==200):
            Logging.consoleLog('succ',f'Success:Get request successfull')
            return status.text,True
        return [],False
    
    @staticmethod
    def postFiles(files,subUrl):
        pass