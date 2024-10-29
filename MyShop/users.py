class User:
    def __init__(userId):
        pass

    def login(username,password):
        pass
    def logout():
        pass
    def authenticated():
        pass
    def userPermissions():
        pass

class Cashier(User):
    def addSale():
        pass
    def payCreditSale(saleID):
        pass
    def genSalesReport():
        pass

class Admin(Cashier):
    #admin user actions
    def addUser():
        pass
    def deleteUser():
        pass
    def updateUser():
        pass

    #admin stock actions
    def addStock():
        pass
    def deleteStock():
        pass
    def updateStock():
        pass
