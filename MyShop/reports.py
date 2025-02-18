import datetime
from views import UserView,TransactionView,PaymentView,SoldItemsView
from utils import Logging
class Reports:
    #daily reports
    def generateXReport(self,dateTimeStamp):
        reportName='X Report'
        storeDetails={'storeId':'Main Store'}
        dateTime=f'Date: {datetime.datetime.date} Time: {datetime.datetime.time}'
        
        numberOfTransactions=0

        mpesaSales={'amount':50000,'numOfTransactions':1}
        cashSales={'amount':20000,'numOfTransactions':2}
        cardSales={'amount':16000,'numOfTransactions':3}
        creditSales={'amount':3000,'numOfTransactions':4}
        openningFloat=0
        grossSales=mpesaSales['amount']+cashSales['amount']+cardSales['amount']+creditSales['amount']
        cashInHand=grossSales-creditSales['amount']+openningFloat
        netSales=0
        taxes=0

        auth={
            'shiftId':'faslkdjfalk',
            'openningTime':'12:01am',
            'logins':6,
            'operatorId':1,
        }
        
        reportString=f'''
            {reportName} {dateTime}
            Store: {storeDetails['storeId']}        
            Shift Id: {auth['shiftId']} Operator Id: {auth['operatorId']}
            Openning Time: {auth['openningTime']}
            Num of Logins: {auth['logins']}
            -------------------------------------------------------------
            Sales:
            Number of Sales : ------------{numberOfTransactions}
            Gross Sales:------------------{grossSales}
            Credit Sales:------------------{creditSales['amount']}
            Money at hand:-----------------{cashInHand}
            Tax:----------------------------{taxes}

            Number of Cash Transactions: {cashSales['numOfTransactions']}
            Cash(Float):-----------------{openningFloat}
            Cash(Collected):-------------{cashSales['amount']}
            Total Cash: -----------------{openningFloat+cashSales["amount"]}

            Number of Bank Transactions: {cardSales['numOfTransactions']}
            Bank(Collected):-------------{cardSales["amount"]}

            Number of Mpesa Transactions: {mpesaSales['numOfTransactions']}
            Mpesa Total Collected---------{mpesaSales['amount']}

            Number of Credit Transactions: {creditSales['numOfTransactions']}
            Total Credit ------------------{creditSales['amount']}

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

class CalcSales:
    @staticmethod
    def calcPaymentTypeSold(startTimeStamp,endTimeStamp,salesType):
        p=PaymentView()
        payments=p.filterPaymentByPaymentType(startTimeStamp,endTimeStamp,salesType)
        total=0
        if(payments!=None):
            numOfCashTransactions=len(payments)
            total=p.calcTotal(payments)
            if(total==0):
                Logging.consoleLog(f"Error while calculating total {salesType} sales")
        else:
            Logging.consoleLog("Got None from PaymentView.filterPaymentByPaymentType()")
        return total,numOfCashTransactions

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