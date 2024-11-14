from sqlalchemy import create_engine,ForeignKey, Column, Integer, String,Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


##users
class UserModel:
    __tablename__='Users'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    password=Column(String)

    def login(username,password):
        pass

    def logout(userToken):
        pass

class Authenticated:
    __tablename__='Authenticated'
    id=Column(Integer)
    time=Column(String)
    userId=Column(Integer)
    token=Column(String)

    def isAuthenticated(token):
        pass

##transactions
class TransactionModel:
    __tablename__='Transaction'
    transactionId=Column(String,primary_key=True)
    customerId=Column(String)
    sellerId=Column(String)
    tillId=Column(String)
    time=Column(String)
    saleAmount=Column(Integer)
    paidAmount=Column(Integer)
    
class SoldItemsModel:
    __tablename__='SoldItems'
    transactionId=Column(String)
    productId=Column(String)
    quantity=Column(Integer)
    sellingPrice=Column(Integer)
    itemsCollected=Column(Boolean)

class PaymentModel:
    __tablename__='Payments'
    transactionId=Column(String)
    paymentMethod=Column(String)
    amountPayed=Column(String)
    time=Column(String)

##Products and stock
class Products:
    __tablename__='Products'
    productId=Column(String,primary_key=True)
    desc=Column(String)
    buyingPrice=Column(Integer)
    sellingPrice=Column(Integer)
    returnContainers=Column(Boolean)

class Stock:
    __tablename__='Stock'
    productId=Column(String)
    location=Column(String)
    quantity=Column(String)
    lastUpdated=Column(String)

class Empties:
    __tablename__='Empties'
    transactionId=Column(String)
    productId=Column(String)
    goodCondition=Column(Integer)
    damaged=Column(Integer)
    lastUpdated=Column(String)

class BusinessCosts:
    __tablename__='Costs'
    billName=Column(String,primary_key=True)
    amount=Column(Integer)
    monthlyRecurring=Column(Boolean)
    costTimeline=Column(String)
    desc=Column(String)
    paid=Column(Boolean)
