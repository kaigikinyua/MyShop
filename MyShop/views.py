from sqlalchemy.orm import sessionmaker

from models import engine,UserModel,AuthModel,ProductsModel,ShiftModel,TransactionModel,PaymentModel,CustomerModel,SoldItemsModel
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
            session.add(auth)
            session.commit()
            
            shiftId=ShiftView.getOpenShiftId()
            if(shiftId==False):
                shiftId=ShiftView.openShift(u[0].id)
            if(shiftId!=False):
                ShiftView.addLogin(shiftId)

            return True,token,u[0].userLevel,shiftId
        return False,'Wrong username or password',0,0

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
        return activeSessions
    
    #check whether the user is authenticated
    def is_authenticated(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        auth=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(auth)>0):
            return True
        return False

    #gets the user from the UserModel
    def getUser(self,username):
        Session=sessionmaker(bind=engine)
        session=Session()
        users=session.query(UserModel).filter_by(name=username).one_or_none()
        if(users!=None):
            return users
        else:
            return None
    
    #creates a new user while checking for name collisions
    def addUser(self,username,userpassword,userLevel):
        if(len(username)>1 and len(userpassword)>5 and userLevel!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            collision_name=session.query(UserModel).filter_by(name=username).all()
            if(len(collision_name)>0):
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
                Logging.logToFile("warn",f"Updated user id={uid} name={user.name} level to {userLevel}")
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
                return True,'Deleted user with id of {uId}'
            else:
                return False,'There is no user by id {uId}'
        return False,'User id to be deleted cannot be empty'


    def permitAction(self,userToken):
        pass

class ShiftView:
    @staticmethod
    def openShift(openningId=0):
        Logging.consoleLog('succ',"Openning Shift")
        openShifts=ShiftView.checkOpenShifts()
        if(openShifts!=False):
            if(openShifts==None):
                sId=ShiftView.createShiftId()
                Session=sessionmaker(bind=engine)
                session=Session()
                sDate=FormatTime.getDateToday()
                shift=ShiftModel(shiftId=sId,shiftDate=sDate,startingAmount=0,closingAmount=0,openningId=openningId,closingId=0,logins=1,isClosed=False)
                session.add(shift)
                session.commit()
                return sId
            else:
                Logging.consoleLog('warn',f'Shift {openShifts} is not yet closed')
                return openShifts
        else:
            Logging.consoleLog('err','More than one shift is open')
            return False        

    @staticmethod
    def shiftIsOpen(shiftId):
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).filter_by(shiftId=shiftId,isClosed=False)
        if(len(openShifts)==1):
            return True
        elif(len(openShifts)==0):
            Logging.consoleLog('warn',f'There is no open shift by shiftId {shiftId}')
        elif(len(openShifts)>1):
            Logging.consoleLog('err',f'There is more than one shift with id {shiftId}')
        return False
    
    @staticmethod
    def getOpenShiftId():
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).filter_by(isClosed=False).all()
        if(len(openShifts)==1):
            return openShifts[0].shiftId
        elif(len(openShifts)==0):
            Logging.consoleLog('warn',f'There is no open shift')
        elif(len(openShifts)>1):
            Logging.consoleLog('err',f'There is more than one shift opened')
        return False
    
    @staticmethod
    def checkOpenShifts():
        Session=sessionmaker(bind=engine)
        session=Session()
        openShifts=session.query(ShiftModel).filter_by(isClosed=False).all()
        if(len(openShifts)==1):
            return openShifts[0].shiftId
        elif(len(openShifts)==0):
            return None
        elif(len(openShifts)>1):
            return False #Error more than one shift is open

    @staticmethod
    def closeShift(closingAmount=0,closingId=0):
        closId=closingId
        closAmount=closingAmount
    
    @staticmethod
    def createShiftId():
        timeStamp=FormatTime.now()
        tillId=Settings.tillId()
        return f'{tillId}{timeStamp}'

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
    def declareStartingAmount(startingAmount,shiftId):
        Session=sessionmaker(bind=engine)
        session=Session()
        shift=session.query(ShiftModel).filter_by(shiftId=shiftId,startingAmount=0).all()
        if(len(shift)==1):
            shift[0].startingAmount=startingAmount
            session.commit()
            return True
        elif(len(shift)>1):
            Logging.consoleLog(f'There is more than one shift with shift id {shiftId} whose starting amount=0')
        elif(len(shiftId)==0):
            Logging.consoleLog(f'There is no shift with the shift id {shiftId} whose starting amount is 0')
        return False

    @staticmethod
    def declareClosingAmount(closingAmount,shiftId):
        Session=sessionmaker(bind=engine)
        session=Session()
        shift=session.query(ShiftModel).filter_by(shiftId=shiftId,closingAmount=0).all()
        if(len(shift)==1):
            shift[0].closingAmount=closingAmount
            session.commit()
            return True
        elif(len(shift)>1):
            Logging.consoleLog(f'There is more than one shift with shift id {shiftId} whose closing amount=0')
        elif(len(shiftId)==0):
            Logging.consoleLog(f'There is no shift with the shift id {shiftId} whose closing amount is 0')
        return False


