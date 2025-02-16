import eel

from users import User,Cashier

pages=["index.html","till.html","admin.html"]

eel.init("web")  

@eel.expose    
def login(username,password):
    u=User()
    auth,message,userLevel,shiftId=u.login(username,password)
    if(auth):
        return {"auth":auth,"token":message,"userLevel":userLevel,"shiftId":shiftId}    
    return {"auth":auth,"message":message,"userLevel":None,"shiftId":None}

@eel.expose
def logOut(userId):
    print("logging out")
    u=User()
    u.logout(int(userId))
    return {"state":True}

@eel.expose
def makeSale(busketList,paymentList,tillId,cashier,custId):
    print("Making Sale")
    c=Cashier()
    state,message=c.makeSale(busketList,paymentList,tillId,cashier,custId)
    if(state==False):
        return {"state":False,"message":"Could Not complete sale"}
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
    def getAllProducts():
        c=Cashier()
        return c.fetchAllProducts()

class CashierActions:
    @staticmethod
    def getAllProducts():
        c=Cashier()
        c.fetchAllProducts()
    @staticmethod
    def declareStartingAmount():
        pass
    @staticmethod
    def declareClosingAmount():
        pass

    @staticmethod
    def payCreditSale():
        print("paying credit sale")

    @staticmethod
    def receiveStock():
        pass
    @staticmethod
    def despatchStock():
        pass

    @staticmethod
    def stockTake():
        pass


    @staticmethod
    def genXReport():
        pass
    @staticmethod
    def genZReport():
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
    
    # #all functions
    eel._expose("getAllProducts",fetchData.getAllProducts)
    

    eel.start("login.html",port=4040)