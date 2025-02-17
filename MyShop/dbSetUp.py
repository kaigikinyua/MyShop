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

class ProductsSetUp:
    @staticmethod
    def createProducts():
        products=[
            {'name':'Tusker Malt 500ml','barCode':'134253456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Guiness Malt 500ml','barCode':'13678456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'County 1000ml','barCode':'15234456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Honey Master 300ml','barCode':'5346356','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
            {'name':'Sugar Malt','barCode':'856785456','tags':'tusker','desc':'500ml','bPrice':300,'sPrice':500,'returnContainers':False},
        ]
        i=1
        for p in products:
            x=ProductsView()
            x.addProduct(i,p['name'],p['barCode'],p['tags'],p['desc'],p['bPrice'],p['sPrice'],p['returnContainers'])
            i=i+1

class SaleSettingsSetUp:
    @staticmethod
    def addSalesSettings():
        id=1
        maxCredit=5000
        discount=5
        vat=16
        currency='Kenyan Shillings;Ksh'
        tillId='WareHouse'

        s=SaleSettingsView()
        state,settings=s.getSalesSettings()
        if(state==True):
            s.deleteSalesSettings()    
        s.addSalesSettings(id,maxCredit,discount,vat,currency,tillId)

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


if __name__=="__main__":
    if Settings.mode=="DEBUG":
        UsersSetUp.createUsers()
        ProductsSetUp.createProducts()
        SaleSettingsSetUp.addSalesSettings()