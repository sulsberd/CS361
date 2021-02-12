from tkinter import *
from tkinter import ttk
import csv
import sys

#root = Tk()
#root.title('Life Generator')
#root.geometry("800x600")

def auto_variables(input_arr):
    """This prepares the values in the input.csv for the auto-run"""
    result_dictionary = {}
    #print(input_arr, 'input arr')
    #print(input_arr[0])
    header = 0
    key_values = []
    for i in range(len(input_arr[0])):
        temp = []
        key_n = input_arr[0][i]
        value_n = input_arr[1][i]
        temp.append(key_n)
        temp.append(value_n)
        key_values.append(temp)

    for i in range(len(key_values)):
        key = key_values[i][0]
        value = key_values[i][1]
        result_dictionary[key] = value        

        #input_item_type = None

    loop = ['input_item_type', 'input_item_category', 'input_number_to_generate']
    keys = result_dictionary.keys()
    
    item_type = result_dictionary[loop[0]]
    category_type = result_dictionary[loop[1]]
    num_generate = result_dictionary[loop[2]]

    #print(item_type, category_type, num_generate)
    #print(result_dictionary, 'result dictionary')
    return item_type, category_type, num_generate

def auto_run(item_type, category_type, num_generate, csv_file):
    print('autorun beep')
    auto_result = sort_alg(num_generate, category_type, csv_file, 1)
    #print(auto_result)
    return auto_result

# Delete button func
def myDelete():
    try:
        #myLabel.destroy()
        myButton['state'] = NORMAL
        #show_Label.destroy()
        show_button['state'] = NORMAL
    except:
        return

# Input function
def myClick():
    global myLabel
    global num
    num = e.get()
    #print(num + 'num in here')
    #myLabel = Label(root, text=num)
    #e.delete(0, 'end')
    #myLabel.pack()
    myButton['state'] = DISABLED

#Drop down box
# Defining click def as a string bc our variables are strings
# Using a list to populate the dropdown

"""
def show():
    global show_Label
    click = clicked.get()
    show_Label = Label(root, text=click)
    show_Label.pack(pady=10)
    show_button['state'] = DISABLED
"""
def new_search():
    fh.seek(0)
    Gen_button['state'] = NORMAL
    #myLabel.destroy()
    myButton['state'] = NORMAL
    #show_Label.destroy()
    #DeleteButton['state'] = NORMAL

#Generate button

# THIS MAY NOT BE USED NOW
def show_gen():
    global gen_label
    clicked_gen = clicked_generate.get()
    #gen_label = Label(root, text=clicked_gen)
    #gen_label.pack(pady=10)

def normal():
    """This is used as the GUI helper"""
    myButton['state'] = DISABLED
    #DeleteButton['state'] = DISABLED
    step_before = alg_helper()
    output_headers = ('#', 'output_item_name', 'output_item_rating', 'output_item_num_reviews')
        
    cut_row = []
    for rows in step_before:
        temp_row = []
        temp_row.append(rows[1])
        temp_row.append(rows[5])
        temp_row.append(rows[7])
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

    #Data
    #my_tree.insert(parent="", index='end', iid=0, values=("John", 1, "Pepperoni"))

    #example = ['danny']
    counter = 0
    for i in cut_row:
        my_tree.insert(parent="", index='end', iid=counter, values=(counter + 1, i[0], i[1], i[2]))
        counter +=1
        
    my_tree.pack()

def alg_helper():
    Gen_button['state'] = DISABLED
    category = clicked.get()
    #print(num, category)

    alg_result = sort_alg(num, category, csv_file)
    #print(alg_result)
    return alg_result

def sort_alg(num, category_selected, csv_file, flag=0):
    #Takes category keyword
    #print(num, 'this is num')
    number = int(num)
    new_arr = []
    if flag == 1:
        category_selected = category_selected + ' '

    for row in csv_file:
        try:
            if row[8]== "":
                continue
            else:
                item = row[8]
                split = item.split(">")
                
                if split[0] == category_selected:
                    new_arr.append(row)
                    #print('yeye')
                else:
                    continue
        except:
            continue
    #print(len(new_arr))

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
    #for i in range(range_num):
        #try:
            #print(ten_uniq[i][0])
        #except:
            #break

    #Sorts top10uniqID by avg review
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
    
def auto():
    if len(sys.argv) > 1:
        fh = open('CSV_DOC.csv', "r", encoding='utf-8-sig')
        global csv_file
        csv_file = csv.reader(fh)
        print('Upload successful')
        print(csv_file)
        cat_arr = []

        finput = open('input.csv', "r", encoding='utf-8-sig')
        input_file= csv.reader(finput)
        print('Input upload successful')

        input_arr = []
        counter = 0
        for row in input_file:
            try:            
                input_arr.append(row)

            except:
                continue

        #print(input_arr, 'input arr')
        citem_type, ccategory_type, cnum_generate = auto_variables(input_arr)
        #print(citem_type)
        #print(ccategory_type)
        #Fprint(cnum_generate)
        automatic_result = auto_run(citem_type, ccategory_type, cnum_generate, csv_file)
        #print(automatic_result[0])
    
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
            temp_row.append(rows[1])
            temp_row.append(rows[5])
            temp_row.append(rows[7])
            output_writer.writerow(temp_row)
            temp_row=[]
        #print(automatic_result)

        output_file.close()


        fh.seek(0)
        counter = 0
        headers = 0
        while counter == 0:
            for row in csv_file:
                headers = row
                break
            counter +=1
        #print(headers)
        
        count = 0
        header_keys = output_headers
        #print(header_keys, 'header keys')
        #print(headers, 'headers')
        #for heads in headers:
            #if heads == "":
                #continue
            #if heads in header_keys:
                #print('heads yesyes')

def main():
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
        fh = open('CSV_DOC.csv', "r", encoding='utf-8')
        global csv_file
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

    global clicked
    clicked = StringVar()
    clicked.set(cat_arr[1])

    # Number Input boxes
    global e 
    e = Entry(frame_top, width =25)
    e.grid(row = 0, column = 0, padx = 10)
    e.insert(0, "3")

    global myButton
    myButton = Button(frame_top, text="Confirm Parameters", width = 25, command=myClick)
    myButton.grid(row = 0, column = 1, padx = 10)

    #Drop down box
    global drop
    drop = OptionMenu(frame_top, clicked, *cat_arr[1:])
    drop.grid(row = 1, column = 0)
    """
    global show_button
    show_button = Button(frame_top, text="Confirm Category", width = 25, command=show)
    show_button.grid(row = 1, column = 1)"""
    """
    global DeleteButton
    DeleteButton = Button(frame_top, text = "Clear parameters", width = 25, command=myDelete)
    DeleteButton.grid(row = 1, column = 1)
    """

    # Generate stuff
    global clicked_generate
    clicked_generate = StringVar()
    clicked_generate.set('Generate!!!!!!!!!!')

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

    #myTree = ttk.Treeview(root)


    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        auto()
    else:
        main()