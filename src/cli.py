import sys
from cli_tools.dbSetUp import *

def mapToActions(command):
    command=command.lower()
    if(command=='migrate'):
        migrate()
    elif(command=='setupdb'):
        addAllSetUps()
    else:
        print(f"command {command} not found")

if __name__=="__main__":
    systemArguments=sys.argv[1:len(sys.argv)]
    if(len(systemArguments)>0):
        mapToActions(systemArguments[0])
    else:
        print("cli expects the following commands at the moment")
        print("migrate | setupdb ")
