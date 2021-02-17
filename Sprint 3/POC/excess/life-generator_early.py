""" Name: Danny Sulsberger Project: life-generator.py Course: CS 361"""

from tkinter import *
from tkinter import filedialog
import csv



# Read the dataset file
    

# Main Window
root = Tk()
root.title('Title')
root.geometry("600x600")
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

try:

    csv_file = csv.reader(open('CSV_DOC.csv', "r", encoding='utf-8'))

    for row in csv_file:
        for i in range(len(row)):
            if row[i] == "":
                continue
            else:
                print(row[i])
        break

    
    cat_arr = []
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
except:
    print('No File was added')

"""
#Opening the dir and pick a file type of CSV
root.filename = filedialog.askopenfilename(initialdir="/Users/18122/Documents/GitHub/CS361/Sprint 3/POC", title="Enter CSV", filetypes=(("CSV file", "*.csv"), ("allfiles", "*.*")))
my_label = Label(root, text=root.filename).pack()
"""

# This is used for the directory selection.. stuff  ('default root is jsut '/')

"""
def open_button():
    global filename
    global clicked
    try:
        filename = filedialog.askopenfilename(initialdir="/Users/18122/Documents/GitHub/CS361/Sprint 3/POC", title="Enter CSV", filetypes=(("CSV file", "*.csv"), ("allfiles", "*.*")))
        my_label = Label(root, text=filename).pack()

        csv_file = csv.reader(open(filename, "r", encoding='utf-8'))
    
        for row in csv_file:
            for i in range(len(row)):
                if row[i] == "":
                    continue
                else:
                    print(row[i])
            break

        
        cat_arr = []
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
        
    except:
        print('No File was added')


my_btn = Button(root, text="Open File", command=open_button).pack()
"""
# Number Input boxes 
e = Entry(root, width =25, borderwidth = 1)
e.pack()
# Get the input
e.insert(0, "3")

def myClick():
    global myLabel
    #changing text will change what is printed
    myLabel = Label(root, text="You've selected " + e.get() + " items.")
    myLabel.pack()

myButton = Button(root, text="Update Number of Results Shown", command=myClick)
myButton.pack()


#Drop down box
# Defining click def as a string bc our variables are strings
# Using a list to populate the dropdown

def show():
    global show_Label
    show_Label = Label(root, text=clicked.get()).pack()

clicked = StringVar()
clicked.set(cat_arr[0])


#Drop down box
drop = OptionMenu(root, clicked, *cat_arr)
drop.pack()

myButton = Button(root, text="Show Selection", command=show).pack()


#Generate button

def show_gen():
    global gen_label
    gen_label = Label(bottomFrame, text=clicked_gen.get()).pack()

clicked_gen = StringVar()
clicked_gen.set('Generate!!!!!!!!!!')

Gen_button = Button(root, text="Generate", command=show_gen).pack()

#Delete

def myDelete():
    show_Label.delete()
    my_Label.delete()

DeleteButton = Button(root, text="Delete Text", command=myDelete)
DeleteButton.pack(pady=10)

# Displays to screen
root.mainloop()
