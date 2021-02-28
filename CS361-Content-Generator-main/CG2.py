# Name: Josh Nguyen
# Date: 2/14/2021
# Class: CS361
# Description: This program generates text based off of inputted keywords.

from tkinter import *
from tkinter import ttk
import requests as res
import bs4 as bs


def request_html(keyword):
    """Requests the HTML from the Wiki page"""
    request = res.get(keyword)
    wiki_html = bs.BeautifulSoup(request.text, "html.parser")
    return wiki_html


def create_url(keyword):
    """Attach keyword into URL format"""
    wiki_url = "https://en.wikipedia.org/wiki/"
    wiki_url += keyword
    return wiki_url


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

    website_url = create_url(p_keyword)
    wiki_data = request_html(website_url)
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


open_gui()
