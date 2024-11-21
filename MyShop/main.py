import eel

from users import User

pages=["index.html","till.html","admin.html"]

eel.init("web")  

# Exposing the random_python function to javascript
@eel.expose    
def login(username,password):
    u=User()
    auth,message,userLevel=u.login(username,password)
    if(auth):
        return {"auth":auth,"token":message,"userLevel":userLevel}    
    return {"auth":auth,"message":message,"userLevel":None}

@eel.expose
def logOut(userId):
    print("logging out")
    u=User()
    u.logout(int(userId))
    return {"state":True}





if __name__=="__main__":
    # Start the index.html file
    eel.start("login.html")