from views import UserView
from settings import Settings
def createUsers():
    users=[
        {'name':'admin','password':'admin12345','level':'admin'},
        {'name':'cashier','password':'admin12345','level':'cashier'}
    ]
    for u in users:
        x=UserView()
        x.addUser(u['name'],u['password'],u['level'])


if __name__=="__main__":
    if Settings.mode=="DEBUG":
        createUsers()