#simple GUI

from tkinter import *

class GraphicInterface:
    #add in the various intervals for all the different sensors that we will be using as arguments
    def __init__(self, DHTInterval=None, CurrentInterval=None, RPMInterval=None):
        self.DHTInterval = DHTInterval if DHTInterval is not None else 0
        self.CurrentInterval = CurrentInterval if CurrentInterval is not None else 0
        self.RPMInterval = RPMInterval if RPMInterval is not None else 0
        self.tkvar1 = None
        self.tkvar2 = None
        self.tkvar3 = None
        self.is_Ready = False
        self.mainframe = None
        self.root = None
        
        
    def createwindow(self):
        self.root = Tk()
        # Create a Tkinter variable
        tkvar = StringVar(self.root)
        self.tkvar1 = StringVar(self.root)
        self.tkvar2 = StringVar(self.root)
        self.tkvar3 = StringVar(self.root)

        #modify the self.root window

        self.root.title("SensorPi")
        self.root.geometry("1900x1300")


        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(pady = 100, padx = 10)
         
        
         
        # List with options
        choices = [ '0.5','1.0','1.5','2.0','2.5']

        #setting up the various pop-up menus to make the choices available 
        popupMenu1 = OptionMenu(self.mainframe, self.tkvar1, *choices, command=self.setDHT)
        Label(self.mainframe, text="Choose the frequency of checking the DHT sensor (every how many minutes)   ").grid(row = 1, column = 1)
        popupMenu1.grid(row = 2, column = 1)
        popupMenu1["menu"].config(bg="WHITE")
        self.tkvar1.set('1.0') # set the default option

        popupMenu2 = OptionMenu(self.mainframe, self.tkvar2, *choices, command = self.setCurrent)
        Label(self.mainframe, text="Choose the frequency of checking the current sensor (every how many minutes)   ").grid(row = 1, column = 2)
        popupMenu2.grid(row = 2, column = 2)
        popupMenu2["menu"].config(bg="WHITE")
        self.tkvar2.set('1.0') # set the default option

        popupMenu3 = OptionMenu(self.mainframe, self.tkvar3, *choices, command = self.setRPM)
        Label(self.mainframe, text="Choose the frequency of checking the RPM sensor (every how many minutes)   ").grid(row = 1, column = 3)
        popupMenu3.grid(row = 2, column = 3)
        popupMenu3["menu"].config(bg="WHITE")
        self.tkvar3.set('1.0') # set the default option


        SubmitButton = Button(self.mainframe, text = "Submit", command= lambda: self.buttonClick())
        SubmitButton.grid(row = 3, column = 2)

        #self.tkvar1.trace('w', self.change_dropdown)
        #self.tkvar2.trace('w', self.change_dropdown)
        #self.tkvar3.trace('w', self.change_dropdown)
        self.root.mainloop()

    # on change dropdown value
    
    def change_dropdown(self, *args):
        print( tkvar.get())
    
    def setDHT(self,value):
        self.DHTInterval = value
    
    def setCurrent(self, value):
        self.CurrentInterval = value
        
    def setRPM(self,value):
        self.RPMInterval = value
    
    def dismiss(self):
        self.mainframe.destroy()
        self.root.destroy()
    
    def buttonClick(self):
        self.is_Ready = True
        self.dismiss()

gui = GraphicInterface(1,1,1)
gui.createwindow()



