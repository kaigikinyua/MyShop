import sys
from views import UserView,ProductsView,SaleSettingsView
from settings import Settings

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

class ProductsSetUp:
    products=[
            {'name':'Tusker Malt 500ml','barCode':'134253456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Guiness Malt 500ml','barCode':'13678456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'County 1000ml','barCode':'15234456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Honey Master 300ml','barCode':'5346356','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Sugar Malt','barCode':'856785456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
        ]
    
    @staticmethod
    def createProducts():
        i=1
        for p in ProductsSetUp.products:
            x=ProductsView()
            x.addProduct(i,p['name'],p['barCode'],p['tags'],p['desc'],p['bPrice'],p['sPrice'],p['returnContainers'])
            i=i+1
    @staticmethod
    def removeProducts():
        pass

class SaleSettingsSetUp:
    
    @staticmethod
    def addSalesSettings():
        id=1
        maxCredit=5000
        discount=5
        vat=16
        currency='Kenyan Shillings;Ksh'
        tillId='MainWareHouse'
        tillTag='WareHouse'

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

class CSV_Data_Dump:
    pass


def addAllSetUps():
    UsersSetUp.createUsers()
    ProductsSetUp.createProducts()
    SaleSettingsSetUp.addSalesSettings()

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