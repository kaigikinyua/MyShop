from sqlalchemy.orm import sessionmaker
from models import engine,UserModel,AuthModel
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
            token=str(time)+':'+str(u[0].name)
            auth=AuthModel(uid=u[0].id,time=time,token=token,active=True)
            session.add(auth)
            session.commit()
            return True
        return False



    def logout(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        activeSessions=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(activeSessions)>0):
            for sess in activeSessions:
                sess.active=False
                session.commit()

    def is_authenticated(self,uid):
        Session=sessionmaker(bind=engine)
        session=Session()
        auth=session.query(AuthModel).filter_by(uid=uid,active=True).all()
        if(len(auth)>0):
            return True
        return False
    
    def permitAction():
        pass
    def updatePassword():
        pass

class TransactionView:
    def createTransaction():
        pass
    def fetchTransactionById(self,tId):
        pass
    def fetchAllTransactions(self):
        pass
    def updatePaidAmount(self,tId,addAmount):
        pass
    def filterTransaction(self):
        pass

class PaymentView:
    def addPayment():
        pass
    def fetchPayments(self,tId):
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
