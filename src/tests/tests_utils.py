'''
Unit/Module tests for the following
modules.utils.py
    FormatTime,Logging,JsonFile,File,CSV
'''

import unittest
from unittest import TestCase

from modules.utils import Settings,FormatTime,Logging,JsonFile,File,CSV


class Tests_Settings(unittest.TestCase):
    def test_getDataBaseUrl(self):
        dbUrl=Settings.getDataBaseUrl()
        self.assertNotEqual(dbUrl,None)
        if(Settings.mode=='DEBUG'):
            self.assertEqual(dbUrl,'sqlite:///data/databases/debug/myshop.db')
        elif(Settings.mode=='PROD'):
            self.assertEqual(dbUrl,'sqlite:///data/databases/prod/myshop.db')
    
    def test_getServerCredentials(self):
        serverUrl,token=Settings.getServerCredentials()
        data=JsonFile.readJsonFile(Settings.configFileUrl)
        sUrl=data["reportToServer"]["serverUrl"]
        sToken=data["reportToServer"]["token"]
        self.assertEqual(sUrl,serverUrl)
        self.assertEqual(sToken,token)

    def test_logFile(self):
        logFile=Settings.logFile()
        self.assertNotEqual(logFile,None)
        #logFileExists=File.fileExists(logFile)
        #self.assertEqual(logFileExists,True)
    
    def test_tillId(self):
        terminalName,terminalTic=Settings.tillId()
        data=JsonFile.readJsonFile(Settings.configFileUrl)
        tName=data["identity"]["terminalName"]
        tTic=data["identity"]["terminalTic"]
        self.assertEqual(terminalName,tName)
        self.assertEqual(terminalTic,tTic)


    def test_hashAndSalt(self):
        password='password'
        hashPw=Settings.hashAndsalt(password)
        match=Settings.hashCompare('password',hashPw)
        self.assertEqual(match,True)


class Tests_FormatTime(unittest.TestCase):
    
    def test_monthsTotalDays(self):
        pass
    
    def test_now(self):
        pass

    def test_toTimeStamp(self):
        pass

    def test_getDateTime(self):
        pass

    def test_getDateTime(self):
        pass

    


if __name__=='__main__':
    unittest.main()