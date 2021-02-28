# Project: life-generator
# Name: Danny Sulsberger
# Date: 14FEB2021
# See assignment 3.4 requirements for functionality
# Project is POC for use case

from tkinter import *
from tkinter import ttk
import csv
import sys
from subprocess import Popen, PIPE
import os

def auto():
    """auto triggers from main if arg added to sys.argv"""

    # Opens DB
    fh = open('amazon_co-ecommerce_sample.csv', "r", encoding='utf-8-sig')
    global csv_file
    csv_file = csv.reader(fh)
    print('Database upload successful')

    # Opens Input file from sys.argv highlight
    finput = open('input.csv', "r", encoding='utf-8-sig')
    input_file= csv.reader(finput)
    print('Input CSV upload successful')

    #Move rows into arr
    input_arr = []
    for row in input_file:
        try:            
            input_arr.append(row)
        except:
            continue

    addContent()
    # Sorting per Requirements
    citem_type, ccategory_type, cnum_generate = auto_variables(input_arr)
    automatic_result = sort_alg(cnum_generate, ccategory_type, csv_file, 1)

    output_file = open('output.csv', 'w', newline='')

    output_headers = ['input_item_type', 'input_item_category', 'input_number_to_generate',
    'output_item_name', 'output_item_rating', 'output_item_num_reviews']

    output_writer = csv.writer(output_file)
    output_writer.writerow(output_headers)
    temp_row = []
    for rows in automatic_result:
        temp_row.append(citem_type)
        temp_row.append(ccategory_type)
        temp_row.append(cnum_generate)
        temp_row.append(rows[1]) # Item name
        temp_row.append(rows[7]) # Item Rating
        temp_row.append(rows[5]) # Number of Review
        output_writer.writerow(temp_row)
        temp_row=[]
    print('output.csv export successful')
    output_file.close()

    fh.seek(0)

