"""tkiner tutorial series -> https://www.youtube.com/watch?v=RTM9tiV_HoY"""


from tkinter import *

# Main Window
root = Tk()


def printName(event):
    print("Hello my name is Danny")

# function cannot have "event" as a parameter
button_1 = Button(root, text="Print Name", command=printName)
button_1.pack()

# function must have "event" as parameter
button_2 = Button(root, text="Print Name")
button_2.bind("<Button-1>", printName)
button_2.pack()

"""

label_1 = Label(root, text="Name")
label_2 = Label(root, text="Password")
#input that displays in root
entry_1 = Entry(root)
entry_2 = Entry(root)

#default col is always equal to 0
#Specify an x and y
#Right Align is E (East, north, ect)
label_1.grid(row=0, column=0, sticky=E)
label_2.grid(row=1, column=0, sticky=E)

entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

#Checkbox that takes up 2 columns
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan=2)
"""
"""
# positioning
one = Label(root, text="One", bg="red", fg="white")
one.pack()
two = Label(root, text="Two", bg="green", fg="black")
# Fill X = will stretch as far as X is stretched in the app
two.pack(fill=X)
three = Label(root, text="Three", bg="blue", fg="white")
# Fill Y = will stretch as far as Y is stretched in the app
three.pack(side=LEFT, fill=Y)
"""
"""
#Making two frames a top and bottom
#Make an invisible container, put in main aka root
topFrame = Frame(root)

# Packs the frame into the area? Since we define the bottom it assumes this is the top
topFrame.pack()

# Make a bottom frame
bottomFrame = Frame(root)

# packs in main window at bottom -> side=BOTTOM
bottomFrame.pack(side=BOTTOM)

#Maknig buttons
# Button, (which frame, what to show up, button text color)
button1 = Button(topFrame, text="Button 1", fg="red")

button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="purple")

# Must pack the buttons in
# By default they stack
#side = pos will change pos
button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)
"""
# Displays to screen
root.mainloop()
