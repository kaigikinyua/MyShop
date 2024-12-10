from views import UserView,ProductsView
from settings import Settings
def createUsers():
    users=[
        {'name':'admin','password':'admin12345','level':'admin'},
        {'name':'cashier','password':'admin12345','level':'cashier'}
    ]
    for u in users:
        x=UserView()
        x.addUser(u['name'],u['password'],u['level'])

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

if __name__=="__main__":
    if Settings.mode=="DEBUG":
        createUsers()
        createProducts()