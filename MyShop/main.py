import eel
from utils import Logging
from users import User,Cashier


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
    state,message=c.makeSale(busketList,paymentList,tillId,cashier,custId)
    if(state==False):
        return {"state":False,"message":f"Could Not complete sale: Error=> {message}"}
    return {"state":True}

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
            Logging.consoleLog('message',int(startingAmount))
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
    def payCustomerCredit(userId,tId,custId,creditId,paymentList):
        c=Cashier()
        state,message=c.payCreditSale(userId,tId,custId,creditId,paymentList)
        return {'state':state,'message':message}
    
    @staticmethod
    def receiveStock(userId,busketList):
        c=Cashier()
        state,message=c.receiveStock(userId,busketList)
        return {'state':state,'message':message}
    
    @staticmethod
    def genXReport(shiftId):
        pass

    @staticmethod
    def genZReport(shiftId):
        pass

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

if __name__=="__main__":
    fetchData=FetchData()
    cashierActions=CashierActions()
    # #all functions
    eel._expose("getProductsAndBranches",fetchData.getProductsAndBranches)
    eel._expose("getAllTransactions",fetchData.getAllTransactions)
    eel._expose("getAllCustomers",fetchData.fetchAllCustomers)

    eel._expose("declareStartingAmount",cashierActions.declareStartingAmount)
    eel._expose("declareClosingAmount",cashierActions.declareClosingAmount)
    eel._expose("registerCustomer",cashierActions.registerCustomer)
    eel._expose("fetchCustomerTotalCredit",cashierActions.fetchCustomerTotalCredit)

    eel.start("login.html",port=4040)