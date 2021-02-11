from tkinter import *
import csv
import sys

root = Tk()
root.title('Life Generator')
root.geometry("400x400")

#if len(sys.argv) > 1:
finput = open('input.csv', "r", encoding='utf-8-sig')
input_file = csv.reader(finput)
print('Input upload successful')

input_arr = []
counter = 0
for row in input_file:
    try:            
        input_arr.append(row)

    except:
        continue

print(input_arr, 'input arr')

try:
    fh = open('CSV_DOC.csv', "r", encoding='utf-8')
    csv_file = csv.reader(fh)
    print('Upload successful')
    print(csv_file)
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
    fh.seek(0)
except:
    print('No File was added')

# Delete button func
def myDelete():
    try:
        myLabel.destroy()
        myButton['state'] = NORMAL
        show_Label.destroy()
        show_button['state'] = NORMAL
    except:
        return

# Input function
def myClick():
    global myLabel
    global num
    num = e.get()
    print(num + 'num in here')
    myLabel = Label(root, text=num)
    #e.delete(0, 'end')
    myLabel.pack()
    myButton['state'] = DISABLED

#Drop down box
# Defining click def as a string bc our variables are strings
# Using a list to populate the dropdown

def show():
    global show_Label
    click = clicked.get()
    show_Label = Label(root, text=click)
    show_Label.pack(pady=10)
    show_button['state'] = DISABLED

clicked = StringVar()
clicked.set(cat_arr[1])
#show_Label = Label(root, text=cat_arr[1]).pack()

def new_search():
    fh.seek(0)
    Gen_button['state'] = NORMAL
    myLabel.destroy()
    myButton['state'] = NORMAL
    show_Label.destroy()
    show_button['state'] = NORMAL
#Generate button

# THIS MAY NOT BE USED NOW
def show_gen():
    global gen_label
    clicked_gen = clicked_generate.get()
    gen_label = Label(root, text=clicked_gen)
    gen_label.pack(pady=10)

def alg_helper():
    Gen_button['state'] = DISABLED
    category = clicked.get()
    print(num, category)

    alg_result = sort_alg(num, category)
    print(alg_result)
    return alg_result

def sort_alg(num, category_selected):
    #Takes category keyword
    print(num, 'this is num')
    number = int(num)
    new_arr = []
    for row in csv_file:
        try:
            if row[8]== "":
                continue
            else:
                item = row[8]
                split = item.split(">")
                if split[0] == category_selected:
                    new_arr.append(row)
                else:
                    continue
        except:
            continue
    print(len(new_arr))

    # Sorts by Unique ID

    sorted_id = merge_sort(new_arr)
    #for i in range(100):
        #print(sorted_id[i][0])

    # Sorts by # of reviews

    sorted_rev = merge_sort(sorted_id, 1)
    #for i in range(len(sorted_rev)):
        #print(sorted_rev[i][5])

    # Take top x * 10 results
    top_ten = []
    range_num = 10 * number
    for i in range(range_num):
        try:
            top_ten.append(sorted_rev[i])
        except:
            break
    #print(top_ten)

    #Sorts top x * 10 by uniq ID
    ten_uniq = merge_sort(top_ten)
    for i in range(range_num):
        try:
            print(ten_uniq[i][0])
        except:
            break

    #Sorts top10uniqID by avg review
    ten_avg = merge_sort(ten_uniq, 2)
    for i in range(range_num):
        try:
            print(ten_avg[i][7])
        except:
            break

    final_arr = []
    for i in range(number):
        try:
            final_arr.append(ten_avg[i])
            print(final_arr[i][0], final_arr[i][7])
        except:
            break
    #Does stuff from there


def merge(left, right):
    """Merge to deal with unique ID"""
    values = {"0": 0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "a":10, "b":11, "c":12, "d":13, "e": 14, "f": 15, "g":16, "h":17, "i":18,
"j":19, "k":20, "l":21, "m":22, "n":23, "o":24, "p":25, "q":26, "r":27, "s":28, "t":29, "u":30, "v":31, "w":32, "x":33, "y":34, "z":35}
    
    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        L = left[left_index][0]
        R = right[right_index][0]

        #lefty = left[left_index][0][0]
        #righty = right[right_index][0][0]

        if len(L) < len(R):
            shortest = L
        else:
            shortest = R

        for i in range(len(shortest)):
            left_first = left[left_index][0][i]
            right_first = right[right_index][0][i]
            test_1 = values[left_first]
            test_2 = values[right_first]

            if values[left_first] == values[right_first]:
                continue
            else:
                break

        if values[left_first] > values[right_first]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result


def merge_sort(array, flag=0):
    """Base merge all mergs will call"""
    if len(array) <= 1:  # base case
        return array

    if flag == 1:
        # divide array in half and merge sort recursively
        half = len(array) // 2
        left = merge_sort(array[:half], 1)
        right = merge_sort(array[half:], 1)

        return merge_reviews(left, right, 1)

    if flag == 2:
        # divide array in half and merge sort recursively
        half = len(array) // 2
        left = merge_sort(array[:half], 2)
        right = merge_sort(array[half:], 2)

        return merge_average(left, right, 2)

    else:
    # divide array in half and merge sort recursively
        half = len(array) // 2
        left = merge_sort(array[:half])
        right = merge_sort(array[half:])

        return merge(left, right)

def merge_average(left, right, sort_number):
    """Merge to deal with average"""

    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        lefty = left[left_index]
        righty = right[right_index]

        l_string = lefty[7]
        l_split = l_string.split(" ")
        left_first = l_split[0]
        r_string = righty[7]
        r_split = r_string.split(" ")
        right_first = r_split[0]

        if left_first > right_first:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result

def merge_reviews(left, right, sort_number):
    """Merge to deal with review"""

    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        lefty = left[left_index]
        righty = right[right_index]

        l_string = lefty[5]
        #Deals with the few numbers that have commas
        l_string = l_string.replace(',','')
        l_string = l_string.replace('','0')
        left_first = int(l_string)
        r_string = righty[5]
        #Deals with the few numbers that have commas
        r_string = r_string.replace(',','')
        r_string = r_string.replace('','0')
        right_first = int(r_string)

        if left_first > right_first:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result

# Number Input boxes 
e = Entry(root, width =25)
e.pack()
e.insert(0, "3")

myButton = Button(root, text="Confirm # of Results", command=myClick)
myButton.pack()

#Drop down box
drop = OptionMenu(root, clicked, *cat_arr[1:])
drop.pack()

show_button = Button(root, text="Show Selection", command=show)
show_button.pack()

DeleteButton = Button(root, text = "Clear parameters", command=myDelete)
DeleteButton.pack(pady=10)

# Generate stuff
clicked_generate = StringVar()
clicked_generate.set('Generate!!!!!!!!!!')

Gen_button = Button(root, text="Generate", command=alg_helper)
Gen_button.pack()

# Reset button
clicked_newSearch = StringVar()
clicked_newSearch.set('Generate!!!!!!!!!!')

newSearch_button = Button(root, text="New Search", command=new_search)
newSearch_button.pack()
root.mainloop()