def addContent():
    process = Popen(['python.exe', 'Content_Generator.py'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    content_Output = open('outputCG.csv', "r", encoding='utf-8-sig')
    contentOutputCSV= csv.reader(content_Output)
    rawContentText = []
    for lines in contentOutputCSV:
        rawContentText.append(lines)

    pureContentText = rawContentText[2][1]
    return pureContentText

def auto_variables(input_arr):
    """Takes input arr and returns the values associated with each header
        It's slightly more complicated to deal with the situation where the headers
        are not in the same order as they were defined in default"""
    # input_arr = rows of input.csv in an arr 

    result_dictionary = {}
    # Makes an arr of arrs with the correct key/value
    for i in range(len(input_arr[0])):
        key_n = input_arr[0][i]
        #print(key_n)
        value_n = input_arr[1][i]
        result_dictionary[key_n] = value_n
   
    #Uses the loop to check for a key and get that value out
    loop = ['input_item_type', 'input_item_category', 'input_number_to_generate']
    
    item_type = result_dictionary[loop[0]]
    category_type = result_dictionary[loop[1]]
    num_generate = result_dictionary[loop[2]]

    return item_type, category_type, num_generate

def my_par_click():
    """button to confirm the parameters"""
    global num
    num = e.get()
    my_parameter['state'] = DISABLED
    e['state'] = DISABLED

def new_search():
    """Function to reset search to default"""
    fh.seek(0)
    e['state'] = NORMAL
    Gen_button['state'] = NORMAL
    my_parameter['state'] = NORMAL

def normal():
    """This is used as the GUI helper"""
    my_parameter['state'] = DISABLED
    Gen_button['state'] = DISABLED
    #DeleteButton['state'] = DISABLED
    category = clicked.get()
    
    step_before = sort_alg(num, category, csv_file)
    output_headers = ('#', 'output_item_name', 'output_item_rating', 'output_item_num_reviews')
        
    contentGeneratorText = addContent()
    cut_row = []
    for rows in step_before:
        temp_row = []
        temp_row.append(rows[1]) # Item Name
        temp_row.append(rows[7]) # Item Rating
        temp_row.append(rows[5]) # Num of Reviews
        cut_row.append(temp_row)

  
   # Create Treeview Frame
    tree_frame = Frame(root)
    tree_frame.pack(pady=20)

    # Treeview Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create Treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    my_tree['columns'] = output_headers

    # Content Generator Tree
    contentFrame = Frame(root)
    contentFrame.pack(pady=20)

    
    contentHeaders = 'Content'
    contentTree = ttk.Treeview(contentFrame)
    contentTree['columns'] = contentHeaders

    contentTree.column("#0", width=0, stretch=YES)
    contentTree.column('Content', anchor=CENTER, width=400)

    contentTree.heading("#0", text="", anchor=CENTER)
    contentTree.heading('Content', text="Content", anchor=CENTER)

    print(contentGeneratorText)
    contentTree.insert(parent="", index='end', iid=0, values=(contentGeneratorText))

    #Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    
    #Format columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column('#', anchor=CENTER, width=40)
    my_tree.column('output_item_name', anchor=W, width=400)
    my_tree.column('output_item_rating', anchor=CENTER, width=120)
    my_tree.column('output_item_num_reviews', anchor=CENTER, width=180)

    #headers
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("#", text="#", anchor=CENTER)
    my_tree.heading("output_item_name", text="output_item_name", anchor=CENTER)
    my_tree.heading("output_item_rating", text="output_item_rating", anchor=CENTER)
    my_tree.heading("output_item_num_reviews", text="output_item_num_reviews", anchor=CENTER)

    counter = 0
    #Adds the correct info from the final cut array to the tree
    for i in cut_row:
        my_tree.insert(parent="", index='end', iid=counter, values=(counter + 1, i[0], i[1], i[2]))
        counter +=1
        
    my_tree.pack()
    contentTree.pack()


def sort_alg(num, category_selected, csv_file, flag=0):
    # Merge Sort
    number = int(num)
    new_arr = []
    # This deals with the auto files 
    if flag == 1:
        category_selected = category_selected + ' '

    for row in csv_file:
        try:
            if row[8]== "":
                continue
            else:
                item = row[8]
                split = item.split(">")
                split = split[:-1]
                
                if split[0] == category_selected:
                    new_arr.append(row)
                    #print('yeye')
                else:
                    continue
        except:
            continue

    # Sorts by Unique ID #Z-A 0-9 0 on top Z on bottom per piazza
    sorted_id = merge_sort(new_arr)
    #for i in range(1000):
        #print(sorted_id[i][0], sorted_id[i][1])

    # Sorts by # of reviews
    sorted_rev = merge_sort(sorted_id, 1)
    
    #print(' top ten ID + Sorted reviews')
    #count = 0
    #for i in range(100):
        #print(count +1, sorted_rev[i][0], sorted_rev[i][5])
        #count += 1
    
    # Take top x * 10 results
    top_ten = []
    range_num = 10 * number
    for i in range(range_num):
        try:
            top_ten.append(sorted_rev[i])
        except:
            break

    #for i in range(range_num):
        #print(top_ten[i][0])

    #Sorts top x * 10 by uniq ID #Z-A 0-9 0 on top Z on bottom per piazza
    ten_uniq = merge_sort(top_ten)
    #for i in range(10):
        #try:
            #print(ten_uniq[i][0])
            #print(ten_uniq[i][1])
            #print(ten_uniq[i][5])
            #print(ten_uniq[i][7])
        #except:
            #break

    #Sorts top10uniqID by avg review (high to low)
    ten_avg = merge_sort(ten_uniq, 2)
    #for i in range(range_num):
        #try:
            #print(ten_avg[i][7])
        #except:
            #break

    final_arr = []
    for i in range(number):
        try:
            final_arr.append(ten_avg[i])
            #print(final_arr[i][0], final_arr[i][7])
        except:
            break
    #Does stuff from there
    return final_arr


def merge(left, right):
    """Merge to deal with unique ID"""
    values = {"0": 0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "a":10, "b":11, "c":12, "d":13, "e": 14, "f": 15, "g":16, "h":17, "i":18,
"j":19, "k":20, "l":21, "m":22, "n":23, "o":24, "p":25, "q":26, "r":27, "s":28, "t":29, "u":30, "v":31, "w":32, "x":33, "y":34, "z":35}
    
    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        L = left[left_index][0]
        R = right[right_index][0]

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

        if values[left_first] < values[right_first]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result


def merge_sort(array, flag=0):
    """Base merge all mergs will call falgs deligate where to go"""
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
    """Merge to deal with average_reviews"""

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
    """Merge to deal with number_of_reviews"""

    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        lefty = left[left_index]
        righty = right[right_index]

        l_string = lefty[5]
        #Deals with the few numbers that have commas
        l_string = l_string.replace(',','') 
        # Deals with blanks in the rating, assigns them 0
        if len(l_string) > 0:
            left_first = int(l_string)
        else:
            left_first = 0
        r_string = righty[5]
        
        #Deals with the few numbers that have commas
        r_string = r_string.replace(',','')
        # Deals with blanks in the rating, assigns them 0
        if len(r_string) > 0:
            right_first = int(r_string)
        else:
            right_first = 0

        if left_first > right_first:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result
    

def main():
    """Main creates GUI, auto called if nothing in syst args"""
    global root
    root = Tk()
    root.title('Life Generator')
    root.geometry("1000x1200")
    global frame_above
    frame_above = Frame(root)
    frame_above.pack(side = TOP)
    global frame_top
    frame_top = Frame(root)
    global frame_bottom
    frame_bottom = Frame(root)
    frame_top.pack(side = TOP)
    frame_bottom.pack(side = BOTTOM)
    global fh
    try:
        fh = open('amazon_co-ecommerce_sample.csv', "r", encoding='utf-8')
        global csv_file
        csv_file = csv.reader(fh)
        #print('Upload successful')
        #print(csv_file)
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

    global clicked
    clicked = StringVar()
    clicked.set(cat_arr[1])

    # Number Input boxes
    global e 
    e = Entry(frame_top, width =25)
    e.grid(row = 0, column = 0, padx = 10)
    e.insert(0, "3")

    global my_parameter
    my_parameter = Button(frame_top, text="Confirm Parameters", width = 25, command=my_par_click)
    my_parameter.grid(row = 0, column = 1, padx = 10)

    #Drop down box
    global drop
    drop = OptionMenu(frame_top, clicked, *cat_arr[1:])
    drop.grid(row = 1, column = 0)

    # Generate stuff
    global clicked_generate
    clicked_generate = StringVar()

    global Gen_button
    Gen_button = Button(frame_top, text="Generate", width = 25, command=normal)
    Gen_button.grid(row = 0, column = 2, padx = 10)

    # Reset button
    global clicked_newSearch
    clicked_newSearch = StringVar()
    clicked_newSearch.set('Generate!!!!!!!!!!')

    global newSearch_button
    newSearch_button = Button(frame_top, text="New Search", width = 25, command=new_search)
    newSearch_button.grid(row = 0, column = 3, padx = 10)


    my_label1 = Label(frame_above, width = 100, font=('Helvetica', 10), text="Welcome! Please Select your parameters and Press 'Confirm Parameters' then press 'Generate'. Press 'New Search' to start over.")
    my_label1.grid(row=1, column = 1, rowspan=3, pady = 10)


    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        auto()
    else:
        main()