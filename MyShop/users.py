from views import UserView,TransactionView,PaymentView,ProductsView,SoldItemsView
from utils import Logging
class User:
    def login(self,username,password):
        if(len(username)>4 and len(password)>7):
            u=UserView()
            auth,token,userLevel,shiftId=u.login(username,password)
            if(auth):
                return True,token,userLevel,shiftId
            return False,token,None,None
        else:
            return False,'Username should be more than 5 characters and Password should 8 or more characters',None

    def logout(self,userId):
        u=UserView()
        if(u.logout(userId)):
            return True
    
    def getUserLevel(self,userId):
        u=UserView()
        user=u.getUserById(userId)
        return user.userLevel

    def authUserLevelAction(self,userId,targetLevel):
        uLevel=self.getUserLevel(userId)
        if(targetLevel==uLevel):
            return True
        return False

    def authenticated(self,userToken):
        pass

class Cashier(User):
    def declareStartingAmount(startingAmount):
        pass

    def declareClosingAmount(closingAmount):
        pass
    
    def makeSale(self,busketList,paymentList,tillId,cashierId,custId):
        authAction=super().authUserLevelAction(cashierId,"cashier")
        if(authAction):
            transaction=TransactionView()
            payment=PaymentView()
            soldProduct=SoldItemsView()

            #paidAmount,creditAmount=t.calcPaidandCreditAmount(paymentList)
            saleAmount=transaction.calcTotalAmount(paymentList)
            
            tState,tId=transaction.createTransaction(custId,cashierId,tillId,saleAmount)
            pState,pMessage=payment.addPaymentList(paymentList,tId)
            sPState,sPMessage=soldProduct.addSoldItemsList(tId,busketList,True)

            if(tState and pState and sPState):
                return True,"Success in adding Transaction,Payments and SoldItems"
            else:
                #RollBack Contigency [delete transaction, delete payments,deleteSoldProducts]
                rollBackState,rollBackMessage=transaction.rollBackTransaction(tId,paymentList,busketList)
                errorMessage=f"Error while adding Transaction,Payments and Sold Items\nTransaction Error {tId}\n\nPayment Error {pMessage}\n\nSoldProduct Error {sPMessage}"
                if(rollBackState!=True):
                    errorMessage+=f"\n\nRollBackError {rollBackMessage}"
                return False,errorMessage
        return False,"User level is not cashier"

    
    def payCreditSale(saleID,amountPayed,paymentMethod):
        pass
    
    def fetchAllProducts(self):
        pV=ProductsView()
        products=pV.getAllProducts()
        pList=[]
        for i in products:
            pList+=[{'id':i.productId,'name':i.name,'barCode':i.barCode,'sPrice':i.sellingPrice}]
        print(pList)
        return pList

    def receiveStock(items,uid):
        pass

    def despatchStock(items,uid):
        pass

    def stockTake():
        pass

    def genXReport():
        pass

    def genZReport():
        pass


class Admin(Cashier):
    #admin user actions
    def addUser(self,username,password,userLevel):
        if(len(username)>4 and len(password)>8 and userLevel!=None):
            newUser=UserView()
            success,message=newUser.addUser(username,password,userLevel)
            if(success):
                Logging.consoleLog('succ','{message}:[{username}] to users')
                return True
            else:
                Logging.consoleLog(message)
                return False
        else:
            Logging.consoleLog('err','Username must have more than 5 characters: {username}')
            Logging.consoleLog('err',"Password must be more than 8 characters: {password}")
            Logging.consoleLog('err',"UserLevel must not be none: {userLevel}")
            return False

    def deleteUser(self,uid):
        pass

    def updateUser(self,uid,username,userLevel):
        pass

    #admin product actions
    def addProduct():
        pass
    def deleteProduct():
        pass
    def updateProduct():
        pass

    #admin stock actions
    def addStock():
        pass
    def deleteStock():
        pass
    def updateStock():
        pass

