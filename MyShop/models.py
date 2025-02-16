from sqlalchemy import create_engine,ForeignKey,Float, Column, Integer, String,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from settings import Settings

dbUrl=Settings.dataBaseUrl
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

class CustomerModel(Base):
    __tablename__="Customers"
    id=Column(Integer,primary_key=True)
    name=Column(String,primary_key=True)
    phoneNumber=Column(String,primary_key=True)

##transactions
class TransactionModel(Base):
    __tablename__='Transaction'
    id=Column(Integer,primary_key=True)
    transactionId=Column(String)
    customerId=Column(String)
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
    managerPhoneNumber=Column(String)

class StockModel(Base):
    __tablename__='Stock'
    stockId=Column(Integer,primary_key=True)
    branchId=Column(Integer)
    productId=Column(String)
    stockType=Column(String)
    quantity=Column(String)
    authorId=Column(Integer)
    time=Column(Float)

class StockDispatchReceivingModel(Base):
    __tablename__='DispatchAndReceiving'
    id=Column(Integer,primary_key=True)
    stockId=Column(Integer)
    dispatcher=Column(Integer)
    receiver=Column(Integer)
    received=Column(Boolean)
    rejected=Column(Boolean)

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
    goodCondition=Column(Integer)
    damaged=Column(Integer)
    timeLastUpdate=Column(Float)

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