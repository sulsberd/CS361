# Project: life-generator
# Name: Danny Sulsberger
# Date: 14FEB2021
# See assignment 3.4 requirements for functionality
# Project is POC for use case

from tkinter import *
from tkinter import ttk
import csv
import sys

def noGui():
    global amazonDB
    amazonDB = openDB()
    noGuiInputs = openInput()
    noGUIResults = sortInputs(noGuiInputs, 1)
    makeOutputFile(noGUIResults, noGuiInputs)

def openDB():
    global unreadDB
    unreadDB = open('amazon_co-ecommerce_sample.csv', "r", encoding='utf-8-sig')
    amazonDB = csv.reader(unreadDB)
    print('Database upload successful')
    return amazonDB

def openInput():
    finput = open('input.csv', "r", encoding='utf-8-sig')
    inputFile= csv.reader(finput)
    print('Input CSV upload successful')
    inputArr = parseInputRows(inputFile)
    noGuiInputs = getInputs(inputArr)
    return noGuiInputs

def parseInputRows(inputFile):
    inputArr = []
    for row in inputFile:
        try:            
            inputArr.append(row)
        except:
            continue
    
    return inputArr

def getInputs(inputArr):
    itemType = inputArr[1][0]
    categorySelected = inputArr[1][1]
    numberOfResultsParameter = inputArr[1][2]

    noGuiInputs = []
    noGuiInputs.append(itemType)
    noGuiInputs.append(categorySelected)
    noGuiInputs.append(numberOfResultsParameter)
    return itemType, categorySelected, numberOfResultsParameter

def sortInputs(inputs, flag=0):
    
    numberOfResultsParameter = inputs[2]
    categorySelected = inputs[1]
    categorySelected = guiFormating(categorySelected, flag)
    
    # Merge Sort
    numberOfResultsParameter = int(numberOfResultsParameter)
    filteredByCategory = filterByCategory(categorySelected)

    normalizedResults = normalizingFilter(filteredByCategory, numberOfResultsParameter)
    return normalizedResults

def guiFormating(categorySelected, flag):
    if flag == 1:
        categorySelected = categorySelected + ' '

    return categorySelected

def filterByCategory(categorySelected):
    filteredByCategory = []
    for row in amazonDB:
        try:
            checkBlankCategory(categorySelected, filteredByCategory, row)
        except:
            continue

    return filteredByCategory

def makeOutputFile(noGUIResults, noGuiInputs):
    outputFile = open('output.csv', 'w', newline='')

    outputHeaders = ['input_item_type', 'input_item_category', 'input_number_to_generate',
    'output_item_name', 'output_item_rating', 'output_item_num_reviews']
    writeOutput(outputFile, outputHeaders, noGUIResults, noGuiInputs)

def writeOutput(outputFile, outputHeaders, noGUIResults, noGuiInputs):
    outputWriter = csv.writer(outputFile)
    outputWriter.writerow(outputHeaders)
    writeResults(noGUIResults, noGuiInputs, outputWriter)
    print('output.csv export successful')
    outputFile.close()

    unreadDB.seek(0)

def writeResults(noGUIResults, noGuiInputs, outputWriter):
    tempRow = []
    for rows in noGUIResults:
        tempRow.append(noGuiInputs[0])
        tempRow.append(noGuiInputs[1])
        tempRow.append(noGuiInputs[2])
        tempRow.append(rows[1]) # Item name
        tempRow.append(rows[7]) # Item Rating
        tempRow.append(rows[5]) # Number of Review
        outputWriter.writerow(tempRow)
        tempRow=[]


def confirmParameterClick():
    """button to confirm the parameters"""
    global numberOfResultsParameter
    numberOfResultsParameter = numberOfResults.get()
    confirmParameters['state'] = DISABLED
    numberOfResults['state'] = DISABLED

def newSearchClick():
    """Function to reset search to default"""
    unreadDB.seek(0)
    numberOfResults['state'] = NORMAL
    generateButton['state'] = NORMAL
    confirmParameters['state'] = NORMAL

