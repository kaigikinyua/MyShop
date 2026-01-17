import sys,unittest
from unittest import TestCase
from modules.reports import CSV

class TestReports(unittest.TestCase):
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

if __name__=='__main__':
    unittest.main()