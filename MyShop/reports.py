import datetime
from views import ShiftView,EndOfDaySales,CustomerCreditView,SaleSettingsView,UserView,TransactionView,PaymentView,SoldItemsView
from utils import Logging,CSV,FormatTime

class Reports:
    #daily reports
    def generateSalesReport(self,reportType,shiftObj,startTime,endTime):
        sTime,endTime=startTime,endTime
        mpesaSales,cashSales,bankSales,creditObj=ReportData.getSalesByType(startTime,endTime)
        numberOfTransactions=mpesaSales['num']+cashSales['num']+bankSales['num']
        salesSettingsState,salesSettings=SaleSettingsView.getSalesSettings()
        storeDetails={'storeId':salesSettings.tillId}
        dateTime=f'Date: {FormatTime.dateTimeToStandardTime(FormatTime.now())} Time: {datetime.datetime.time}'
        openningFloat=shiftObj.startingAmount
        closingAmount=shiftObj.closingAmount

        grossSales=EndOfDaySales.calcEndOfDaySales(shiftObj.startTime,FormatTime.now())
        taxes=EndOfDaySales.calcTaxes(grossSales)
        netSales=grossSales-taxes
        
        auth={
            'shiftId':shiftObj.shiftId,
            'openningTime':FormatTime.dateTimeToStandardTime(shiftObj.startTime),
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
            Number of Sales : --------------\t{numberOfTransactions}
            Gross Sales:--------------------\t{grossSales}
            Tax:----------------------------\t{taxes}
            Net Sales:----------------------\t{netSales}

            Number of Cash Transactions:    \t{cashSales['num']}
            Cash(Starting Amount):----------\t{openningFloat}
            Cash(Collected):----------------\t{cashSales['totalAmount']}
            Total Cash: --------------------\t{openningFloat+cashSales["totalAmount"]}
            Cash(Closing Amount):-----------\t{closingAmount}

            Number of Bank Transactions:    \t{bankSales['num']}
            Bank(Collected):----------------\t{bankSales["totalAmount"]}

            Number of Mpesa Transactions:   \t{mpesaSales['num']}
            Mpesa Total Collected-----------\t{mpesaSales['totalAmount']}

            -----------------------------------------------------------------
            Credit Paid today---------------\t{creditObj['paid']}
            Credit Unpaid ------------------\t{creditObj['unpaid']}

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

    def genFullCreditReport(self):
        paidCredit,unpaidCredit=EndOfDaySales.calcAllPaidAndUnpaidCredit()
        creditView=CustomerCreditView()
        reportName,creditReport=creditView.genFullCreditReport(False)
        Logging.consoleLog('message',creditReport)
        if(reportName!=False):
            custReportTxt=''
            for credit in creditReport:
                custReportTxt+='\n---------------------------------------------------------\n'
                custReportTxt+='Name: '+credit['name']+'\n'+'Phone: '+credit['phone']+'\n\n'
                for c in credit['credit']:
                    custReportTxt+='\t\n\nTransaction Id:------- '+str(c['transactionId'])
                    custReportTxt+='\t\nDeadLine:--------------- '+str(c['deadLine'])
                    custReportTxt+='\t\nCredit Amount:---------- '+str(c['creditAmount'])
                    custReportTxt+='\t\nPaid Amount:------------ '+str(c['paidAmount'])
                    custReportTxt+='\t\nDeficit----------------- '+str(float(c['creditAmount'])-float(c['paidAmount']))+'\n'
        allCreditReport=f'''
        Full Credit Report 
        Date:{FormatTime.dateTimeToStandardTime(FormatTime.now())}\n\n

        Unpaid Credit-----------------------{unpaidCredit}
        Paid Credit-------------------------{paidCredit}


        Unpaid Credit List:
        {custReportTxt}

        '''

        return allCreditReport

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

    @staticmethod
    def generateReportByName(reportName,startDate,endDate):
        if(reportName==None or startDate==None or endDate==None):
            Logging.consoleLog('Cannot pass None to generateReportByName(reportName={reportName},startDate={startDate},endDate={endDate})')
            return {}
        else:
            report={'name':reportName,'data':['not implemented','not implemented']}
            if(reportName=='saleReport'):
                pass
            elif(reportName=='stockReport'):
                pass
            elif(reportName=='creditReport'):
                pass
            elif(reportName=='xReport'):
                pass
            elif(report=='zReport'):
                pass
            return report


class ReportData:

    @staticmethod
    def getSalesByType(sTime,endTime):
        p=PaymentView()
        mpesaPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'mpesa')
        cashPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'cash')
        bankPayments=p.fetchPaymentsByTimeAndPaymentMethod(sTime,endTime,'bank')
        dayPaidCredit=EndOfDaySales.calcDayPaidCredit(sTime,endTime)
        dayUnPaidCredit=EndOfDaySales.calcDayCredit(sTime,endTime)

        totalMpesa=CalcSales.calcTotal(mpesaPayments)
        totalCash=CalcSales.calcTotal(cashPayments)
        totalBank=CalcSales.calcTotal(bankPayments)

        numMpesa=len(mpesaPayments)
        numCash=len(cashPayments)
        numBank=len(bankPayments)
        
        mpesaObj={'paymentType':'mpesa','num':numMpesa,'totalAmount':totalMpesa}
        cashObj={'paymentType':'cash','num':numCash,'totalAmount':totalCash}
        bankObj={'paymentType':'bank','num':numBank,'totalAmount':totalBank}
        creditObj={'paid':dayPaidCredit,'unpaid':dayUnPaidCredit}
        return mpesaObj,cashObj,bankObj,creditObj
    
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
