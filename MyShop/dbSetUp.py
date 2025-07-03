import random
import sys
from views import StockView,UserView,CustomerView,ProductsView,SaleSettingsView,BranchesView,CustomerModel
from settings import Settings
from utils import FormatTime,CSV
class UsersSetUp:
    @staticmethod
    def createUsers():
        users=[
            {'name':'admin','password':'admin12345','level':0},
            {'name':'cashier','password':'admin12345','level':1}
        ]
        for u in users:
            x=UserView()
            x.addUser(u['name'],u['password'],u['level'])
    @staticmethod
    def removeUsers():
        pass

class BranchesSetUp:
    branches=[
            {'name':'MainWareHouse','loc':'Ngara','phone':'074GASDGSL','tillNumb':'62467FAS','mName':'TestUser','mPhone':'011FAKJSHFASS'},
            {'name':'KBX 101k','loc':'Nairobi','phone':'0745XDFAGAS','tillNumb':'123XYZ','mName':'James Kuria King','mPhone':'07454ADFALKSGA'},
            {'name':'Nyamakima 01','loc':'Nairobi Downtown','phone':'0745DFJALKNC','tillNumb':'6425FASGA','mName':'Kamotho Kamau','mPhone':'07ASLKDJFLA'},
            {'name':'Juja 02','loc':'Juja Town','phone':'0745GBAKSJB','tillNumb':'2145SDFA','mName':'Susan Wajomoko','mPhone':'07GASJLKVSD'},
            {'name':'Kericho 05','loc':'Kericho Town','phone':'074RQWUOFASL','tillNumb':'782FASDF','mName':'Abdul Kharim','mPhone':'07FASKLJDFCAS'},
        ]
    
    @staticmethod
    def addBranches(branches):
        branchObj=BranchesView()
        for b in branches:
            branchObj.addBranch(b['name'],b['loc'],b['phone'],b['tillNumb'],b['mName'],b['mPhone'])

class ProductsSetUp:

    @staticmethod
    def setUpProducts():
        allData=CSV.readCSVFile('./data/products.csv')
        headers,noHeaders=CSV.removeCSVHeaders(allData)
        # dictNames=['id','name','barCode','tags','desc';'bPirce','sPrice','returnContainers']
        products=[]
        for row in noHeaders:
            print(row)
            r=row.split(',')
            products.append({'id':r[0],'barCode':r[1],'name':r[2],'desc':r[2],'tags':r[3],'quantity':r[4],'sPrice':r[5],'bPrice':r[6],'returnContainers':bool(r[7])})
        return products
    
    @staticmethod
    def createProducts():
        products=ProductsSetUp.setUpProducts()
        i=1
        for p in products:
            x=ProductsView()
            x.addProduct(i,p['name'],p['barCode'],p['tags'],p['desc'],p['bPrice'],p['sPrice'],p['returnContainers'])
            i=i+1

    @staticmethod
    def removeProducts():
        pass

class StockSetUp:
    @staticmethod
    def addStock():
        products=ProductsSetUp.setUpProducts()
        i=1
        time=FormatTime.now()
        for p in products:
            x=StockView()
            x.addProductToStock(i,p['barCode'],p['quantity'],2,time)
            i=i+1

class SaleSettingsSetUp:
    
    @staticmethod
    def addSalesSettings():
        id=1
        maxCredit=5000
        discount=5
        vat=16
        currency='Kenyan Shillings;Ksh'
        tillId=BranchesSetUp.branches[0]['name']
        tillTag=BranchesSetUp.branches[0]['name']

        s=SaleSettingsView()
        settings=SaleSettingsView.getSalesSettings()
        if(settings!=None):
            s.deleteSalesSettings()    
        s.addSalesSettings(id,tillId,maxCredit,discount,vat,currency,tillTag)

class TransactionsSetUp:
    transactions=[
        {"custId":'',"sellerId":'',"tillId":'',"saleAmount":''}
    ]
    payments=[
        {"tId":None,"paymentType":'',"amount":0,"phoneNum":'',"mpesaTid":'',"bankName":'',"bankAccNumber":'',}
    ]
    def createTransactions():
        pass

    def deleteTransactions():
        pass

class CustomerSetUp:
    customers=[
        {'name':'James 007','phoneNum':'123456789'},
        {'name':'Kamau Eric','phoneNum':'05412314564'},
        {'name':'Wangiku','phoneNum':'89745631'},
        {'name':'Mary Yvone','phoneNum':'023151045'},
    ]
    @staticmethod
    def addCustomers():
        custViewObj=CustomerView()
        for c in CustomerSetUp.customers:
            custViewObj.addCustomer(c['name'],c['phoneNum'])


def addAllSetUps():
    UsersSetUp.createUsers()
    BranchesSetUp.addBranches(BranchesSetUp.branches)
    ProductsSetUp.createProducts()
    SaleSettingsSetUp.addSalesSettings()
    StockSetUp.addStock()
    CustomerSetUp.addCustomers()

def backupdb():
    pass

def addSpecificSetUp(setUp):
    implementedArgs=['users','products','salessettings']
    if(setUp=='users'):
        UsersSetUp.createUsers()
    elif(setUp=='products'):
        ProductsSetUp.createProducts()
    elif(setUp=='salessettings'):
        SaleSettingsSetUp.addSalesSettings()
    else:
        print(f"Argument {setUp} not yet defined in addSpecificSetUp")
        print(f'Implemented arguments are {implementedArgs}')


if __name__=="__main__":
    systemArguments=sys.argv[1:len(sys.argv)]
    if Settings.mode=="DEBUG":
        if(systemArguments[0]=='all'):
            addAllSetUps()
        elif(systemArguments[0]=='backup'):
            backupdb()
        else:
            addSpecificSetUp(systemArguments[0])