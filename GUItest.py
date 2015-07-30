import tkinter as tk
from enigma import *

root1 = tk.Tk()  # root window
label = tk.Label(root1, text='this is a label')  # writes some text to label the entry
entry = tk.Entry(root1)  # makes a text box to take input
label.pack(side=tk.TOP)  # make the things appear in the root window
entry.pack()  # automatically appears below
def showentry(event):
    print(entry.get())

entry.bind('<Return>', showentry)
root1.mainloop()  # this makes the root window appear

root2 = tk.Tk()
label2 = tk.Label(root2, text='Choose a button')
buttonstr = tk.StringVar()  # make a variable of type StringVar
buttonA = tk.Radiobutton(root2, text='Button A', variable=buttonstr, value='ButtonA string')  # make some radiobuttons
buttonB = tk.Radiobutton(root2, text='Button B', variable=buttonstr, value='ButtonB string')
buttonC = tk.Radiobutton(root2, text='Button C', variable=buttonstr, value='ButtonC string')
def showstr(event=None):  # this is just a function
    print(buttonstr.get())  # it prints the value of buttonstr by using its get method

buttonA.config(command=showstr)  # these reference the above function as a callback
buttonB.config(command=showstr)  # this means the function runs when the button is selected
buttonC.config(command=showstr)
#set the widgets up for the grid manager
label2.grid(column=0, row=0)
buttonA.grid(column=0, row=1)
buttonB.grid(column=0, row=2)
buttonC.grid(column=0, row=3)
buttonA.select()
root2.mainloop()