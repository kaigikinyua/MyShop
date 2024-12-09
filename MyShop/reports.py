import datetime
from views import UserView,TransactionView,PaymentView,SoldItemsView

class Reports:
    #daily reports
    def generateXReport(self,dateTimeStamp):
        reportName='X Report'
        storeDetails={'storeId':'Main Store'}
        dateTime=f'Date: {datetime.datetime.date} Time: {datetime.datetime.time}'
        
        mpesaSales={'amount':5000,'numOfTransactions':1}
        cashSales={'amount':5000,'numOfTransactions':1}
        cardSales={'amount':5000,'numOfTransactions':1}
        openningFloat=0
        grossSales,netSales,taxes=0,0,0

    

        auth={
            'shiftId':'faslkdjfalk',
            'openningTime':'12:01am',
            'logins':6,
            'operatorId':1,
        }
        sales={
            'numberOfSales':5,
            'cashSales':{'collected':cashSales['amount'],'float':openningFloat},
            'bankSales':{'bank':5000,'card':3000},
            'mpesaSales':10000,
            'GrossSales':grossSales
            }
        
        reportString=f'''
            {reportName} {dateTime}
            Store: {storeDetails['storeId']}        
            Shift Id: {auth['shiftId']} Operator Id: {auth['operatorId']}
            Openning Time: {auth['openningTime']}
            Num of Logins: {auth['logins']}
            -------------------------------------------------------------
            Sales:
            Number of Sales : {sales['numberOfSales']}
            Total Sales:

            Cash(Float):{sales['cashSales']['float']}
            Cash(Collected):{sales['cashSales']['collected']}
            Total Cash: {sales['cashSales']['collected']+sales['cashSales']['float']}

            Bank

        '''

    def generateZReport(self,dateTimeStamp):
        reportName='Z Report'
        dateTime=f'Date: {datetime.datetime.date} Time: {datetime.datetime.time}'
        auth={
            'shiftId':'faslkdjfalk',
            'openningTime':'12:01am',
            'logins':6,
            'operatorId':1,
        }
        sales={
            'numberOfSales':5,
            'cashSales':{'collectedCash':300,'float':5000},
            'bankSales':{'bank':5000,'card':3000},
            'mpesaSales':10000
            }
        stockSales=[
            {'productId':'Jin Whiskey 500ml','quantity':5},
        ]


    def generateStockReport(self,startDate,endDate):
        reportName='Stock Report'
        dateTime=f'Date: {datetime.datetime.date} Time: {datetime.datetime.time}'
        stockReport={
            'instockItems':[
                {'itemId':'fasjdfklla','itemName':'','quantiry':100}
            ],
            'soldItems':[
                {'itemId':'fasjdfklla','itemName':'','quantiry':100}
            ],
            'soldItemsValue':1000,
            'cashReceived':100,
            'mpesaReceived':300,
            'bankReceived':400,
            'creditAmout':200,
            'creditedTransactions':[
                {'transactionId':'003','date':'11/12/2024','creditAmount':100,'custName':'James','phone':'+i560898768'},
                {'transactionId':'004','date':'11/12/2024','creditAmount':50,'custName':'Hammond','phone':'+i5698098768'}
            ]
        }

    def generateOperationReport(self,startDate,endDate):
        reportName='Operation Report'
        dateTime=f'Date: {datetime.datetime.date} Time: {datetime.datetime.time}'
        operationReport={
            'bills':[
                {'billName':'rent','desc':'Rent for Warehouse','amount':50000,'date':'11/12/2024','paid':True},
                {'billName':'electricity','desc':'Electricity for warehouse','amount':300,'date':'11/12/2024','paid':True},
                {'billName':'fuel','desc':'fuel for KBZ 100Q','amount':3000,'date':'11/12/2024','paid':True},
                {'billName':'water','desc':'water bill for warehouse','amount':50000,'date':'11/12/2024','paid':True},
            ],
            'pettyCash':[
                {'desc':'Callers credit','amount':400,'paid':True},
                {'desc':'4 Casual labourers','amount':400,'paid':True},
            ],
            'wages':[
                {'employeeName':'James Njoroge','amount':30000,'paid':True}
            ]
        }

    def printReport(self,reportData,outPutFile):
        pass

class CSV:
    @staticmethod
    def headers(headers,emptyStart):
        if(len(headers)>0):
            h=''
            if(emptyStart==True):
                h+=','
            for header in headers:
                h+=f'{str(header)},'
            return f'{h}\n'
        return False

    @staticmethod
    def rowData(two_D_array,numberedRow=False,emptyStart=True):
        if(len(two_D_array)>0):
            numRow=1
            d=''
            for row in two_D_array:
                if(emptyStart):
                    d=','
                if(numberedRow):
                    d=d+f'{str(numRow)},'
                for elm in row:
                    d=d+f'{elm},'
                d=d+'\n'
                numRow+=1
            return d
        
    @staticmethod
    def columData(header,data):
        dataString=f'{str(header)},'
        for d in data:
            dataString+=f'{str(d)},\n'
        return dataString
    
    @staticmethod
    def addColumn(previousColumns,column):
        pass
        
    @staticmethod
    def dataSheet(headers,data):
        headersString=CSV.headers(headers,True)
        dataString=CSV.rowData(data,True,False)
        dataSheet=headersString+dataString
        return dataSheet