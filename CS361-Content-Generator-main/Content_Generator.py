# Name: Josh Nguyen
# Date: 2/14/2021
# Class: CS361
# Description: This program generates text based off of inputted keywords.

from tkinter import *
from tkinter import ttk
import requests as res
import bs4 as bs
import csv


def request_html(keyword):
    """Requests the HTML from the Wiki page"""
    wiki_url = "https://en.wikipedia.org/wiki/" + keyword  # create wiki URL
    request = res.get(wiki_url)
    wiki_html = bs.BeautifulSoup(request.text, "html.parser")  # get HTML from site
    return wiki_html


def parse_wiki_data(data, primary_keyword, secondary_keyword):
    """Parse through Wiki page for paragraphs containing the secondary keyword"""

    for p in data.find_all("p"):
        if (primary_keyword in p.get_text()) and (secondary_keyword in p.get_text()):
            for c in p:  # go through contents of paragraph to remove citations (eg: [2])
                if isinstance(c, bs.element.Tag):
                    if c.name == "sup":  # remove citation numbers from lines
                        c.clear()
            return p.get_text()  # output paragraph as string

    return "No matches found."  # For no matches


def generate_output(p_keyword, s_keyword, result):
    """Generates the output text"""
    p_keyword = str(p_keyword)
    s_keyword = str(s_keyword)

    wiki_data = request_html(p_keyword)
    result.set(parse_wiki_data(wiki_data, p_keyword, s_keyword))


def open_gui():

    root = Tk()
    root.title("Content Generator")

    # Create window
    mainframe = ttk.Frame(root, padding="20 20 20 20")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Set entry field for primary keyword
    primary_keyword = StringVar()
    primary_keyword_field = ttk.Entry(mainframe, width=20, textvariable=primary_keyword)
    primary_keyword_field.grid(column=2, row=1, sticky=(W, E))

    # Set entry field for secondary keyword
    secondary_keyword = StringVar()
    secondary_keyword_field = ttk.Entry(mainframe, width=20, textvariable=secondary_keyword)
    secondary_keyword_field.grid(column=2, row=2, sticky=(W, E))

    # Create and place "Generate" button
    ttk.Button(mainframe, text="Generate",
               command=lambda: generate_output(primary_keyword.get(), secondary_keyword.get(), result)).grid(
                column=3, row=3, sticky=W)

    # Create "Download Output" button
    ttk.Button(mainframe, text="Download Output",
               command= lambda: download_output(primary_keyword.get(), secondary_keyword.get())).grid(
                column=2, row=3, sticky=E)

    # Create field labels for Primary & Secondary Keyword
    ttk.Label(mainframe, text="Primary Keyword").grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, text="Secondary Keyword").grid(column=1, row=2, sticky=W)

    # Create field label for output text
    ttk.Label(mainframe, text="Generated Text").grid(column=1, row=4, sticky=W)

    # Create field for output text to print
    result = StringVar()
    result.set(" ")
    ttk.Label(mainframe, textvariable=result, wraplength=500).grid(column=2, row=5, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Highlight primary keyword field by default
    primary_keyword_field.focus()

    # Bind "Enter" key press
    root.bind("<Return>", lambda x: generate_output(primary_keyword.get(), secondary_keyword.get(), result))
    root.mainloop()


def download_output(p_key, s_key):
    """Takes the keywords and places them into a dict. Generates output.csv using generate_output_csv()"""
    keyword_dictionary = {p_key: s_key}
    generate_output_csv(keyword_dictionary)


def parse_input_csv(csv_data):
    """Parses through the CSV file for the keywords and returns the keywords as a dictionary"""
    raw_data = [line.split(";") for line in csv_data.split("\n")]
    raw_data = raw_data[1:]
    return dict(raw_data)  # format = {primary keyword:secondary keyword}


def generate_output_csv(keywords):
    """Reads in dictionary of keywords to call parse_wiki_data, then writes to output.csv"""
    with open('output.csv', mode='w') as csv_file:
        header_names = ["input_keywords", "output_content"]
        writer = csv.DictWriter(csv_file, fieldnames=header_names)

        writer.writeheader()

        for k, v in keywords.items():
            wiki_page = request_html(k)
            writer.writerow({"input_keywords": k + ";" + v, "output_content": parse_wiki_data(wiki_page, k, v)})


if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    keyword_dict = parse_input_csv(contents)
    generate_output_csv(keyword_dict)

else:
    open_gui()
