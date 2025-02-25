from views import UserView,TransactionView,PaymentView,CustomerView
from views import ProductsView,StockView,StockHistoryView,SoldItemsView,CustomerCreditView,ShiftView,BranchesView
from utils import Logging,FormatTime
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
            Logging.consoleLog('succ',f'User access level is correct')
            return True
        else:
            Logging.consoleLog('error',f'User level is {uLevel} and it should be {targetLevel}')
        return False

    def authenticated(self,userToken):
        pass

    def getBranchesList(self):
        branchesList=[]
        branch=BranchesView()
        branchesObj=branch.getAllBranches()
        for b in branchesObj:
            i={
                'id':b.branchId,
                'name':b.branchName,
                'location':b.location,
                'phone':b.branchPhone,
                'tillNumber':b.tillNumber,
                'managerName':b.managerName,
                'managerPhone':b.managerPhone
            }
            branchesList.append(i)
        return branchesList

    def fetchAllProducts(self):
        pV=ProductsView()
        products=pV.getAllProducts()
        pList=[]
        for i in products:
            pList+=[{'id':i.id,'name':i.name,'barCode':i.barCode,'sPrice':i.sellingPrice}]
        return pList
    
    def fetchAllTransactions(self):
        tObject=TransactionView()
        transactionObj=tObject.getAllTransactions()
        transactionsList=[]
        for t in transactionObj:
            transactionsList.append({
                'id':t.id,
                'transactionId':t.transactionId,
                'custId':t.customerId,
                'sellerId':t.sellerId,
                'tillId':t.tillId,
                'saleAmount':t.saleAmount,
                'paidAmount':t.paidAmount,
                'sellDate':FormatTime.dateTimeToStandardTime(t.time),
                'soldItems':self.fetchTransactionSoldItems(t.id)
            })
        return transactionsList

    def fetchTransactionSoldItems(self,tId):
        if(tId!=None):
            s=SoldItemsView()
            soldItemsObj=s.fetchSoldItemsByTransaction(tId)
            soldItems=[]
            p=ProductsView()
            for i in soldItemsObj:
                product=p.getProductByBarCode(i.barCode)
                soldItems.append({'id':i.id,'tId':i.transactionId,'barCode':i.barCode,'name':product.name,'quantity':i.quantity,'soldPrice':i.soldPrice,'discount':i.discountPercent})
            return soldItems
        else:
            return []

    def fetchAllCustomers(self):
        c=CustomerView()
        customers=c.getAllCustomers()
        customersList=[]
        for customer in customers:
            customersList.append({
                "id":customer.id,
                "name":customer.name,
                "phoneNum":customer.phoneNumber,
                "creditOwed":customer.totalCreditOwed
                })
        return customersList

