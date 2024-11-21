import eel

from users import User

pages=["index.html","till.html","admin.html"]

eel.init("web")  

# Exposing the random_python function to javascript
@eel.expose    
def login(username,password):
    print("Login from python")
    u=User()
    auth,message,userLevel=u.login(username,password)
    if(auth):
        return {"auth":auth,"message":message,"userLevel":userLevel}    
    return {"auth":auth,"message":message,"userLevel":None}

@eel.expose
def logout():
    print("logged out")





if __name__=="__main__":
    # Start the index.html file
    eel.start("login.html")