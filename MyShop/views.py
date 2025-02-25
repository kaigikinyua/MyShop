from sqlalchemy.orm import sessionmaker

from models import engine,UserModel,AuthModel,ProductsModel,ShiftModel,TransactionModel,StockModel,EmptiesModel,StockHistoryModel
from models import PaymentModel,CustomerModel,SoldItemsModel,SalesSettingsModel,CustomerCreditModel,BranchesModel

from utils import FormatTime,Logging
from settings import Settings

#All the CRUD operations for a model MUST be in a class <modelName>View
class UserView:
    
    #logs in the user plus adds details to the Auth[uId,time,token] and Shift[ShiftId,logins] models
    def login(self,username,password):
        Session=sessionmaker(bind=engine)
        session=Session()
        u=session.query(UserModel).filter_by(name=username,password=password).all()
        if(len(u)==1):
            if(self.is_authenticated(u[0].id)):
                self.logout(u[0].id)
            time=FormatTime.now()
            token=str(time)+':'+str(u[0].name)+':'+str(u[0].id)
            auth=AuthModel(uid=u[0].id,time=time,token=token,active=True)
            userLevel=u[0].userLevel
            session.add(auth)
            session.commit()
            session.close()
            return True,token,userLevel
        return False,None,'Wrong username or password'

    #logs out the user so a new token should be added on next login
    def logout(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        activeSessions=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        #Logging.consoleLog('succ',f'Active sessions to logout={len(activeSessions)}')
        if(len(activeSessions)>0):
            for sess in activeSessions:
                sess.active=False
                session.commit()
                session.close()
                #Logging.consoleLog('succ',f'logging out {sess}')
            return True
        else:
            return False
    
    #gets the users active sessions[where in the AuthModel the active field is True]
    def get_UserActiveSessions(self,username):
        Session=sessionmaker(bind=engine)
        session=Session()
        user=self.getUser(username)
        activeSessions=session.query(AuthModel).filter_by(uid=user.id,active=True).all()
        session.close()
        if(activeSessions!=None and len(activeSessions)>0):
            return activeSessions
        return []
    
    #check whether the user is authenticated
    def is_authenticated(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        auth=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(auth)>0):
            session.close()
            return True
        session.close()
        return False

    #gets the user from the UserModel using username
    def getUser(self,username):
        Session=sessionmaker(bind=engine)
        session=Session()
        user=session.query(UserModel).filter_by(name=username).one_or_none()
        if(user!=None):
            return user
        else:
            return None
    
    #get user from UserModel using userId
    def getUserById(self,userId):
        Session=sessionmaker(bind=engine)
        session=Session()
        users=session.query(UserModel).filter_by(id=userId).one_or_none()
        if(users!=None):
            return users
        else:
            return None
    
    #creates a new user while checking for name collisions
    def addUser(self,username,userpassword,userLevel):
        if(username!=None and userpassword!=None and userLevel!=None):
            if(len(username)<4 or len(userpassword)<8):
                return False,'Username is less than 4 characters or password is less than 8 characters'
            Session=sessionmaker(bind=engine)
            session=Session()
            collision_name=session.query(UserModel).filter_by(name=username).all()
            
            if(collision_name!=None and len(collision_name)>0):
                return False,'User name collision'
            else:
                ulevel=UserModel.usrLevelChoices[userLevel]
                user=UserModel(name=username,password=userpassword,userLevel=ulevel)
                #add checks incase database failed connection
                session.add(user)
                session.commit()
                return True,'Added user'
        else:
            return False,'Make sure the username and password is not empty'

    def updateUserLevel(self,uid,userLevel):
        if(uid!=None and userLevel!=None):
            Session=sessionmaker()
            session=Session()
            user=session.query(UserModel).filter_by(id=uid).one_or_none()
            if(user!=None):
                user.userLevel=UserModel.usrLevelChoices[userLevel]
                session.commit()
                Logging.consoleLog("warn",f"Updated user id={uid} name={user.name} level to {userLevel}")
                return True,f'Updated user level to {userLevel}'
            else:
                session.close()
                return False,f'There is no user by id {uid}'
        return False,'Ensure the username, userid and userlevel are not empty'
        
    def updatePassword(self,uid,newPassword):
        if(uid!=None and newPassword!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            user=session.query(UserModel).filter_by(id=uid).one_or_none()
            if(user!=None):
                user.password=newPassword
                session.commit()
                return True,'Updated user password'
            session.close()
        return False,'Ensure the uid and new password is not empty'

    def deleteUser(self,uId):
        if(uId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            user=session.query(UserModel).filter_by(id=uId).one_or_none()
            if(user!=None):
                session.delete(user)
                session.commit()
                Logging.logToFile('warn',f'Deleted user id={user.id} name={user.name} level={user.userLevel}')
                return True,f'Deleted user with id of {uId}'
            else:
                return False,f'There is no user by id {uId}'
        return False,f'User id to be deleted cannot be empty'

    def getAllUsers(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        users=session.query(UserModel).all()
        return users

class ShiftView:
    @staticmethod
    def openShift(openningId=0):
        sId=ShiftView.createShiftId()
        sId=ShiftView.createShift(sId,openningId,False)
        return sId      

    @staticmethod
    def shiftIsOpen(shiftId):
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).filter_by(shiftId=shiftId,isClosed=False).all()
        if(openShifts!=None and len(openShifts)==1):
            return True
        elif(openShifts!=None and len(openShifts)==0):
            Logging.consoleLog('warn',f'There is no open shift by shiftId {shiftId} {openShifts}')
        elif(len(openShifts)>1):
            Logging.consoleLog('err',f'There is more than one shift with id {shiftId}')
        return False
    
    @staticmethod
    def getOpenShifts():
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).filter_by(isClosed=False).all()
        if(len(openShifts)<=0 or openShifts==None):
            Logging.consoleLog('succ',f'Number of open shifts are {len(openShifts)}')
            return []
        else:
            Logging.consoleLog('error',f'There are {len(openShifts)} open shifts')
            return openShifts

    @staticmethod
    def closeShift(shiftId):
        if(shiftId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            shift=session.query(ShiftModel).filter_by(shiftId=shiftId)
            if(shift!=None):
                shift.isClosed=True
                shift.endTime=FormatTime.now()
                session.commit()
                return True,'Shift is now closed'
            return None,f'Shift by shift id {shiftId} could not be found'
        return False,'None parameter passed to ShiftView.closeShift()'
    
    @staticmethod
    def createShiftId():
        timeStamp=FormatTime.now()
        settings=SaleSettingsView.getSalesSettings()
        if(settings!=None):
            tillId=settings.tillId
        else:
            tillId=Settings.tillId()
        return f'{tillId}|{timeStamp}'

    @staticmethod
    def getOpenShiftTime():
        shift=ShiftView.getOpenShifts()
        if(shift!=None and len(shift)==1):
            startTime=shift[0].startTime
            endTime=shift[0].endTime
            if(endTime==None):
                endTime=FormatTime.now()
            return startTime,endTime

    @staticmethod
    def getOpenShiftObj():
        shifts=ShiftView.getOpenShifts()
        if(len(shifts)==1):
            return shifts[0]
        else:
            return None
    
    @staticmethod
    def addLogin(shiftId):
        Session=sessionmaker(bind=engine)
        session=Session()
        shift=session.query(ShiftModel).filter_by(shiftId=shiftId).all()
        if(len(shift)==1):
            shift[0].logins=shift[0].logins+1
            session.commit()
            return True
        return False

    @staticmethod
    def handleShiftOnLogOn(userId):
        openShifts=ShiftView.getOpenShifts()
        shiftId=False
        if(len(openShifts)==0):
            shiftId=ShiftView.openShift(userId)
        elif(len(openShifts)==1):
            addedLogin=ShiftView.addLogin(openShifts[0].shiftId)
            if(addedLogin):
                shiftId=openShifts[0].shiftId
            else:
                Logging.consoleLog('error','Could not add the login to already open')
        else:
            Logging.consoleLog('error',f'There are {len(openShifts)} already open and maximum open shifts should be 1')
        return shiftId

    @staticmethod
    def declareStartingAmount(shiftId,startingAmount):
        message=''
        if(startingAmount>=0 and shiftId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            shift=session.query(ShiftModel).filter_by(shiftId=shiftId,startingAmount=-1).one_or_none()
            if(shift!=None):
                shift.startingAmount=startingAmount
                session.commit()
                session.close()
                return True,'Declared starting amount'
            else:
                session.close()
                return False,f'No shift with shift id {shiftId} and starting amount {-1}'
        else:
            message=f'None type or non-negative type passed to Shift.declareStartingAmount(): statringAmount={startingAmount} shiftId={shiftId}'
            Logging.consoleLog('error',message)
        return False,message

    @staticmethod
    def declareClosingAmount(shiftId,closingAmount):
        message=''
        if(closingAmount>=0 and shiftId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            shift=session.query(ShiftModel).filter_by(shiftId=shiftId,closingAmount=-1).one_or_none()
            message=''
            if(shift!=None):
                shift.closingAmount=closingAmount
                session.commit()
                session.close()
                return True,'Declared Closing Amount'
            else:
                session.close()
                return False,f'No shift with shift id {shiftId} and closing amount {-1}'
        else:
            message=f'None type or non-negative type passed to Shift.declareStartingAmount(): closingAmount={closingAmount} shiftId={shiftId}'
        return False,message

    @staticmethod
    def createShift(shiftId,openningId,isClosed):
        if(shiftId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            sDate=FormatTime.getDateToday()
            sTime=shiftId.split('|')[1]
            eTime=None
            shift=ShiftModel(
                shiftId=shiftId,
                shiftDate=sDate,
                startingAmount=-1,
                closingAmount=-1,
                openningId=openningId,
                closingId=0,
                logins=1,
                isClosed=isClosed,
                startTime=sTime,
                endTime=eTime    
            )
            
            session.add(shift)
            session.commit()
            session.close()
            return True,shiftId
        return False,'None Parameter passed to ShiftView.createShift()'
    
    @staticmethod
    def deleteShift(shiftId):
        if(shiftId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            shift=session.query(ShiftModel).filter_by(shiftId=shiftId).one_or_none()
            if(shift!=None):
                session.delete(shift)
                session.commit()
                session.close()
                return True,'Shift deleted successfully'
            return False,f'No shift by {shiftId} was found'
        return False,f'None parameter passed to ShiftView.deleteShift()'

    @staticmethod
    def getAllShifts():
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).all()
        session.close()
        return openShifts
    
class ProductsView:
    def addProduct(self,id,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        if(len(pName)>0 and len(barCode)>0 and bPrice!=None and sPrice!=None and returnContainers!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            noCollisionBarCode=session.query(ProductsModel).filter_by(barCode=barCode).one_or_none()
            noCollisionId=session.query(ProductsModel).filter_by(id=id).one_or_none()
            if(noCollisionBarCode==None and noCollisionId==None):
                p=ProductsModel(id=id,name=pName,barCode=barCode,buyingPrice=bPrice,sellingPrice=sPrice,returnContainers=returnContainers,productTags=tags,desc=desc)
                session.add(p)
                session.commit()
                return True
            Logging.consoleLog('error','Id or BarCode collision detected while trying to add product')
            return False
        else:
            return False
    
    def getAllProducts(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        result=session.query(ProductsModel).all()
        return result
    
    def getProductById(self,pId):
        if(pId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            result=session.query(ProductsModel).filter_by(id=pId).one_or_none()
            return result
        else:
            return False
    
    def getProductByBarCode(self,barcode):
        if(len(barcode)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            result=session.query(ProductsModel).filter_by(barCode=barcode).one_or_none()
            return result
        else:
            return False
        
    def updateProduct(self,pId,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        if(len(pId)>0 and len(pName)>0 and len(barCode)>0 and bPrice!=None and sPrice!=None and returnContainers!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            p=session.query(ProductsModel).filter_by(productId=pId).one_or_none()
            if(p!=None):
                p.name=pName
                p.barCode=barCode
                p.buyingPrice=bPrice
                p.sellingPrice=sPrice
                p.returnContainers=returnContainers
                p.productTags=tags
                p.desc=desc
                session.commit()
                return True,''
            else:
                return False,f'Product {pId} not found'
        return False,f'One or more required fields are empty: Pid={pId} name={pName}'
    
    def deleteProduct(self,pId):
        if(pId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            p=session.query(ProductsModel).filter_by(id=pId).one_or_none()
            if(p!=None):
                session.delete(p)
                session.commit()
                session.close()
                Logging.consoleLog('warn',f'Deleted product with pid {pId}')
                return True
            else:
                Logging.consoleLog(f'There is no product that has product id {pId}')
            return False,''
        else:
            return False,'Product id is empty Pid={pId}'

class CustomerView:
    def addCustomer(self,custName,phoneNumber):
        if(custName!=None and phoneNumber!=None):
            if(self.customerAlreadyExists(phoneNumber)==False):
                Session=sessionmaker(bind=engine)
                session=Session()
                customer=CustomerModel(name=custName,phoneNumber=phoneNumber,totalCreditOwed=0)
                session.add(customer)
                session.commit()
                session.close()
                return True,'Customer Added successfully'
            return False,'Customer Phone Number Already Exists'
        else:
            return False,'None type passed to CustomerView.addCustomer()'
        
    def getCustomer(self,custId):
        if(custId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            return session.query(CustomerModel).filter_by(id=custId).one_or_none()
        else:
            return False,'Passed a None Parameter to CustomerView.getCustomer()'

    def getCustomerByPhoneNumber(self,phone):
        if(phone!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            cust=session.query(CustomerModel).filter_by(phoneNumber=phone).one_or_none()
            return cust
        else:
            return False,'Passed a None Parameter to CustomerView.getCustomerByPhoneNumber()'

    def getAllCustomers(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        return session.query(CustomerModel).all()

    def updateCustomerDetails(self,custId,custName,phoneNumber):
        if(custId!=None and len(custName)>0 and len(phoneNumber)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            c=session.query(CustomerModel).filter(id=custId)
            c.name=custName
            c.phoneNumber=phoneNumber
            session.commit()
            return True
        else:
            return False
        
    def deleteCustomer(self,custId):
        Session=sessionmaker(bind=engine)
        session=Session()
        result=session.query(CustomerModel).filter_by(id=custId).one_or_none()
        if(result!=None):
            session.delete(result)
            session.commit()
            return True
        return False
    
    def getCustomerTransactions(self,custId):
        if(custId!=None):
            t=TransactionView()
            return t.filterTransactionByCustomer(custId)
        else:
            return False

    def customerAlreadyExists(self,phoneNumber):
        Session=sessionmaker(bind=engine)
        session=Session()
        pNumberExists=session.query(CustomerModel).filter_by(phoneNumber=phoneNumber).all()
        if(len(pNumberExists)>0):
            #print(pNumberExists[0].phoneNumber)
            return True
        return False

class TransactionView:
    def createTransaction(self,custId,sellerId,tillId,saleAmount):
        if(custId!=None and sellerId!=None and tillId!=None):
            if(int(saleAmount)):
                time_id=FormatTime.now()
                t=TransactionModel()
                t.transactionId=tillId+str(time_id)
                t.customerId=custId
                t.sellerId=sellerId
                t.tillId=tillId
                t.saleAmount=int(saleAmount)
                t.paidAmount=0
                t.time=time_id

                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(t)
                session.commit()
                session.close()
                return True,t.transactionId
            else:
                return False,"Either saleamount or paidamount could not be typecasted to integer"
        else:
            return False,f"There could be a null value passed to function TransactionView.createTransaction()\ncustomerId {custId} sellerId {sellerId} tillId {tillId} saleAmount {saleAmount}"
    
    def deleteTransaction(self,tId):
        if(tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            t=session.query(TransactionModel).filter_by(transactionId=tId).one_or_none()
            if(t!=None):
                session.delete(t)
                session.commit()
                session.close()
                transactionString=f'[id:{t.id},transactionId:{t.transactionId},customerId:{t.customerId},sellerId:{t.sellerId},tillId:{t.tillId},paidAmount:{t.paidAmount},time:{t.time}]'
                Logging.logToFile('warn',f'Deleted transaction{transactionString}')
                return True,'Deleted transaction with tranactionId{tId}'
            else:
                return False,f'There is no transaction with transactionId {tId}'
        return False,'Parameter "tId" to function deleteTransaction(tId) is "None"'
        
    def rollBackTransaction(self,tId,paymentList,busketList):
        payment=PaymentView()
        product=SoldItemsView()
        message=""
        delPaymentState,delPaymentMessage,failedToDelete=payment.deletePaymentList(paymentList,tId)
        deletedProductsState,delProductsMessage=product.rollBackSoldItems(tId,busketList)
        delTransactionState,delTransactionMessage=self.deleteTransaction(tId)
        if(delPaymentState==True and delTransactionState==True and deletedProductsState==True):
            return True,f'Rolled back successfull'
        if(delPaymentState==False):
            message+=delPaymentMessage+'\n'
        if(delTransactionState==False or deletedProductsState==False):
            message+=delTransactionMessage+'\n'+delProductsMessage
        return False,message

    def fetchTransactionById(self,tId):
        if(tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            transactions=session.query(TransactionModel).filter_by(transactionId=tId).first()
            session.close()
            return transactions
        return None
    
    def filterTransactionByPeriod(self,startDate,endDate):
        if(startDate!=None and endDate!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            transactions=session.query(TransactionModel).filter(TransactionModel.time>=startDate,TransactionModel.time<=endDate)
            session.close()
            return transactions
        else:
            Logging.consoleLog('error','None Type passed to TransactionView.filterTransactionByPeriod(startDate,endDate)')
            return []
        
    def filterTransactionByCustomer(self,custId):
        if(len(custId)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            customerTransasctions=session.query(TransactionModel).filter_by(customerId=custId).all()
            session.close()
            return customerTransasctions
        else:
            return False
        
    def fetchAllTransactions(self,startTime,endTime):
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startTime!=None and endTime!=None):
            return session.query(TransactionModel).filter(TransactionModel.time>=startTime,TransactionModel.time<=endTime)
        else:
            Logging.consoleLog('error',f'Could not get transactions between {startTime} and {endTime}')
            return self.getAllTransactions()

    def updatePaidAmount(self,tId,addAmount):
        try:
            addAmount=int(addAmount)
        except:
            return False
        if(tId!=None and addAmount!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            t=session.query(TransactionModel).filter_by(transactionId=tId).first()
            t.paidAmount=t.paidAmount+int(addAmount)
            session.commit()
            return True
        return False

    def calcPaidandCreditAmount(self,paymentList):
        paidAmount=0
        creditAmount=0
        for p in paymentList:
            if(p["paymentType"]=="credit"):
                creditAmount=creditAmount+int(p["amount"])
            else:
                paidAmount=paidAmount+int(p["amount"])
        return paidAmount,creditAmount
    
    def calcTotalAmount(self,paymentList):
        total=0
        for p in paymentList:
            total=total+int(p["amount"])
        return total

    def getAllTransactions(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        return session.query(TransactionModel).all()

class PaymentView:
    def addPayment(self,paymentMethod,paymentAmount,transactionId,transactionCredentials,paymentTime):
        t=TransactionView()
        tr=t.fetchTransactionById(transactionId)
        if(tr==None):
            #no transaction whose id=transactionId hence no payment can be made
            return False,f'There is no transaction whose with transactionId={transactionId}'
        if(len(paymentMethod)>0 and paymentAmount>0 and len(transactionId)>0 and paymentTime!=None):
            bal=self.balanceOnPayment(transactionId,paymentAmount)
            if(bal>=0):
                payment=PaymentModel()
                payment.transactionId=transactionId
                payment.paymentMethod=paymentMethod
                payment.amountPayed=paymentAmount
                payment.time=paymentTime
                if(paymentMethod=='mpesa'):
                    payment.mpesaTransaction=transactionCredentials
                elif(paymentMethod=='bank'):
                    payment.bankAcc=transactionCredentials
                elif(paymentMethod=='cash'):
                    payment.mpesaTransaction='None;Cash'
                    payment.bankAcc='None;Cash'
                else:
                    return False,f'Payment method {paymentMethod} is not implemented in PaymentView.addPayment()'
                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(payment)
                rslt=t.updatePaidAmount(transactionId,paymentAmount)
                if(rslt):
                    session.commit()
                    return True,'Completed Successfully'
                else:
                    session.rollback()
                    return False,'An error occured during payment hence rollback database'
            elif(bal<0):
                return False,f'The customer will have paid exess of {bal*-1}'
        else:
            #one or some of the parameters are none
            return False,'None parameter passed to addPayment(self,paymentMethod,paymentAmount,transactionId,transactionCredentials,paymentTime)'
    
    def addPaymentList(self,paymentList,tId):
        if(len(paymentList)>0 and tId!=None):
            allPaymentsDone=True
            errorMessage=None
            paymentTime=FormatTime.now()
            for p in paymentList:
                transactionCredentials="None"
                pMethod=p["paymentType"]
                if(pMethod!='credit'):
                    if(pMethod=='mpesa'):
                        transactionCredentials=p["phoneNum"]+';'+p["mpesaTid"]
                    elif(pMethod=='bank'):
                        transactionCredentials=p["bankName"]+';'+p["bankAccNumber"]
                    pState,pmessage=self.addPayment(p["paymentType"],int(p["amount"]),tId,transactionCredentials,paymentTime)
                    if(pState==False):
                        allPaymentsDone=False
                        errorMessage=pmessage
            if(allPaymentsDone):
                return True,"Transaction success"
            else:
                Logging.logToFile(f"One or more payments failed to be added to the database {errorMessage}")
                return False,f"One or more payments failed to be added to the database {errorMessage}"
        else:
            return False,"None Parameter passed to function addPaymentList(paymentList,tId)"

    def deletePayment(self,tId,payment):
        if(tId!=None and payment!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            p=session.query(PaymentModel).filter_by(transactionId=tId,paymentMethod=payment["paymentType"],amountPayed=payment["amount"]).first()
            if(p!=None):
                session.delete(p)
                session.commit()
                paymentString=f'[id:{p.id},transactionId:{p.transactionId},paymentMethod:{p.paymentMethod},amountPayed:{p.amountPayed},time:{p.time},bankAcc:{p.bankAcc},mpesaTransaction:{p.mpesaTransaction}]'
                Logging.logToFile('warn',f'Deleted payment {paymentString}')
                return True,'Deleted Payment with transactionId {tId}'
            else:
                return False,f'There is no payment with transactionId {tId}'
        return False,'Parameter "tId" to function deletePayment(tId) is "None"'
    
    def deletePaymentList(self,paymentList,tId):
        if(paymentList!=None and len(paymentList)>0):
            failedToDelete=[]
            for p in paymentList:
                payment={"paymentType":p["paymentType"],"amount":p["amount"]}
                state,message=self.deletePayment(tId,payment)
                if(state!=True):
                    failedToDelete+=p
            if(len(failedToDelete)==0):
                return True,'Deleted all payments',failedToDelete
            else:
                return False,f'Failed to delete all payments',failedToDelete
        return False,'None "paymentList" passed to deletePaymentList(paymentList)'

    def settledPayment(self,tId):
        if(tId!=None):
            t=TransactionView()
            transaction=t.fetchTransactionById(tId)
            if(transaction==None):
                return None
            if(transaction.saleAmount>transaction.paidAmount):
                return False
            elif(transaction.saleAmount==transaction.paidAmount):
                return True 
        else:
            return None
        
    def balanceOnPayment(self,tId,additionalAmount):
        t=TransactionView()
        transaction=t.fetchTransactionById(tId)
        if(transaction!=None):
            diff=transaction.saleAmount-(transaction.paidAmount+int(additionalAmount))
            #diff>0 - customer needs to top up
            #diff<0 -customer has paid excess
            return diff

    def payCredit(self,paymentMethod,paymentAmount,tId,creditId,transactionCredentials,paymentTime):
        state=False
        message=''
        if(paymentMethod!=None and paymentAmount>0 and tId!=None and creditId!=None and transactionCredentials!=None and paymentTime!=None):
            t=TransactionView()
            tr=t.fetchTransactionById(tId)
            if(tr==None):
                #no transaction whose id=transactionId hence no payment can be made
                message=f'There is no transaction whose with transactionId={tId}'
            else:
                payment=PaymentModel()
                payment.transactionId=tId
                payment.paymentMethod=paymentMethod
                payment.paidForCreditId=creditId
                payment.amountPayed=paymentAmount
                payment.time=paymentTime
                if(paymentMethod=='mpesa'):
                    payment.mpesaTransaction=transactionCredentials
                elif(paymentMethod=='bank'):
                    payment.bankAcc=transactionCredentials
                elif(paymentMethod=='cash'):
                    payment.mpesaTransaction='None;Cash'
                    payment.bankAcc='None;Cash'
                rslt=t.updatePaidAmount(tId,paymentAmount)
                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(payment)
                rslt=t.updatePaidAmount(tId,paymentAmount)
                if(rslt):
                    session.commit()
                    state=True
                    message='Completed Successfully'
                else:
                    session.rollback()
                    message='An error occured during credit payment hence rollback database'
        else:
            message='None type passed to PaymentView.payCredit()'
        return state,message

    def calcCreditInPayment(self,paymentList):
        if(paymentList!=None and len(paymentList)>0):
            total=0
            for p in paymentList:
                if(p["paymentType"]=='credit'):
                    total=total+p['amount']
            return total
        return -1,

    def fetchTransactionPayments(self,tId):
        if(tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            return session.query(PaymentModel).filter_by(transactionId=tId).all()
        else:
            #return error message tId is empty
            return None

    def fetchAllPaymentsWithinPeriod(self,startTime,endTime):
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startTime!=None and endTime!=None):
            return session.query(PaymentModel).filter(PaymentModel.time>=startTime,PaymentModel.time<=endTime).all()
        else:
            Logging.consoleLog('error',f'Could not get all payments between {startTime} and {endTime}')
            return self.getAllPayments()

    def fetchPaymentsByTimeAndPaymentMethod(self,startTime,endTime,paymentMethod):
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startTime!=None and endTime!=None):
            return session.query(PaymentModel).filter(PaymentModel.time>=startTime,PaymentModel.time<=endTime,paymentMethod=paymentMethod).all()
        else:
            return None

    def calcTotal(self,payments):
        total=0
        for p in payments:
            total=total+p.amountPayed
        return total

    def getAllPayments(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        return session.query(PaymentModel).all()

class CustomerCreditView:

    def payCredit(self,custId,creditId,tId,paymentList):
        if(paymentList!=None and tId!=None):
            creditBalance=self.creditBalance(custId,creditId,tId)
            creditObj=self.fetchCreditById(custId,creditId)
            p=PaymentView()
            amount=p.calcTotal(paymentList)
            if(creditBalance>=amount):
                payTime=FormatTime.now()
                error=False
                for pay in paymentList:
                    rslt,message=p.payCredit(pay['paymentType'],pay['amount'],tId,creditId,pay['credentials'],payTime)
                    if(rslt==None or rslt==False):
                        error=True
                if(error==False):
                    creditObj.totalCreditPaid=creditObj.totalCreditPaid+amount
                    Session=sessionmaker(bind=engine)
                    session=Session()
                    session.add(creditObj)
                    session.commit()
                    session.close()
                else:
                    #initiate rollback
                    pass
            else:
                return False,f'Customer will have overpaid the credit balance Credit Balance={creditBalance} amount paid={amount}'
        return False,'None parameter passed to payCredit(self,custId,tId,paymentMethod,amount,transactionCredentials,creditId)'

    def addCredit(self,custId,tId,cAmount,cDeadline):
        state=False
        message=''
        if(custId!=None and tId!=None and cAmount!=None and cDeadline!=None):
            creditExists=self.fetchCreditTransactionByCustomer(custId,tId)
            if(creditExists==None):
                customerCredit=CustomerCreditModel()
                customerCredit.customerId=custId
                customerCredit.transactionId=tId
                customerCredit.creditAmount=cAmount
                customerCredit.totalCreditPaid=0
                customerCredit.creditDeadline=cDeadline
                customerCredit.fullyPaid=False
                customerCredit.time=FormatTime.now()

                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(customerCredit)
                session.commit()
                state=True
                message='Credit added'
            else:
                message='Credit Transaction already Exists'
        else:
            message='Credit could not be added'
        return state,message

    def creditBalance(self,custId,creditId,tId):
        if(custId!=None and tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            credit=session.query(CustomerCreditModel).filter_by(customerId=custId,id=creditId,transactionId=tId).one_or_none()
            if(credit!=None):
                balance=credit.creditAmount-credit.totalCreditPaid
                return balance
            else:
                return False,f'Çustomer credit record [Customer id {custId} Transaction id {tId}] could not be found'

        return False,'None value passed to creditFullySettled(self,custId,tId)'

    def calcTotalCustomerCredit(self,custId):
        if(custId!=None):
            debtList=self.fetchAllCreditTransactionsByCustomer(custId,False)
            totalDebt=0
            transactionIds=[]
            for debt in debtList:
                totalDebt=totalDebt+(debt.creditAmount-debt.totalCreditPaid)
                transactionIds.append(debt.transactionId)
            return totalDebt,transactionIds
        return False,'None parameter passed to calcTotalCustomerCredit(self,custId)'
    
    def isCustomerCreditWorthy(self,custId):
        if(custId!=None):
            totalCredit,creditTransactions=self.calcTotalCustomerCredit(custId)
            sSettings=SaleSettingsView.fetchSettings()
            if(totalCredit<sSettings.maxCustomerCredit):
                return True,sSettings.maxCustomerCredit-totalCredit
            else:
                return False,0
        return False,'None paramenter passed to CustomerCreditView.isCustomerCreditWorthy()'
    
    def fetchCreditById(self,custId,creditId):
        if(custId!=None and creditId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            credit=session.query(CustomerCreditModel).filter_by(id=creditId,customerId=custId).one_or_none() 
            session.close()
            if(credit!=None):
                return credit
        return None

    def fetchCreditTransactionByCustomer(self,custId,tId):
        if(custId!=None and tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            credit=session.query(CustomerCreditModel).filter_by(transactionId=tId,customerId=custId).one_or_none() 
            session.close()
            if(credit!=None):
                return credit
            else:
                return None
        return False
    
    def fetchAllCreditTransactionsByCustomer(self,custId,creditState=False):
        Session=sessionmaker(bind=engine)
        session=Session()
        allCredit=session.query(CustomerCreditModel).filter_by(fullyPaid=creditState,customerId=custId).all()
        session.close()
        if(len(allCredit)>0):
            return allCredit
        return []    

    def fetchUnpaidCreditByCustomer(self,custId):
        credit=self.fetchCreditByCustomer(custId,False)
        if(credit!=None):
            return credit
        return []
    
    def fetchPaidCreditByCustomer(self,custId):
        credit=self.fetchCreditByCustomer(custId,True)
        if(credit!=None):
            return credit
        return []

    def fetchCreditWithinPeriod(self,startTime,endTime,paid):
        Session=sessionmaker(bind=engine)
        session=Session()
        creditSales=session.query(CustomerCreditModel).filter_by(CustomerCreditModel.time>=startTime,CustomerCreditModel.time<=endTime,fullyPaid=paid).all()
        return creditSales

    def calcTotalCreditByCustomer(self,creditList):
        if(len(creditList)>0):
            paidTotal=0
            unPaidTotal=0
            for c in creditList:
                paidTotal=paidTotal+creditList.totalCreditPaid
                unPaidTotal=unPaidTotal+creditList.creditAmount
            return paidTotal,unPaidTotal
        return 0,0

    def createCreditReportFromList(self,creditList):
        c=CustomerView()
        p=PaymentView()
        sItem=SoldItemsView()
        report=[]
        for credit in creditList:
            customer=c.getCustomer(credit.customerId)
            soldItems=sItem.fetchSoldItemsByTransaction(credit.transactionId)
            payments=p.fetchTransactionPayments(credit.transactionId)
            r={
                'name':customer.name,
                'system id':customer.id,
                'phone':customer.phoneNumber,
                'transactionId':credit.transactionId,
                'credit':credit.creditAmount,
                'paid':credit.totalCreditPaid,
                'deadline':credit.creditDeadline,
                'payments':payments,
                'products':soldItems,
                }
            report.append(r)
        return report

    def calcTotalCredit(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        unpaidCredit=session.query(CustomerCreditModel).filter_by(fullyPaid=False).all()
        total=0
        for credit in unpaidCredit:
            total=total+(credit.creditAmount-credit.totalCreditPaid)
        return total

    def calcTotalCreditFromCreditList(self,creditList):
        total=0
        for credit in creditList:
            total=total+(credit.creditAmount-credit.totalCreditPaid)
        return total

    def fetchCreditList(self,fullyPaid=False):
        Session=sessionmaker(bind=engine)
        session=Session()
        allCredit=session.query(CustomerCreditModel).filter_by(fullyPaid=fullyPaid).all()
        return allCredit
    
    def getAllCredit(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        allCredit=session.query(CustomerCreditModel).all()
        return allCredit

class SoldItemsView:
    def addSoldItem(self,tId,productId,barCode,quantity,actualSellingPrice,itemsCollected):
        if(tId!=None and productId!=None and quantity!=None and actualSellingPrice!=None and itemsCollected!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            bp=session.query(ProductsModel).filter_by(id=productId).one_or_none()
            if(bp!=None):
                buyingPrice=bp.buyingPrice
                productSellingPrice=bp.sellingPrice
                discountPercent=((productSellingPrice-actualSellingPrice)/productSellingPrice)*100
                if(actualSellingPrice>buyingPrice):
                    t=FormatTime.now()
                    soldItem=SoldItemsModel(transactionId=tId,productId=productId,barCode=barCode,soldPrice=actualSellingPrice,expectedSellingPrice=productSellingPrice,discountPercent=discountPercent,buyingPrice=buyingPrice,quantity=quantity,itemsCollected=itemsCollected,time=t)
                    session.add(soldItem)
                    session.commit()
                    return True,'Success: Item has been sold '
                else:
                    return False,'You are selling at a loss'
            else:
                return False,bp
        else:
            return False,'None parameter passed to addSoldItem(tId,productId,quantity,actualSellingPrice,itemsCollected)'
    
    def deleteSoldItem(self,tId,productId,barCode):
        if(tId!=None and productId!=None and barCode!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            sp=session.query(SoldItemsModel).filter_by(transactionId=tId,productId=productId,barCode=barCode).one_or_none()
            if(sp!=None):
                p={
                    "id":sp.id,
                    "transactionId":sp.transactionId,
                    "productId":sp.productId,
                    "barCode":sp.barCode,
                    "quantity":sp.quantity,
                    "soldPrice":sp.soldPrice,
                    "expectedSellingPrice":sp.expectedSellingPrice,
                    "itemsCollected":sp.itemsCollected,
                    "time":sp.time
                    }
                session.delete(sp)
                session.commit()
                Logging.logToFile('warn',f'Deleted Sold Item {p}')
            return False,f'Sold Product from transaction {tId} was not saved to database transactionId={tId} productId={productId} barCode={barCode}'
        return False,'None parameter passed to SoldItemsView.deleteSoldItem(self,tId,productId,barCode)'

    def addSoldItemsList(self,tId,soldItemsList,itemsCollected):
        if(tId!=None and len(soldItemsList)>0 and itemsCollected!=None):
            error=False
            message=""
            pView=ProductsView()
            for item in soldItemsList:
                product=pView.getProductByBarCode(item['barCode'])
                if(product!=False):
                    soldItemState,soldItemMessage=self.addSoldItem(tId,product.id,product.barCode,item['quantity'],item["price"],itemsCollected)
                    if(soldItemState==False):
                        error=True
                        message=message+soldItemMessage
            if(error==False):
                return True,'Added all the products to SoldItemsList'
            else:
                return False,message
        else:
            return False,'None passed as a parameter to addSoldItemsList(tId,soldItemsList,itemsCollected)'

    def rollBackSoldItems(self,tId,soldItemsList):
        if(tId!=None and len(soldItemsList)>0):
            error=False
            message=""
            for item in soldItemsList:
                pView=ProductsView()
                product=pView.getProductByBarCode(item['barCode'])
                if(product!=False):
                    deletedItemState,deletedItemMessage=self.deleteSoldItem(tId,product.id,product.barCode)
                    if(deletedItemState==False):
                        error=True
                        message=message+deletedItemMessage
            if(error==False):
                return True,'Rolled back all the products'
            else:
                return False,message

    def fetchSoldItemsByTransaction(self,tId):
        Session=sessionmaker(bind=engine)
        session=Session()
        soldItems=session.query(SoldItemsModel).filter_by(transactionId=tId).all()
        return soldItems

    def fetchSoldItemsByDate(self,timeBegin,timeEnd):
        if(timeBegin!=None and timeEnd!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            soldItems=session.query(SoldItemsModel).filter(SoldItemsModel.time>=timeBegin,SoldItemsModel.time<=timeEnd)
            return soldItems
        else:
            Logging.consoleLog('error',f'None type passed to SoldItemsView.fetchSoldItemsByDate()')
            return []

    def fetchReservedItems(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        reservedItems=session.query(SoldItemsModel).filter_by(itemsCollected=False)
        return reservedItems

    def collectReservedItems(self,transactionId):
        if(transactionId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            reservedItems=session.query(SoldItemsModel).filter_by(transactionId=transactionId,itemsCollected=False)
            if(reservedItems!=None and len(reservedItems)>0):
                for item in reservedItems:
                    item.itemsCollected=True
                session.commit()
            return True
        else:
            Logging.consoleLog('error','None Type passes to SoldItemsView.collectReservedItems')
            return False

    def getAllReservedItems(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        reservedItems=session.query(SoldItemsModel).filter_by(itemsCollected=False)
        return reservedItems
    
class SaleSettingsView:
    def addSalesSettings(self,id,tillId,maxCredit,discount,vat,currency,tillTag):
        if(id!=None,maxCredit!=None,discount!=None,vat!=None,currency!=None,tillTag!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            settings=SalesSettingsModel(id=id,tillId=tillId,maxCustomerCredit=maxCredit,maxDiscountPercent=discount,valueAddedTaxPercent=vat,currencyTag=currency,tillTagId=tillTag)
            session.add(settings)
            session.commit()
            return True,'Settings added Successfully'
        return False,'Passed a None or null parameter to addSalesSettings(self,id,maxCredit,discount,vat,currency,tillTag)'

    @staticmethod
    def getSalesSettings():
        Session=sessionmaker(bind=engine)
        session=Session()
        settings=None
        settings=session.query(SalesSettingsModel).filter_by(id=1).one_or_none()
        if(settings!=None):
            return settings
        return None 

    def deleteSalesSettings(self):
        state,settings=self.getSalesSettings()
        if(state==True):
            Session=sessionmaker(bind=engine)
            session=Session()
            session.delete(settings)
            session.commit()
            return True
        return False

    @staticmethod
    def fetchSettings():
        Session=sessionmaker(bind=engine)
        session=Session()
        s=session.query(SalesSettingsModel).filter_by(id=1).one_or_none()
        return s

class StockView:

    def addProductToStock(self,branchId,productId,barCode,quantity,authorId,time):
        message=''
        if(branchId!=None and productId!=None and barCode!=None and  quantity!=None and authorId!=None and time!=None):
            pByBarCode=self.getProductByBarCode(barCode)
            pByProductId=self.getProductById(productId)
            if(pByBarCode==None and pByProductId==None):
                Session=sessionmaker(bind=engine)
                session=Session()
                product=ProductsModel(
                    branchId=branchId,
                    productId=productId,
                    barCode=barCode,
                    quantity=quantity,
                    authorId=authorId,
                    time=time
                )
                session.add(product)
                session.commit()
                session.close()
            else:
                message='Product already exists hence could not be added'
        else:
            message='None type passed to StockView.addProductToStock()'
            Logging.consoleLog('error',message)
        return False,message
    
    def getProductByBarCode(self,barCode):
        if(barCode!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            product=session.query(StockModel).filter_by(barCode=barCode).one_or_none()
            session.close()
            return product
        return False
    
    def getProductById(self,productId):
        if(productId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            product=session.query(StockModel).filter_by(productId=productId).one_or_none()
            session.close()
            return product
        return False
    
    def addItems(self,userId,productId,barCode,addQuantity):
        message=''
        state=False
        if(userId!=None and productId!=None and barCode!=None and addQuantity>=1):
            Session=sessionmaker(bind=engine)
            session=Session()
            product=session.query(StockModel).filter_by(productId=productId,barCode=barCode).one_or_none()
            if(product!=None):
                currQuantity=product.quantity
                product.quantity=currQuantity+addQuantity
                session.add(product)
                session.commit()
                session.close()
                state=True
                message=f'Restocked item Pid={productId} barCode={barCode} with additional={addQuantity}'
            else:
                message=f'Product with barCode {barCode} and productId {productId} could not be found in StockModel'
        else:
            message='None type passed to StockView.addItems()'
        return state,message

    def removeItems(self,userId,productId,barCode,removeQuantity):
        message=''
        state=False
        if(userId!=None and productId!=None and barCode!=None and removeQuantity>=1):
            Session=sessionmaker(bind=engine)
            session=Session()
            product=session.query(StockModel).filter_by(productId=productId,barCode=barCode).one_or_none()
            if(product!=None):
                currQuantity=product.quantity
                product.quantity=currQuantity-removeQuantity
                session.add(product)
                session.commit()
                session.close()
                state=True
                message=f'RemovedItems from Pid={productId} barCode={barCode} with quantityRemoved={removeQuantity}'
            else:
                message=f'Product with barCode {barCode} and productId {productId} could not be found in StockModel'
        else:
            message='None type passed to StockView.removeItems()'
        return state,message

    def getProductFromStockModel(self,productId,barCode):
        state=False
        message=''
        if(productId!=None and barCode!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            product=session.query(StockModel).filter_by(productId=productId,barCode=barCode).one_or_none()
            session.close()
            return product,'retrieved successfully'
        else:
            message='None Type passed to StockView.getProductsStockCount()'
        return state,message

class StockHistoryView:
    @staticmethod
    def getDelta(stockAction,quantity):
        actions=StockHistoryModel.stockActionList
        try:
            delta=actions[stockAction]*quantity
            return delta
        except KeyError:
            return False
        
    @staticmethod
    def addStockHistory(stockReceipt,stockAction,branchId,productId,barCode,quantity,authorId):
        state=False
        message=''
        if(branchId!=None and productId!=None and barCode!=None and quantity!=None and authorId!=None):
            stockDelta=StockHistoryView.getDelta(stockAction,quantity)
            if(stockDelta!=False):
                Session=sessionmaker(bind=engine)
                session=Session()
                time=FormatTime.now()
                product=StockHistoryModel(
                    stockReceipt=stockReceipt,
                    stockAction=StockHistoryModel.stockActionList[stockAction],
                    stockDelta=StockHistoryModel.getDelta(stockAction,quantity),
                    userId=authorId,
                    branchId=branchId,
                    productId=productId,
                    barCode=barCode,
                    quantity=quantity,
                    time=time,
                )
                session.add(product)
                session.commit()
                session.close()
                state=True
                message='Stock History added successfully'
            else:
                message=f'There is no stock action by the name {stockAction} valid stock actions are {StockHistoryModel.stockActionList}'
        else:
            message='None type passed to StockHistoryView.addStockHistory()'
        Logging.consoleLog('message',message)
        return state,message

    @staticmethod
    def getStockHistory(startDate=0,endDate=0):
        stockHistory=[]
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startDate>0 and endDate>0):
            stockHistory=session.query(StockHistoryModel).filter(StockHistoryModel.time>=startDate, StockHistoryModel.time<=endDate)
        else:
            stockHistory=session.query(StockHistoryModel).all()
        return stockHistory

class EmptiesView:
    
    @staticmethod
    def productsWithEmpties(productsList,returnDate):
        emptiesList=[]
        if(productsList!=None):
            pObj=ProductsView()
            for p in productsList:
                product=pObj.getProductByBarCode(p['barCode'])
                if(product!=None and product!=False and product.returnContainers==True):
                    empty={'productId':product.id,'barCode':product.barCode,'returnDate':returnDate,'quantity':p['quantity']}
                    emptiesList.append(empty)
        return emptiesList

    @staticmethod
    def addEmpties(transactionId,emptiesList):
        if(transactionId!=None and emptiesList!=None):
            time=FormatTime.now()
            Session=sessionmaker(bind=engine)
            session=Session()
            for p in emptiesList:
                empty=EmptiesModel(
                    transactionId=transactionId,
                    productId=p['productId'],
                    barCode=p['barCode'],
                    returned=False,
                    takenDate=time,
                    quantityReturned=0,
                    returnDate=p['returnDate']
                )
                session.add(empty)
                session.commit()
            session.close()
            return True
        else:
            return False
    
    @staticmethod
    def addReturned(transactionId,productId,barCode,quantityReturned):
        if(transactionId!=None and productId!=None and barCode!=None and quantityReturned>=1):
            Session=sessionmaker(bind=engine)
            session=Session()
            #there may be a querry collision since a customer can take the same product with empties in the same transaction
            empty=session.query(EmptiesModel).filter_by(transactionId=transactionId,productId=productId,barCode=barCode,returned=False).first()
            empty.quantityReturned=empty.quantityReturned+quantityReturned
            session.add(empty)
            session.commit()
            session.close()
            return True
        return False

    @staticmethod
    def fetchEmptiesFromTransaction(transactionId):
        if(transactionId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            empties=session.query(EmptiesModel).filter_by(transactionId=transactionId).all()
            return empties
        return False

class BranchesView:

    def addBranch(self,branchName,location,branchPhone,tillNumber,managerName,managerPhone):
        if(branchName!=None and location!=None and branchPhone!=None and tillNumber!=None and managerName!=None and managerPhone!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            branch=BranchesModel(branchName=branchName,location=location,branchPhone=branchPhone,tillNumber=tillNumber,managerName=managerName,managerPhone=managerPhone)
            session.add(branch)
            session.commit()
            return True
        else:
            Logging.consoleLog('error','None type passed to BranchesView.addBranch()')
            return False

    def updateManager(self,branchId,managerName,managegerPhone):
        if(branchId!=None and managerName!=None and managegerPhone!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            branch=session.query(BranchesModel).filter_by(branchId=branchId).one_or_none()
            if(branch!=None):
                branch.managerName=managerName
                branch.managerPhone=managegerPhone
                session.commit()
                return True
            else:
                Logging.consoleLog('error',f'Branch with branchId {branchId} could not be found')
                return False
        else:
            Logging.consoleLog('error','None type passed to BranchesView.updateManager()')
            return False
    
    def updateTill(self,branchId,tillNum):
        if(branchId!=None and tillNum!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            branch=session.query(BranchesModel).filter_by(branchId=branchId).one_or_none()
            if(branch!=None):
                branch.tillNumber=tillNum
                session.commit()
                return True
            else:
                Logging.consoleLog('error',f'Branch with branchId {branchId} could not be found')
                return False
        else:
            Logging.consoleLog('error','None type passed to BranchesView.updateTill')
            return False

    def updateContact(self,branchId,contact):
        if(branchId!=None and contact!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            branch=session.query(BranchesModel).filter_by(branchId=branchId).one_or_none()
            if(branch!=None):
                branch.branchPhone=contact
                session.commit()
                return True
            else:
                Logging.consoleLog('error',f'Branch with branchId {branchId} could not be found')
                return False
        else:
            Logging.consoleLog('error','None type passed to BranchesView.updateContact()')
            return False

    def getAllBranches(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        branches=session.query(BranchesModel).all()
        return branches