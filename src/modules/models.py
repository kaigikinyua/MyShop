from sqlalchemy import create_engine,ForeignKey,Float, Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from .settings import Settings

dbUrl=Settings.getDataBaseUrl()
engine=create_engine(dbUrl)
Base=declarative_base()

##users
class UserModel(Base):
    __tablename__='Users'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    password=Column(String)
    userLevel=Column(String)
    usrLevelChoices=['admin','cashier']
    #userPermissions=Column(String)
    #passwordExpireRyDate=Column(Float) 

class AuthModel(Base):
    __tablename__='Authenticated'
    id=Column(Integer,primary_key=True)
    uid=Column(Integer)
    time=Column(Float)
    token=Column(String)
    active=Column(Boolean)

class ShiftModel(Base):
    __tablename__="Shifts"
    id=Column(Integer,primary_key=True)
    shiftId=Column(String)
    shiftDate=Column(String)
    startingAmount=Column(Integer)
    closingAmount=Column(Integer)
    openningId=Column(Integer)
    closingId=Column(Integer)
    logins=Column(Integer)
    isClosed=Column(Boolean)
    startTime=Column(Float)
    endTime=Column(Float,default=None)

class EndOfDaySalesModel(Base):
    __tablename__='EndOfDaySales'
    id=Column(Integer,primary_key=True)
    date=Column(Float)
    grossSales=Column(Float,default=0)
    netSales=Column(Float,default=0)
    taxes=Column(Float,default=0)
    dayCredit=Column(Float,default=0)
    totalCredit=Column(Float,default=0)

class SalesSettingsModel(Base):
    __tablename__="SalesSettings"
    id=Column(Integer,primary_key=True)
    tillId=Column(String)
    maxCustomerCredit=Column(Integer)
    maxDiscountPercent=Column(Float)
    valueAddedTaxPercent=Column(Float)
    currencyTag=Column(String)
    tillTagId=Column(String)

class CustomerModel(Base):
    __tablename__="Customers"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    phoneNumber=Column(String)
    totalCreditOwed=Column(Integer,default=0)
    #registrationDate=Column(Float)
##transactions
class TransactionModel(Base):
    __tablename__='Transaction'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    customerId=Column(String,default=0)#for all customers who are not registerd and don't want to be registerd their id =0
    sellerId=Column(String)
    tillId=Column(String)
    time=Column(Float)
    saleAmount=Column(Integer)
    paidAmount=Column(Integer)

class PaymentModel(Base):
    __tablename__='Payments'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    paymentMethod=Column(String)
    amountPayed=Column(String)
    time=Column(Float)
    bankAcc=Column(String)
    mpesaTransaction=Column(String)
    paidForCreditId=Column(String,default=None)

class CustomerCreditModel(Base):
    __tablename__='CustomerCredit'
    id=Column(Integer,primary_key=True)
    customerId=Column(String)
    transactionId=Column(String)
    creditAmount=Column(String)
    totalCreditPaid=Column(Integer,default=0)
    creditDeadline=Column(Float)
    fullyPaid=Column(Boolean,default=False)
    time=Column(Float)

class SoldItemsModel(Base):
    __tablename__='SoldItems'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    productId=Column(String)
    barCode=Column(String)
    quantity=Column(Integer)
    soldPrice=Column(Integer)
    expectedSellingPrice=Column(Integer)
    buyingPrice=Column(Integer)
    discountPercent=Column(Float)
    itemsCollected=Column(Boolean)
    time=Column(Float)

class CollectedItemModel(Base):
    __tablename__='CollectedItem'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    collectorName=Column(String)
    collectorPhone=Column(String)
    timeCollected=Column(Float)

##Products and stock
class ProductsModel(Base):
    __tablename__='Products'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    barCode=Column(String,primary_key=True)
    productTags=Column(String)
    desc=Column(String)
    buyingPrice=Column(Integer)
    sellingPrice=Column(Integer)
    returnContainers=Column(Boolean)

class BranchesModel(Base):
    __tablename__='Branches'
    branchId=Column(Integer,primary_key=True)
    branchName=Column(String)
    location=Column(String)
    branchPhone=Column(String)
    tillNumber=Column(String)
    managerName=Column(String)
    managerPhone=Column(String)

class StockModel(Base):
    __tablename__='Stock'
    stockId=Column(Integer,primary_key=True)
    productId=Column(String)
    barCode=Column(String)
    quantity=Column(Integer)
    authorId=Column(Integer)
    time=Column(Float)

class StockHistoryModel(Base):
    __tablename__='StockHistory'
    id=Column(Integer,primary_key=True)
    stockReceipt=Column(String)#transactionId,dispatchId,invoiceNumber
    stockAction=Column(String)
    stockActionList={'receiving':1,'disptach':-1,'sale':-1,'return':1,'openning':1,'closing':1}
    stockDelta=Column(Integer)#either -1[sale,dispatch] or +1[restock,return] 
    userId=Column(String)
    branchId=Column(String)
    userStateMent=Column(String)
    productId=Column(String)
    barCode=Column(String)
    quantity=Column(String)
    time=Column(Float)

class StockTakeModel(Base):
    __tablename__='StockTake'
    stockId=Column(Integer,primary_key=True)
    branchId=Column(Integer)
    productId=Column(Integer)
    takingDate=Column(Integer)
    expectedCount=Column(Integer)
    counted=Column(Integer)
    variance=Column(Integer)

class EmptiesModel(Base):
    __tablename__='Empties'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    productId=Column(String)
    barCode=Column(String)
    quantity=Column(Integer)
    quantityReturned=Column(Integer,default=0)
    returned=Column(Boolean,default=False)
    despatchedToFactory=Column(Integer,default=0)
    takenDate=Column(Float)
    returnedDate=Column(Float)

class BusinessCostsModel(Base):
    __tablename__='Costs'
    billName=Column(String,primary_key=True)
    amount=Column(Integer)
    monthlyRecurring=Column(Boolean)
    costTimeline=Column(String)
    desc=Column(String)
    paid=Column(Boolean)

if __name__=="__main__":
    Base.metadata.create_all(engine)