def inputFormatting(category):
    inputs = []
    inputs.append('toy')
    inputs.append(category)
    inputs.append(numberOfResultsParameter)
    return inputs

def generateResult():
    """This is used as the GUI helper"""
    confirmParameters['state'] = DISABLED
    generateButton['state'] = DISABLED
    #DeleteButton['state'] = DISABLED
    category = categorySelection.get()
    inputs = inputFormatting(category)

    GUIResults = sortInputs(inputs)
    outputHeaders = ('#', 'output_item_name', 'output_item_rating', 'output_item_num_reviews')
        
    resultFormatForTrees = []
    for rows in GUIResults:
        tempRow = []
        tempRow.append(rows[1]) # Item Name
        tempRow.append(rows[7]) # Item Rating
        tempRow.append(rows[5]) # Num of Reviews
        resultFormatForTrees.append(tempRow)

    createTreeView(outputHeaders, resultFormatForTrees)

def createTreeView(outputHeaders, resultFormatForTrees):
    treeFrame = createFrame()
    treeScroll = createScrollbar(treeFrame)
    treeView = createView(outputHeaders, treeScroll, treeFrame)
    configureScrollBar(treeScroll, treeView)
    addResultsToTree(resultFormatForTrees, treeView)

def createFrame():
    treeFrame = Frame(root)
    treeFrame.pack(pady=20)
    return treeFrame

def createScrollbar(treeFrame):
    treeScroll = Scrollbar(treeFrame)
    treeScroll.pack(side=RIGHT, fill=Y)
    return treeScroll

def createView(outputHeaders, treeScroll, treeFrame):
    treeView = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set)
    treeView['columns'] = outputHeaders
    formatTreeColumns(treeView)
    formatTreeHeaders(treeView)
    return treeView

def configureScrollBar(treeScroll, treeView):
    treeScroll.config(command=treeView.yview)

def formatTreeColumns(treeView):   
    treeView.column("#0", width=0, stretch=NO)
    treeView.column('#', anchor=CENTER, width=40)
    treeView.column('output_item_name', anchor=W, width=400)
    treeView.column('output_item_rating', anchor=CENTER, width=120)
    treeView.column('output_item_num_reviews', anchor=CENTER, width=180)

def formatTreeHeaders(treeView):
    treeView.heading("#0", text="", anchor=CENTER)
    treeView.heading("#", text="#", anchor=CENTER)
    treeView.heading("output_item_name", text="output_item_name", anchor=CENTER)
    treeView.heading("output_item_rating", text="output_item_rating", anchor=CENTER)
    treeView.heading("output_item_num_reviews", text="output_item_num_reviews", anchor=CENTER)

def addResultsToTree(resultFormatForTrees, treeView):
    counter = 0
    for resultRow in resultFormatForTrees:
        itemName = resultRow[0]
        itemRating = resultRow[1]
        numberReviews = resultRow[2]
        treeView.insert(parent="", index='end', iid=counter, values=(counter + 1, itemName, itemRating, numberReviews))
        counter +=1
        
    treeView.pack()


def filterFormatting(categoryInRow):
    unformatedCategory = categoryInRow
    formattedCategory = unformatedCategory.split(">")
    return formattedCategory

def checkBlankCategory(categorySelected, filteredByCategory, row):
    categoryInRow = row[8]
    if categoryInRow== "":
        return
    else:
        formattedCategory = filterFormatting(categoryInRow)
        formattedCategory = formattedCategory[:-1]
        if formattedCategory[0] == categorySelected:
            filteredByCategory.append(row)
    return


def normalizingFilter(filteredByCategory, numberOfResultsParameter):

    sortedById = mergeSort(filteredByCategory)
    sortedByReview = mergeSort(sortedById, 1) 
    normalizedRangeArray = normalizedRangeLoop(numberOfResultsParameter, sortedByReview)
    normalizedSortedById = mergeSort(normalizedRangeArray)
    normalizedSortedByAvgReview = mergeSort(normalizedSortedById, 2)

    filterResults = finalResultsArray(numberOfResultsParameter, normalizedSortedByAvgReview)
    return filterResults

