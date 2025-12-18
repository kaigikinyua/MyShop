import eel
from utils import Logging
from users import User,Cashier
from reports import Reports

pages=["index.html","till.html","admin.html"]

eel.init("web")  

@eel.expose    
def login(username,password):
    u=User()
    auth,message,userLevel,shiftId=u.login(username,password)
    branchesList=u.getBranchesList()
    if(auth):
        return {"auth":auth,"token":message,"userLevel":userLevel,"shiftId":shiftId,'branches':branchesList}    
    return {"auth":auth,"message":message,"userLevel":None,"shiftId":None,'branches':None}

@eel.expose
def logOut(userId):
    u=User()
    logOut=u.logout(int(userId))
    if(logOut):
        return {"state":True}
    else:
        return {"state":False}

@eel.expose
def makeSale(busketList,paymentList,tillId,cashier,custId):
    print("Making Sale")
    c=Cashier()
    state,message,transactionId=c.makeSale(busketList,paymentList,tillId,cashier,custId)
    if(state==False):
        return {"state":False,"message":f"Could Not complete sale: Error=> {message}"}
    return {"state":True,'message':'Sale Successfull','tId':transactionId,'payments':paymentList,'busketList':busketList}

@eel.expose
def customerCreditWorthy(custId,custPhone,amount):
    print("Assessing customer credit worthyness")
    return False

class FetchData:
    @staticmethod
    def fetchTransactions():
        pass
    @staticmethod
    def fetchTransaction():
        pass

    @staticmethod
    def getProductsAndBranches():
        u=User()
        productList=u.fetchAllProducts()
        brancheList=u.getBranchesList()
        return {'products':productList,'branches':brancheList}

    @staticmethod
    def getAllTransactions():
        u=User()
        transactionList=u.fetchAllTransactions()
        Logging.consoleLog('message',f'Getting All Transactions {transactionList}')
        return {'transactions':transactionList}
    
    @staticmethod
    def fetchAllCustomers():
        c=User()
        customers=c.fetchAllCustomers()
        return {'state':True,'customers':customers}

class CashierActions:

    @staticmethod
    def declareStartingAmount(userId,shiftId,startingAmount):
        if(userId!=None and shiftId!=None and startingAmount!=None):
            c=Cashier()
            sA=int(startingAmount)
            state,message=c.declareStartingAmount(userId,shiftId,sA)
            if(state==True):
                return {'state':True,'message':message}
            else:
                return {'state':False,'message':message}
        return {'state':False,'message':'Please fill in all the fields'}
        
    @staticmethod
    def declareClosingAmount(userId,shiftId,closingAmount):
        if(userId!=None and shiftId!=None and closingAmount!=None):   
            c=Cashier()
            state,message=c.declareClosingAmount(userId,shiftId,int(closingAmount))
            if(state==True):
                return {'state':True,'message':message}
            else:
                return {'state':False,'message':message}
        else:
            return {'state':False,'message':'Please fill in all the fields'}

    @staticmethod
    def registerCustomer(custName,custPhone):
        state=False
        message=''
        if(custName!=None and custPhone!=None):
            c=Cashier()
            state,message=c.registerCustomer(custName,custPhone)
        else:
            message='Please fill in the customer name and customer phone'
        return {'state':state,'message':message}
    
    @staticmethod
    def fetchCustomerTotalCredit(custId):
        Logging.consoleLog('message',f'Fetching customer Total credit custId={custId}')
        c=Cashier()
        state,creditTaken,creditAvailable,creditTransactions=c.fetchCustomerTotalCredit(custId)
        if(state==True):
            return {'state':True,'message':'Success','creditTaken':creditTaken,'creditAvailable':creditAvailable,'creditTransactions':creditTransactions}
        else:
            return {'state':False,'message':'Error while getting customerCredit','creditTaken':creditTaken,'creditAvailable':creditAvailable,'creditTransactions':creditTransactions}
    
    @staticmethod
    def payCustomerCredit(userId,tId,custId,paymentList):
        Logging.consoleLog('debug',f'Paying customer credit userId={userId} tId={tId} custId={custId} paymentList={paymentList}')
        c=Cashier()
        state,message=c.payCreditSale(userId,tId,custId,paymentList)
        
        return {'state':state,'message':message}
    
    @staticmethod
    def receiveStock(userId,invoiceId,receivedItems):
        if(userId!=None and invoiceId!=None and receivedItems!=None):
            c=Cashier()
            state,message=c.receiveStock(userId,invoiceId,receivedItems)
            return {'state':state,'message':message}
        else:
            return {'state':False,'message':'Empty fields passed to CashierActions.receiveStock()'}
    
    @staticmethod
    def genXReport(userId,shiftId):
        c=Cashier()
        state,report=c.genXReport(userId,shiftId)
        return {'state':state,'message':report,'report':report}
    
    @staticmethod
    def genZReport(userId,shiftId):
        c=Cashier()
        state,report=c.genZReport(userId,shiftId)
        return {'state':True,'message':report,'report':report}

    @staticmethod
    def genCreditReport(userId):
        cObject=Cashier()
        rportState=report=cObject.genCreditReport(userId)
        return {'state':True,'message':report,'report':report}

    @staticmethod
    def closeShift(shiftId,userId):
        if(shiftId!=None and userId!=None):
            c=Cashier()
            state,message,reports=c.closeShift(shiftId,userId)
            return {'state':state,'message':message,'reports':reports}

    @staticmethod
    def stockTake():
        pass

    @staticmethod
    def despatchStock():
        pass

