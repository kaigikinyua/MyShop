from sqlalchemy.orm import sessionmaker

from models import engine,UserModel,AuthModel,ShiftModel,TransactionModel,PaymentModel
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
    def openShift(startingAmount=0,openningId=0):
        shiftDate=FormatTime.nowStandardTime()
        strtAmount=startingAmount
        opnId=openningId

    @staticmethod
    def closeShift(closingAmount=0,closingId=0):
        closId=closingId
        closAmount=closingAmount

    @staticmethod
    def addLogin(loginId):
        pass

    @staticmethod
    def declareStartingAmount():
        pass
    @staticmethod
    def declareClosingAmount():
        pass

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
        pass
    def filterTransactionByPeriod(self,startDate,endDate):
        pass
    def filterTransactionByCustomer(self,custId):
        if(len(custId)>0):
            Session=sessionmaker(bind=engine)
            session=Session()
            return session.query(TransactionModel).filter_by(customerId=custId).all()
        else:
            return False
    def fetchAllTransactions(self):
        pass
    def updatePaidAmount(self,tId,addAmount):
        pass

class PaymentView:
    def addPayment(self,paymentMethod,paymentAmount,transactionId):
        if(len(paymentMethod)>0 and paymentAmount>0 and len(transactionId)>0):
            payment=PaymentModel()
            payment.transactionId=transactionId
            payment.paymentMethod=paymentMethod
            payment.amountPayed=paymentAmount
            payment.time=FormatTime.now()
            Session=sessionmaker(bind=engine)
            session=Session()
            session.add(payment)
            session.commit()
            return True
        else:
            return False

    def fetchTransactionPayments(self,tId):
        Session=sessionmaker(bind=engine)
        session=Session()
        return session.query(PaymentModel).filter_by(transactionId=tId).all()


    def fetchAllPayments(self,startTime,endTime):
        pass

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