class Cashier(User):

    def declareStartingAmount(self,userId,shiftId,startingAmount):
        auth=super().authUserLevelAction(userId,"cashier")
        state=False
        message='' 
        if(auth):       
            if(shiftId!=None and startingAmount!=None):
                state,message=ShiftView.declareStartingAmount(shiftId,startingAmount)
            else:
                message='None type passed to Cashier.declareStartingAmount()'
        else:
            message='User level permision Access Denied'
        return state,message

    def declareClosingAmount(self,userId,shiftId,closingAmount):
        auth=super().authUserLevelAction(userId,"cashier")
        if(auth):
            state=False
            message=''        
            if(shiftId!=None and closingAmount!=None):
                state,message=ShiftView.declareClosingAmount(shiftId,closingAmount)
            else:
                message='None type passed to Cashier.declareClosingAmount()'
        else:
            message='User level permision Access Denied'
        return state,message
    
    def makeSale(self,busketList,paymentList,tillId,cashierId,custId):
        authAction=super().authUserLevelAction(cashierId,"cashier")
        print(authAction)
        if(authAction):
            payment=PaymentView()
            customerCreditRequest=payment.calcCreditInPayment(paymentList)
            if(customerCreditRequest>=0):
                max_credit=self.maximumCustomerCredit(custId)
                if(customerCreditRequest>max_credit):
                    Logging.consoleLog('error',f"Sale failded because: Requested Credit is {customerCreditRequest} and the maximum credit is {max_credit}")
                    return False,'Customer is only eligable for a maximum credit of {max_credit}'
                
                saleResult=self.handleSale(busketList,paymentList,tillId,cashierId,custId)
                if(saleResult==True):
                    Logging.consoleLog('succ','Sale made successfully')
                    return True,"Sale is successfull"
                else:
                    errorMessage=self.handleSaleRollBack(busketList,paymentList,saleResult)
                    Logging.consoleLog('error',f'There was an error while making the sale: Error=>{errorMessage}')
                    return False,errorMessage
            else:
                Logging.consoleLog('error',f'Transaction credit request is {customerCreditRequest}:Negative value')
        Logging.consoleLog('error',f"You need Cashier user level access to make a sale")
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
            addStockToHist,addStockToHistmsg=self.addStockHistory(tId,'sale',tillId,busketList,cashierId)
            reducedStock,reducedStockmsg=self.reduceStockAfterSale(busketList,cashierId)
            if(addStockToHist and reducedStock):
                return True
            else:
                Logging.consoleLog('error',addStockToHistmsg)
                Logging.consoleLog('error',reducedStockmsg)
                return False
        else:
            logMessage=f'''
                RollBack required while making sale busketList={busketList} paymentList={paymentList} tillId={tillId} cashierId={cashierId} customerId={custId}"\n
                TransactionView.createTransaction() Errors=> state {tState} message {tId}"\n
                PaymentView.addPaymentList() Errors=> state {pState} message {pMessage}\n
                SoldItemsView.addSoldItemsList() Errors=> state {sPState} message {sPMessage}
            '''
            Logging.consoleLog('error',logMessage)
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
    
    def checkForCreditInPayMentList(self,paymentList):
        if(paymentList!=None):
            for payment in paymentList:
                if(payment['paymentType']=='credit'):
                    return True
        return False

    def payCreditSale(self,userId,tId,custId,creditId,paymentList):
        state=False
        message=''
        auth=super().authUserLevelAction(userId,'cashier')
        if(auth):
            if(tId!=None and custId!=None and creditId!=None and paymentList!=None):
                creditInPaymentList=self.checkForCreditInPayMentList(paymentList)
                if(creditInPaymentList==False):
                    c=CustomerCreditView()
                    creditState,message=c.payCredit(custId,creditId,tId,paymentList)
                    if(creditState==True):
                        state=True
                        message='Paid credit successfully'
                    else:
                        message='Error while paying credit'
                else:
                    message='You cannot pay credit with another credit.Please use Mpesa,Bank or Cash'
            else:
                message='Please fill in all the details for credit to be payed: NoneType Passed to Cashier.payCredit()'
        else:
            message='Access Denied user level not permited to payCreditSale'
        Logging.consoleLog('message',message)
        return state,message
    
    def addStockHistory(self,receipt,stockAction,branchId,busketList,userId):
        state=False
        message=''
        if(receipt!=None and stockAction!=None and branchId!=None and busketList!=None and userId!=None):
            pView=ProductsView()
            error=False
            sHMessage=''
            for i in busketList:
                product=pView.getProductByBarCode(i['barCode'])
                sHState,sHMessage=StockHistoryView.addStockHistory(receipt,stockAction,branchId,product.id,product.barCode,i['quantity'],userId)
                if(sHState==False):
                    error=True
            if(error==True):
                message=sHMessage
            else:
                state=True
        else:
            message='None type passed to Cashier.addStockHistory()'
        return state,message

    def reduceStockAfterSale(self,busketList,cashierId):
        state=False
        message=''
        if(busketList!=None and cashierId!=None):
            sV=StockView()
            pView=ProductsView()
            error=False
            for i in busketList:
                product=pView.getProductByBarCode(i['barCode'])
                removedItem,rmessage=sV.removeItems(cashierId,product.id,product.barCode,i['quantity'])
                if(removedItem!=True):
                    error=True
                    message=rmessage
            if(error==False):
                state=True
                message='removed stock after sale'
        else:
            message='None type passed to Cashier.reduceStockAfterSale()'
        return state,message

    def receiveStock(self,cashierId,busketList):
        state=False
        message=''
        auth=super().authUserLevelAction(cashierId,'cashier')
        if(auth):
            if(busketList!=None and cashierId!=None):
                sV=StockView()
                pView=ProductsView()
                error=False
                for i in busketList:
                    product=pView.getProductByBarCode(i['barCode'])
                    removedItem,rmessage=sV.addItems(cashierId,product.id,product.barCode,i['quantity'])
                    if(removedItem!=True):
                        error=True
                        message=rmessage
                if(error==False):
                    state=True
                    message='received stock'
            else:
                message='None type passed to Cashier.receiveStock()'
        else:
            message='Access Denied User level not permited to receive stock'
        return state,message

    def registerCustomer(self,custName,custPhone):
        c=CustomerView()
        state,message=c.addCustomer(custName,custPhone)
        return state,message
    
    def genXReport(self,userId):
        pass

    def genZReport(self,userId):
        pass

    def genCreditReport(self,userId):
        pass

    def stockTake(self,userId):
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
    def addProduct(self,uid,pid,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        auth=super().authUserLevelAction(uid,'admin')
        message=''
        state=False
        if(auth):
            p=ProductsView()
            addedProduct=p.addProduct(pid,pName,barCode,tags,desc,bPrice,sPrice,returnContainers)
            if(addedProduct):
                state=True
                message='Added Product successfully'
            else:
                message='Error while adding product'
        else:
            message='You do not have the required access level to Admin.addProduct()'
        Logging.consoleLog('message',message)
        return state,message
        
    def deleteProduct(self,uid,pid):
        auth=super().authUserLevelAction(uid,'admin')
        state=False
        message=''
        if(auth):
            p=ProductsView()
            deletedProduct=p.deleteProduct(pid)
            if(deletedProduct==True):
                state=True
                message='Product deleted succussfully'
            else:
                message='Error while deleting product'
        else:
            message='You do not have the required access level to Admin.deleteProduct()'
        return state,message

    def updateProduct(self,uid,pid,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        pass

    #admin stock actions
    def editStock(self):
        pass

    def deleteStock():
        pass
    
    def updateStock():
        pass

