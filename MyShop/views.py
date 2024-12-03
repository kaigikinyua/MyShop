from sqlalchemy.orm import sessionmaker

from models import engine,UserModel,AuthModel,ProductsModel,ShiftModel,TransactionModel,PaymentModel,CustomerModel
from utils import FormatTime
class UserView:
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
            return True,token,u[0].userLevel
        return False,'Wrong username or password',None

    def logout(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        activeSessions=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(activeSessions)>0):
            for sess in activeSessions:
                sess.active=False
                session.commit()
            return True
    def get_UserActiveSessions(self,username):
        Session=sessionmaker(bind=engine)
        session=Session()
        user=self.getUser(username)
        activeSessions=session.query(AuthModel).filter_by(uid=user.id,active=True).all()
        return activeSessions

    def is_authenticated(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        auth=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(auth)==0):
            return True
        return False
    
    def permitAction(self,userToken):
        pass

    def getUser(self,username):
        Session=sessionmaker(bind=engine)
        session=Session()
        users=session.query(UserModel).filter_by(name=username).all()
        return users[0]

    def addUser(self,username,userpassword,userLevel):
        Session=sessionmaker(bind=engine)
        session=Session()
        collision_name=session.query(UserModel).filter_by(name=username).all()
        if(len(collision_name)>0):
            return False,'User name collision'
        else:
            user=UserModel(name=username,password=userpassword,userLevel=userLevel)
            #add checks incase database failed connection
            session.add(user)
            session.commit()
            return True,'Added user'

    def deleteUser(self,uId):
        pass

    def updateUser(self,uid,username,userLevel):
        Session=sessionmaker()
        session=Session()
        user=session.query(UserModel).filter_by(id=uid).one_or_none()
        if(user!=None):
            user.name=username
            user.userLevel=UserModel.usrLevelChoices[userLevel]
            session.commit()
            return True,'Updated user credentials'
        
    def updatePassword(self,uid,newPassword):
        Session=sessionmaker(bind=engine)
        session=Session()
        user=session.query(UserModel).filter_by(id=uid).one_or_none()
        if(user!=None):
            user.password=newPassword
            session.commit()
            return True,'Updated user password'

class ShiftView:
    @staticmethod
    def openShift(sAmount=0,openningId=0):
        if(sAmount>0 and openningId>0):
            shiftDate=FormatTime.nowStandardTime()
            if(ShiftView.createShiftId(shiftDate)!=None):
                Session=sessionmaker(bind=engine)
                session=Session()
                shift=ShiftModel()
                shift.shiftDate=None
                shift.startingAmount=sAmount
                shift.openningId=openningId
                shift.shiftDate=shiftDate
                shift.closingAmount=None
                shift.closingId=None
                shift.logins=1
                session.add(shift)
                session.commit()
                sId=ShiftView.createShiftId(shiftDate)
                s=session.query(ShiftModel).filter_by(shiftId=None).one_or_none()
                if(s!=None):
                    s.shiftId=sId
                    session.commit()
                    return True
                else:
                    return False,'Shift Id was not created'
                #add method to create shiftId
            else:
                return False,'Cannot create new shift when there is an unclosed shift'

    @staticmethod
    def closeShift(closingAmount=0,closingId=0):
        closId=closingId
        closAmount=closingAmount
    
    @staticmethod
    def createShiftId(shiftDate):
        Session=sessionmaker(bind=engine)
        session=Session()
        r=session.query(ShiftModel).filter(shiftDate=shiftDate,closingAmount=None)
        if(len(r)==0):
            return None
        else:
            return r[0].id+r[0].shiftDate

        
    @staticmethod
    def addLogin(loginId,shiftId):
        pass

    @staticmethod
    def declareStartingAmount():
        pass
    @staticmethod
    def declareClosingAmount():
        pass


class ProductsView:
    def addProduct(self,pName,barCode,tags,desc,bPrice,sPrice,returnContainers):
        if(len(pName)>0 and len(barCode)>0 and bPrice!=None and sPrice!=None and returnContainers!=None):
            Session=sessionmaker(bind=engine)
            session=Session()
            p=ProductsModel()
            p.name=pName
            p.barCode=barCode
            p.buyingPrice=bPrice
            p.sellingPrice=sPrice
            p.returnContainers=returnContainers
            p.productTags=tags
            p.desc=desc
            session.add(p)
            session.commit()
        else:
            return False
        
    def getProduct(self,pId):
        if(len(pId)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            result=session.query(ProductsModel).filter(productId=pId)
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
    def addSoldItem(self,tId,productId,quantity,itemsCollected):
        pass
    def fetchSoldItems(self,timeBegin,timeEnd):
        #timeBegin=year month day hour=00 minute=00 second=00
        pass
    def fetchReservedItems():
        pass

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
    def addStock(self,branchId,pId,stockType,quantity,authorId):
        stockTypes=['Receiving','Dispatch','Openning','Closing']
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