class ProductsView:
    def addProduct(self,pId,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        if(len(pName)>0 and len(barCode)>0 and bPrice!=None and sPrice!=None and returnContainers!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            p=ProductsModel(productId=pId,name=pName,barCode=barCode,buyingPrice=bPrice,sellingPrice=sPrice,returnContainers=returnContainers,productTags=tags,desc=desc)
            session.add(p)
            session.commit()
            return True
        else:
            return False
    
    def getAllProducts(self):
        Session=sessionmaker(bind=engine)
        session=Session()
        result=session.query(ProductsModel).all()
        return result
    
    def getProduct(self,pId):
        if(len(pId)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            result=session.query(ProductsModel).filter_by(productId=pId).all()
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
        if(len(pId)>0):
            Session=sessionmaker()
            session=Session()
            result=session.query(ProductsModel).delete(productId=pId)
            session.commit()
            return True,''
        else:
            return False,'Product id is empty Pid={pId}'

class TransactionView:
    def createTransaction(self,custId,sellerId,tillId,saleAmount,paidAmount):
        if(len(custId)>0 and len(sellerId)>0 and len(tillId)>0):
            if(int(saleAmount) and int(paidAmount)):
                t=TransactionModel()
                t.customerId=custId
                t.sellerId=sellerId
                t.tillId=tillId
                t.saleAmount=int(saleAmount)
                t.paidAmount=int(paidAmount)
                t.time=FormatTime.now()

                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(t)
                session.commit()
                return True
        else:
            return False
        
    def fetchTransactionById(self,tId):
        if(tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            transactions=session.query(TransactionModel).filter_by(id=int(tId)).first()
            return transactions
        return None
    
    def filterTransactionByPeriod(self,startDate,endDate):
        pass

    def filterTransactionByCustomer(self,custId):
        if(len(custId)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            return session.query(TransactionModel).filter_by(customerId=custId).all()
        else:
            return False
        
    def fetchAllTransactions(self,startTime,endTime):
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startTime!=None and endTime!=None):
            return session.query(TransactionModel).filter(TransactionModel.time>=startTime,TransactionModel.time<=endTime)
        else:
            return session.query(TransactionModel).all()

    def updatePaidAmount(self,tId,addAmount):
        try:
            addAmount=int(addAmount)
        except:
            return False
        if(tId!=None and addAmount!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            t=session.query(TransactionModel).filter_by(id=tId).first()
            t.paidAmount=t.paidAmount+int(addAmount)
            session.commit()
            return True
        return False

class PaymentView:
    def addPayment(self,paymentMethod,paymentAmount,transactionId,transactionNumber):
        t=TransactionView()
        tr=t.fetchTransactionById(transactionId)
        if(tr==None):
            #no transaction whose id=transactionId hence no payment can be made
            return False,f'There is no transaction whose id={transactionId}'
        if(len(paymentMethod)>0 and paymentAmount>0 and len(transactionId)>0):
            bal=self.balanceOnPayment(transactionId,paymentAmount)
            if(bal>=0):
                payment=PaymentModel()
                payment.transactionId=transactionId
                payment.paymentMethod=paymentMethod
                if(paymentMethod=='mpesa'):
                    payment.mpesaTransaction=transactionNumber
                elif(paymentMethod=='bank'):
                    payment.bankAcc=transactionNumber
                payment.amountPayed=paymentAmount
                payment.time=FormatTime.now()
                Session=sessionmaker(bind=engine)
                session=Session()
                session.add(payment)
                rslt=t.updatePaidAmount(transactionId,paymentAmount)
                if(rslt):
                    session.commit()
                    return True,'Completed Successfully'
                else:
                    session.rollback()
                    return False,'An error occured hence rollback database'
            elif(bal<0):
                return False,f'The customer will have paid exess of {bal*-1}'
        else:
            #one or some of the parameters are none
            return False,'Please fill in the paymentMethod,paymentAmount,transactionId'
    
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
            
    def fetchTransactionPayments(self,tId):
        if(tId!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            return session.query(PaymentModel).filter_by(transactionId=tId).all()
        else:
            #return error message tId is empty
            return None

    def fetchAllPayments(self,startTime,endTime):
        Session=sessionmaker(bind=engine)
        session=Session()
        if(startTime!=None and endTime!=None):
            return session.query(PaymentModel).filter(PaymentModel.time>=startTime,PaymentModel.time<=endTime).all()
        else:
            return session.query(PaymentModel).all()

            
class SoldItemsView:
    def addSoldItem(self,tId,productId,quantity,actualSellingPrice,itemsCollected):
        Session=sessionmaker(bind=engine)
        session=Session()
        bp=session.query(ProductsModel).filter_by(productId=productId).one_or_none()
        if(bp!=None):
            buyingPrice=bp.buyingPrice
            productSellingPrice=bp.sellingPrice
            discountPercent=((productSellingPrice-actualSellingPrice)/productSellingPrice)*100
            if(actualSellingPrice>buyingPrice):
                t=FormatTime.getDateTime()
                soldItem=SoldItemsModel(transactionId=tId,productId=productId,soldPrice=actualSellingPrice,expectedSellingPrice=productSellingPrice,discountPercent=discountPercent,buyingPrice=buyingPrice,quantity=quantity,itemsCollected=itemsCollected,time=t)
                session.add(soldItem)
                session.commit()
            else:
                return False,'You are selling at a loss'



    def fetchSoldItems(self,timeBegin,timeEnd):
        #timeBegin=year month day hour=00 minute=00 second=00
        pass

    def fetchReservedItems():
        Session=sessionmaker(bind=engine)
        session=Session()
        reservedItems=session.query(SoldItemsModel).filter_by(itemsCollected=False)
        return reservedItems

    def updateItemCollected():
        #update the soldItemsModel.itemsCollected
        #proceed to add collectedItem details
        #commit
        pass

class BranchesView:
    def addBranch(self,branchName,location,branchPhone,tillNumber,manager):
        pass
    def updateManager(self,branchId,manager):
        pass
    def updateTill(self,branchId,tillNum):
        pass
    def updateContact(self,branchId,contact):
        pass

class StockView:
    def addStockState(self,branchId,pId,stockType,quantity,authorId):
        stockTypes=['Receiving','Dispatch','Openning','Closing']
        pass

    def calcItemInStock(pId):
        pass

class CustomerView:
    def addCustomer(self,custName,phoneNumber):
        if(len(custName)>0 and len(phoneNumber)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            c=CustomerModel()
            c.name=custName
            c.phoneNumber=phoneNumber
            session.commit()
            return True
        else:
            return False
    def getCustomer(self,custId,custName,phoneNumber):
        if(custId!=None or custName!=None or phoneNumber!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            if(custId!=None):
                return session.query(CustomerModel).filter_by(id=custId).all()
            elif(custName!=None):
                return session.query(CustomerModel).filter_by(name=custName).all()
            elif(phoneNumber!=None):
                return session.query(CustomerModel).filter_by(phoneNumber=phoneNumber).all()
        else:
            return False
        
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
        result=session.query(CustomerModel).delete(id=custId)
        return True
    
    def getCustomerTransactions(self,custId):
        if(custId!=None):
            t=TransactionView()
            return t.filterTransactionByCustomer(custId)
        else:
            return False
