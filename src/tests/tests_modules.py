'''
Unit/Module tests for the following
modules.utils.py
    FormatTime,Logging,JsonFile,File,CSV
'''
import unittest
from unittest import TestCase
from modules.utils import File,FormatTime,Logging,JsonFile,CSV

import numpy as np

class TestCSVData:
    filePath='./data/products.csv'

class TestCSV(unittest.TestCase):
    def test_readCSVFile(self):
        data=CSV.readCSVFile(TestCSVData.filePath)
        self.assertGreater(len(data),0)

    def test_writeCSVFile(self):
        pass

    def test_removeCSVHeaders(self):
        allData=CSV.readCSVFile(TestCSVData.filePath)
        headers,data=CSV.removeCSVHeaders(allData)
        self.assertEqual(len(data),len(allData)-1)
        self.assertEqual(len(headers),len(allData[0]))

    def test_getColumnByName(self):
        allData=CSV.readCSVFile(TestCSVData.filePath)
        headers,data=CSV.removeCSVHeaders(allData)
        # for h in headers:
        #     column=CSV.getColumnByName(h,data)
        #     print(column)

    def test_getRow(self):
        pass

    def test_createCsv(self):
        pass




'''class TestReports(unittest.TestCase):
    def test_headers(self):
        result1=',Item Name,Bar Code,Quantity,\n'
        array=['Item Name','Bar Code','Quantity']
        csvHeader1=CSV.headers(array,True)
        TestCase.assertEqual(self,result1,csvHeader1)
        result2='Item Name,Bar Code,Quantity,\n'
        csvHeader2=CSV.headers(array,False)
        TestCase.assertEqual(self,result2,csvHeader2)

    def test_rowData(self):
        result1='1,100,200,400,500,600,\n2,123,456,789,345,301,\n'
        array=[[100,200,400,500,600],[123,456,789,345,301]]
        csvData1=CSV.rowData(array,numberedRow=True,emptyStart=False)
        TestCase.assertEqual(self,result1,csvData1)


    def test_dataSheet(self):
        header=['Item Name','Bar Code','Quantity']
        data=[[100,200,400,500,600],[123,456,789,345,301]]
        dataString=CSV.dataSheet(header,data)
        f=open('test_csv.csv','w')
        f.write(dataString)
        f.close()
'''
if __name__=='__main__':
    unittest.main()