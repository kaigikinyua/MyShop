import datetime
from views import ShiftView,CustomerCreditView,SaleSettingsView,UserView,TransactionView,PaymentView,SoldItemsView
from utils import Logging,CSV,FormatTime

class Reports:
    #daily reports
    def generateSalesReport(self,reportType,shiftObj,startTime,endTime):
        sTime,endTime=startTime,endTime
        mpesaSales,cashSales,bankSales=ReportData.getSalesByType(startTime,endTime)
        numberOfTransactions=mpesaSales['num']+cashSales['num']+bankSales['num']
        salesSettings=SaleSettingsView.getSalesSettings()
        reportName='X Report'
        storeDetails={'storeId':salesSettings.tillId}
        dateTime=f'Date: {FormatTime.dateTimeToStandardTime(FormatTime.now())} Time: {datetime.datetime.time}'
        openningFloat=shiftObj.startingAmount
        closingAmount=0
        grossSales=mpesaSales['totalAmount']+cashSales['totalAmount']+bankSales['totalAmount']
        cashInHand=grossSales+openningFloat
        taxes=(salesSettings.valueAddedTaxPercent*grossSales)/100
        netSales=0

        closeOnPrint=False
        zReportStuff=None
        
        auth={
            'shiftId':shiftObj.shiftId,
            'openningTime':shiftObj.startTime,
            'logins':shiftObj.logins,
            'openningId':shiftObj.openningId,
        }
        if(reportType=='z'):
            reportName='Z Report'
        
        reportString=f'''
            Report:{reportType.upper()} 
            {dateTime}
            Store: {storeDetails['storeId']}        
            Shift Id: {auth['shiftId']}
            Openning Id: {auth['openningId']}
            Openning Time: {auth['openningTime']}
            Num of Logins: {auth['logins']}
            -------------------------------------------------------------
            Sales:
            Number of Sales : ------------ {numberOfTransactions}
            Gross Sales:------------------ {grossSales}
            Money at hand:----------------- {cashInHand}
            Tax:---------------------------- {taxes}

            Number of Cash Transactions:  {cashSales['num']}
            Cash(Float):----------------- {openningFloat}
            Cash(Collected):------------- {cashSales['totalAmount']}
            Total Cash: ----------------- {openningFloat+cashSales["totalAmount"]}

            Number of Bank Transactions:  {bankSales['num']}
            Bank(Collected):------------- {bankSales["totalAmount"]}

            Number of Mpesa Transactions: {mpesaSales['num']}
            Mpesa Total Collected---------{mpesaSales['totalAmount']}

            -----------------------------------------------------------------
            Credit Payed today------------_________________
            Credit Unpaid ----------------_________________

        '''
        return reportString

    def genXReport(self,shiftId):

        shift=ShiftView.getShift(shiftId)
        startTime=shift.startTime
        endTime=FormatTime.now()
        if(shift.isClosed):
            endTime=shift.endTime

        reportString=self.generateSalesReport('x',shift,startTime,endTime)
        return reportString
    
    def genZReport(self,shiftId):
        shift=ShiftView.getShift(shiftId)
        startTime=shift.startTime
        endTime=FormatTime.now()
        if(shift.isClosed):
            endTime=shift.endTime

        reportString=self.generateSalesReport('z',shift,startTime,endTime)
        return reportString

    def genFullCreditReport(self,startDate,endDate):
        paymentView=PaymentView()
        paymentView.fetchAllPaymentsWithinPeriod()
    
    def genCustomerCreditReport(self,customerId):
        pass

    def genStockAndEmptiesReport(self,startDate,endDate):
        reportName='Stock and Empties Report'
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

    def printReport(self,reportData,outPutFile):
        pass

class ReportData:

    @staticmethod
    def getSalesByType(sTime,endTime):
        p=PaymentView()
        mpesaPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'mpesa')
        cashPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'cash')
        bankPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'bank')
        #creditPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'credit')
        totalMpesa=CalcSales.calcTotal(mpesaPayments)
        totalCash=CalcSales.calcTotal(cashPayments)
        totalBank=CalcSales.calcTotal(bankPayments)
        totalCredit=CalcSales.calcTotal(bankPayments)
        numMpesa=len(mpesaPayments)
        numCash=len(cashPayments)
        numBank=len(bankPayments)
        #numCredit=len(creditPayments)
        mpesaObj={'paymentType':'mpesa','num':numMpesa,'totalAmount':totalMpesa}
        cashObj={'paymentType':'cash','num':numCash,'totalAmount':totalCash}
        bankObj={'paymentType':'bank','num':numBank,'totalAmount':totalBank}
        #creditObj={'paymentType':'credit','num':numCredit,'totalAmount':totalCredit}
        return mpesaObj,cashObj,bankObj
    
    @staticmethod
    def getShift():
        obj=ShiftView.getOpenShiftObj()
        if(obj!=None):
            return obj
        
    @staticmethod
    def getShiftId():
        shift=ShiftView.getOpenShiftObj()
        if(shift!=None):
            return shift.shiftId
        return 'Error getting shift id'
    
    @staticmethod
    def getNumOfLogins():
        shift=ShiftView.getOpenShiftObj()
        if(shift!=None):
            return shift.logins
        return 'Error getting the num of open shifts'
    
class CalcSales:
    @staticmethod
    def calcTotal(salesObjList):
        total=0
        for sale in salesObjList:
            total=total+int(sale.amountPayed)
        return total
