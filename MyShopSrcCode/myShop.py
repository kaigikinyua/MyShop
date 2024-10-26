from tkinter import *
from tkinter import ttk
class Frame:
    def __init__(self,parent):
        self.parent=parent

    def clearFrame(self):
        pass

class Login(Frame):
    def __init__(self):
        pass

class Home(Frame):
    pass

class CloseShift(Frame):
    pass

class Inventory(Frame):
    pass

class Sale(Frame):
    pass

class Expense(Frame):
    pass

class Reports(Frame):
    pass




if __name__=="__main__":
    root=Tk()
    root.title("My Shop")
    
    #menubar
    menuBar=Menu(root)
    fileMenu=Menu(menuBar,tearoff=0)
    menuBar.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label='New',command=None)
    fileMenu.add_command(label="Open",command=None)
    
    editMenu=Menu(menuBar,tearoff=1)
    editMenu.add_cascade(label="Edit",menu=editMenu)
    editMenu.add_command(label="Edit",command=None)
    menuBar.add_cascade(label="Edit",menu=editMenu)
    root.config(menu=menuBar)
    
    #mainframe
    mainFrame=ttk.Frame(root,padding=10)
    root.mainloop()