def normalizedRangeLoop(numberOfResultsParameter, sortedByReview):
    normalizedRangeArray = []
    normalizedRange = 10 * numberOfResultsParameter
    for i in range(normalizedRange):
        try:
            normalizedRangeArray.append(sortedByReview[i])
        except:
            break
    return normalizedRangeArray

def finalResultsArray(numberOfResultsParameter, normalizedSortedByAvgReview):
    filterResults = []
    for i in range(numberOfResultsParameter):
        try:
            filterResults.append(normalizedSortedByAvgReview[i])
        except:
            break
    return filterResults

def merge(left, right):
    """Merge to deal with unique ID"""
    values = {"0": 0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, 
    "a":10, "b":11, "c":12, "d":13, "e": 14, "f": 15, "g":16, "h":17, "i":18,
    "j":19, "k":20, "l":21, "m":22, "n":23, "o":24, "p":25, "q":26, "r":27, "s":28, 
    "t":29, "u":30, "v":31, "w":32, "x":33, "y":34, "z":35}
    
    leftIndex, rightIndex = 0, 0
    result = []
    while leftIndex < len(left) and rightIndex < len(right):
        leftIDValue = left[leftIndex][0]
        rightIDValue = right[rightIndex][0]

        if len(leftIDValue) < len(rightIDValue):
            shorterValue = leftIDValue
        else:
            shorterValue = rightIDValue

        for i in range(len(shorterValue)):
            leftDigitValue = left[leftIndex][0][i]
            rightDigitValue = right[rightIndex][0][i]

            if values[leftDigitValue] == values[rightDigitValue]:
                continue
            else:
                break

        if values[leftDigitValue] < values[rightDigitValue]:
            result.append(left[leftIndex])
            leftIndex += 1
        else:
            result.append(right[rightIndex])
            rightIndex += 1

    result += left[leftIndex:]
    result += right[rightIndex:]
    return result


def mergeSort(array, flag=0):
    """Base merge all mergs will call falgs deligate where to go"""
    if len(array) <= 1:  # base case
        return array

    if flag == 1:
        # divide array in half and merge sort recursively
        half = len(array) // 2
        left = mergeSort(array[:half], 1)
        right = mergeSort(array[half:], 1)

        return merge_reviews(left, right, 1)

    if flag == 2:
        # divide array in half and merge sort recursively
        half = len(array) // 2
        left = mergeSort(array[:half], 2)
        right = mergeSort(array[half:], 2)

        return merge_average(left, right, 2)

    else:
    # divide array in half and merge sort recursively
        half = len(array) // 2
        left = mergeSort(array[:half])
        right = mergeSort(array[half:])

        return merge(left, right)

def merge_average(left, right, sort_number):
    """Merge to deal with average_reviews"""

    leftIndex, rightIndex = 0, 0
    result = []
    while leftIndex < len(left) and rightIndex < len(right):
        leftValue = left[leftIndex]
        rightValue = right[rightIndex]

        leftString = leftValue[7]
        leftStringSplit = leftString.split(" ")
        leftDigitValue = leftStringSplit[0]
        rightString = rightValue[7]
        rightStringSplit = rightString.split(" ")
        rightDigitValue = rightStringSplit[0]

        if leftDigitValue > rightDigitValue:
            result.append(left[leftIndex])
            leftIndex += 1
        else:
            result.append(right[rightIndex])
            rightIndex += 1

    result += left[leftIndex:]
    result += right[rightIndex:]
    return result

