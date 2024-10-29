class User:
    def __init__(self):
        pass
    
    def login(self,userId,password):
        pass
    
    def logout(self):
        pass

    def resetPassword(self):
        pass

    def userAuth(self):
        pass
    
class Products:
    def __init__(self,productId,productName):
        if self.productId==None:
            #query in the database products with the matching name and get pId
            pass
        self.productId=productId

    def addProduct(self):
        pass

    def deleteProduct(self):
        pass
    
    def updateProduct(self):
        pass

class Counter:
    def __init__(self):
        pass

    def createCounter(self):
        pass

    def deleteCounter(self):
        pass

    def updateCounter(self):
        pass

    def sellToCounter(self):
        pass

    def addCounterSale(self):
        pass

    def updateCounterSale(self):
        pass

    def counterEndOfDay(self):
        pass

class Customer:
    pass

class Store:
    pass



