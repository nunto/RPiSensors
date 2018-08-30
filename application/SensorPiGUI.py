#simple GUI

from tkinter import *

#creating the window
root = Tk()

#modify the root window

root.title("SensorPi")
root.geometry("400x300")


mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 10)
 
# Create a Tkinter variable
tkvar = StringVar(root)
 
# List with options
choices = [ '0.5','1','1.5','2.0','2.5']

 
popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose the frequency of checking").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)
tkvar.set('1') # set the default option

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )
 
# link function to change dropdown
tkvar.trace('w', change_dropdown)



root.mainloop()