def merge_reviews(left, right, sort_number):
    """Merge to deal with number_of_reviews"""

    leftIndex, rightIndex = 0, 0
    result = []
    while leftIndex < len(left) and rightIndex < len(right):
        leftValue = left[leftIndex]
        rightValue = right[rightIndex]

        leftString = leftValue[5]
        #Deals with the few numbers that have commas
        leftString = leftString.replace(',','') 
        # Deals with blanks in the rating, assigns them 0
        if len(leftString) > 0:
            leftDigitValue = int(leftString)
        else:
            leftDigitValue = 0
        rightString = rightValue[5]
        
        #Deals with the few numbers that have commas
        rightString = rightString.replace(',','')
        # Deals with blanks in the rating, assigns them 0
        if len(rightString) > 0:
            rightDigitValue = int(rightString)
        else:
            rightDigitValue = 0

        if leftDigitValue > rightDigitValue:
            result.append(left[leftIndex])
            leftIndex += 1
        else:
            result.append(right[rightIndex])
            rightIndex += 1

    result += left[leftIndex:]
    result += right[rightIndex:]
    return result
    

def gui():
    """Main creates GUI, auto called if nothing in syst args"""
    global unreadDB
    createGUI()
    DropDownMenuArray = makeDropDownMenu()
    makeButtons(DropDownMenuArray)
    root.mainloop()

def createGUI():
    global root
    root = Tk()
    root.title('Life Generator')
    root.geometry("1000x1200")
    createGUIFrames(root)
    
    
def createGUIFrames(root):
    global welcomeFrame
    global topFrame
    global bottomFrame
    welcomeFrame = Frame(root)
    welcomeFrame.pack(side = TOP)

    topFrame = Frame(root)
    bottomFrame = Frame(root)
    topFrame.pack(side = TOP)
    bottomFrame.pack(side = BOTTOM)

def makeDropDownMenu():
    global amazonDB
    amazonDB = openDB()
    DropDownMenuArray = makeDropDownMenuArray(amazonDB)
    #Returns DB to top line, needed if second search made
    unreadDB.seek(0)
    return DropDownMenuArray

def makeDropDownMenuArray(amazonDB):
    DropDownMenuArray = []
    for row in amazonDB:
        categoryInRow = row[8]
        if categoryInRow== "":
            continue
        else:
            formattedCategory = filterFormatting(categoryInRow)
            addCategoryToDropdown(DropDownMenuArray, formattedCategory)      

    return DropDownMenuArray

def addCategoryToDropdown(DropDownMenuArray, formattedCategory):
    if formattedCategory[0] in DropDownMenuArray:
        return DropDownMenuArray
    else:
        DropDownMenuArray.append(formattedCategory[0])
        return DropDownMenuArray

def makeButtons(DropDownMenuArray):
    global categorySelection
    categorySelection = StringVar()
    categorySelection.set(DropDownMenuArray[1])

    global categoryDropDownMenu
    categoryDropDownMenu = OptionMenu(topFrame, categorySelection, *DropDownMenuArray[1:])
    categoryDropDownMenu.grid(row = 1, column = 0)

    global numberOfResults 
    numberOfResults = Entry(topFrame, width =25)
    numberOfResults.grid(row = 0, column = 0, padx = 10)
    numberOfResults.insert(0, "3")

    global confirmParameters
    confirmParameters = Button(topFrame, text="Confirm Parameters", width = 25, command=confirmParameterClick)
    confirmParameters.grid(row = 0, column = 1, padx = 10)

    global generateButton
    generateButton = Button(topFrame, text="Generate", width = 25, command=generateResult)
    generateButton.grid(row = 0, column = 2, padx = 10)

    global newSearch
    newSearch = Button(topFrame, text="New Search", width = 25, command=newSearchClick)
    newSearch.grid(row = 0, column = 3, padx = 10)

    welcomeLabel = Label(welcomeFrame, width = 100, font=('Helvetica', 10), text="Welcome! Please Select your parameters and Press 'Confirm Parameters' then press 'Generate'. Press 'New Search' to start over.")
    welcomeLabel.grid(row=1, column = 1, rowspan=3, pady = 10)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        noGui()
    else:
        gui()