class AdminActions:
    #admin user actions
    @staticmethod
    def addUser():
        pass

    @staticmethod
    def deleteUser():
        pass

    #product actions
    @staticmethod
    def addProduct():
        pass

    @staticmethod
    def deleteProduct(uId,productId):
        print(f"User {uId} Deleting product {productId}")
        return True

    @staticmethod
    def updateProduct():
        pass

    #stock actions
    @staticmethod
    def addStock():
        pass
    
    @staticmethod
    def deleteStock():
        pass

    @staticmethod
    def updateStock():
        pass

    @staticmethod
    def getReportByName(userId,reportName,startDate,endDate):
        u=User()
        authenticated=u.getUserLevel(userId,'admin')
        if(authenticated==False):
            Logging.logToFile('Error: Unauthorized access to ' \
            'getReportByName(userId={userId},reportName={reportName}, startDate={startDate}), endDate={endDate}')

            return {'state':False,'msg':'Unauthorized access','reports':[]}
        else:
            Logging.consoleLog('Generated report {reportName} starting from date {startDate} to end date {endDate}')
            report=Reports.generateReportByName(reportName,startDate,endDate)
            return {'state':True,'msg':'Success','report':report}
        
if __name__=="__main__":
    fetchData=FetchData()
    cashierActions=CashierActions()
    # #all functions
    eel._expose("getProductsAndBranches",fetchData.getProductsAndBranches)
    eel._expose("getAllTransactions",fetchData.getAllTransactions)
    eel._expose("getAllCustomers",fetchData.fetchAllCustomers)

    eel._expose("payCustomerCredit",cashierActions.payCustomerCredit)
    eel._expose("declareStartingAmount",cashierActions.declareStartingAmount)
    eel._expose("declareClosingAmount",cashierActions.declareClosingAmount)
    eel._expose("registerCustomer",cashierActions.registerCustomer)
    eel._expose("fetchCustomerTotalCredit",cashierActions.fetchCustomerTotalCredit)
    eel._expose("receiveStock",cashierActions.receiveStock)

    eel._expose("generateXReport",cashierActions.genXReport)
    eel._expose("generateZReport",cashierActions.genZReport)
    eel._expose("generateCreditReport",cashierActions.genCreditReport)
    eel._expose("closeShift",cashierActions.closeShift)

    eel.start("login.html",port=4040)