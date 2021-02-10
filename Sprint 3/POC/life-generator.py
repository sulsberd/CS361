""" Name: Danny Sulsberger Project: life-generator.py Course: CS 361"""

from tkinter import *
from tkinter import filedialog
import csv

# Main Window
root = Tk()
root.title('Title')
root.geometry("600x600")

"""
#Opening the dir and pick a file type of CSV
root.filename = filedialog.askopenfilename(initialdir="/Users/18122/Documents/GitHub/CS361/Sprint 3/POC", title="Enter CSV", filetypes=(("CSV file", "*.csv"), ("allfiles", "*.*")))
my_label = Label(root, text=root.filename).pack()
"""

# This is used for the directory selection.. stuff  ('default root is jsut '/')

def open_button():
    global my_csv
    global cat_arr = []
    try:
        root.filename = filedialog.askopenfilename(initialdir="/Users/18122/Documents/GitHub/CS361/Sprint 3/POC", title="Enter CSV", filetypes=(("CSV file", "*.csv"), ("allfiles", "*.*")))
        my_label = Label(root, text=root.filename).pack()

        csv_file = csv.reader(open(root.filename, "r", encoding='utf-8'))
    
        for row in csv_file:
            for i in range(len(row)):
                if row[i] == "":
                    continue
                else:
                    print(row[i])
            break

        
        
        for row in csv_file:
            try:
                if row[8]== "":
                    continue
                else:
                    item = row[8]
                    split = item.split(">")
                    if split[0] in cat_arr:
                        continue
                    else:
                        cat_arr.append(split[0])

            except:
                continue
        print(cat_arr)
    except:
        print('No File was added')

my_btn = Button(root, text="Open File", command=open_button).pack()


#Input boxes
e = Entry(root, width =50, borderwidth = 1)
e.pack()
# Get the input
e.insert(0, "3")

def myClick():
    #changing text will change what is printed
    myLabel = Label(root, text="You've selected " + e.get() + " items.")
    myLabel.pack()

myButton = Button(root, text="Press enter after number", command=myClick)
myButton.pack()



#Drop down box
# Defining click def as a string bc our variables are strings
# Using a list to populate the dropdown
#options = ["In a list", "Monday", "Tuesday", "Wednesday", "Ect"]

def show():
    myLabel = Label(root, text=clicked.get()).pack()

clicked = StringVar()
clicked.set(cat_arr[0])


#Drop down box
drop = OptionMenu(root, clicked, *options)
drop.pack()

myButton = Button(root, text="Show Selection", command=show).pack()


#Generate button

def show_gen():
    gen_label = Label(root, text=clicked_gen.get()).pack()

clicked_gen = StringVar()
clicked_gen.set('Generate!!!!!!!!!!')

Gen_button = Button(root, text="Generate", command=show_gen).pack()

# Displays to screen
root.mainloop()
