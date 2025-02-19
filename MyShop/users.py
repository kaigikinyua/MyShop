from views import UserView,TransactionView,PaymentView
from views import ProductsView,SoldItemsView,CustomerCreditView,ShiftView
from utils import Logging
class User:
    def login(self,username,password):
        if(len(username)>4 and len(password)>7):
            u=UserView()
            auth,token,userLevel=u.login(username,password)
            if(auth):
                userObject=u.getUser(username)
                shiftId=ShiftView.handleShiftOnLogOn(userObject.id)
                if(shiftId!=False and shiftId!=None):
                    return True,token,userLevel,shiftId
                else:
                    return False,None,None,'MultipleShifts'
            else:
                return False,None,None,'Wrong username or password'
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
            payment=PaymentView()
            customerCreditRequest=payment.calcCreditInPayment(paymentList)
            if(customerCreditRequest>0 and customerCreditRequest!=-1):
                max_credit=self.maximumCustomerCredit(custId)
                if(customerCreditRequest>max_credit):
                    return False,'Customer is only eligable for a maximum credit of {max_credit}'
                
                saleResult=self.handleSale(busketList,paymentList,tillId,cashierId,custId)
                if(saleResult==True):
                    return True,"Sale is successfull"
                else:
                    errorMessage=self.handleSaleRollBack(busketList,paymentList,saleResult)
                    return False,errorMessage
        return False,"User level is not cashier"

    def maximumCustomerCredit(self,customerId):
        if(customerId=='null'):
            return False
        c=CustomerCreditView()
        creditWorthy,maxAmount=c.isCustomerCreditWorthy(customerId)
        if(creditWorthy):
            return maxAmount
        return 0

    def handleSale(self,busketList,paymentList,tillId,cashierId,custId):
        payment=PaymentView()
        transaction=TransactionView()
        soldProduct=SoldItemsView()
        #paidAmount,creditAmount=t.calcPaidandCreditAmount(paymentList)
        saleAmount=transaction.calcTotalAmount(paymentList)
        
        tState,tId=transaction.createTransaction(custId,cashierId,tillId,saleAmount)
        pState,pMessage=payment.addPaymentList(paymentList,tId)
        sPState,sPMessage=soldProduct.addSoldItemsList(tId,busketList,True)
        if(tState and pState and sPState):
                return True
        else:
            logMessage=f'''
                RollBack required while making sale busketList={busketList} paymentList={paymentList} tillId={tillId} cashierId={cashierId} customerId={custId}"\n
                TransactionView.createTransaction() Errors=> state {tState} message {tId}"\n
                PaymentView.addPaymentList() Errors=> state {pState} message {pMessage}\n
                SoldItemsView.addSoldItemsList() Errors=> state {sPState} message {sPMessage}
            '''
            Logging.logToFile('error',logMessage)
            return tId
        
    def handleSaleRollBack(self,busketList,paymentList,tId):
        t=TransactionView()
        rollBackState,rollBackMessage=t.rollBackTransaction(tId,paymentList,busketList)
        if(rollBackState==True):
            Logging.consoleLog('warn','Isseue with adding sale to database but completed database rollback successfully')
            return True,'Successfully did the database rollback'
        else:
            Logging.consoleLog('err',rollBackMessage)
            return False,rollBackMessage

    def payCreditSale(saleID,amountPayed,paymentMethod):
        pass
    
    def fetchAllProducts(self):
        pV=ProductsView()
        products=pV.getAllProducts()
        pList=[]
        for i in products:
            pList+=[{'id':i.id,'name':i.name,'barCode':i.barCode,'sPrice':i.sellingPrice}]
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

