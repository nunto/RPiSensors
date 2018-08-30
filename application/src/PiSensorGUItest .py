#simple GUI

from tkinter import *


 #creating the window
root = Tk()
# Create a Tkinter variable
tkvar1 = StringVar(root)
tkvar2 = StringVar(root)
tkvar3 = StringVar(root)

#modify the root window

root.title("SensorPi")
root.geometry("1900x1300")


mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 10)
 

 
# List with options
choices = [ '0.5','1','1.5','2.0','2.5']

 
popupMenu = OptionMenu(mainframe, tkvar1, *choices)
Label(mainframe, text="Choose the frequency of checking the DHT sensor (every how many minutes)   ").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column = 1)
popupMenu["menu"].config(bg="WHITE")
tkvar1.set('1.0') # set the default option

popupMenu = OptionMenu(mainframe, tkvar2, *choices)
Label(mainframe, text="Choose the frequency of checking the current sensor (every how many minutes)   ").grid(row = 1, column = 2)
popupMenu.grid(row = 2, column = 2)
popupMenu["menu"].config(bg="WHITE")
tkvar2.set('1.0') # set the default option

popupMenu = OptionMenu(mainframe, tkvar3, *choices)
Label(mainframe, text="Choose the frequency of checking the RPM sensor (every how many minutes)   ").grid(row = 1, column = 3)
popupMenu.grid(row = 2, column = 3)
popupMenu["menu"].config(bg="WHITE")
tkvar3.set('1.0') # set the default option


SubmitButton = Button(mainframe, text = "Submit", command= lambda: buttonClick())
SubmitButton.grid(row = 3, column = 2)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

def buttonClick():
    print('hello')

# link function to change dropdown
tkvar1.trace('w', change_dropdown)
tkvar2.trace('w', change_dropdown)
tkvar3.trace('w', change_dropdown)


root.mainloop()




