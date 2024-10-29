import eel

pages=["index.html","till.html","admin.html"]

eel.init("web")  

# Exposing the random_python function to javascript
@eel.expose    
def login():
    print("logged in")

@eel.expose
def logout():
    print("logged out")





if __name__=="__main__":
    # Start the index.html file
    eel.start("admin.html")