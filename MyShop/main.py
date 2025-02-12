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
    def makeSale():
        print("Making a sale")
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
    cashier=CashierActions()
    admin=AdminActions()
    fetchData=FetchData()
    
    #all functions
    eel._expose("getAllProducts",fetchData.getAllProducts)
    
    #cashier functions
    eel._expose("makeSale",cashier.makeSale)
    
    #adminactions
    eel._expose("deleteProduct",admin.deleteProduct)

    eel.start("login.html",port=4040)