# import pymongo
import datetime
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('File Management GUI')
root.geometry("700x700")


def enter_paper():
    enter_label.grid_forget()
    enter_paper.grid_forget()
    enter_author.grid_forget()
    enter_pub.grid_forget()
    enter_back.grid_forget()
    input_title_flavor.grid(row=0, column=0)
    input_title.grid(row=0, column=3)
    input_author_f_flavor.grid(row=1, column=0)
    input_author_f.grid(row=1, column=3)
    input_author_l_flavor.grid(row=2, column=0)
    input_author_l.grid(row=2, column=3)
    input_pub_flavor.grid(row=3, column=0)
    input_pub.grid(row=3, column=3)
    input_URL_flavor.grid(row=4, column=0)
    input_URL.grid(row=4, column=3)
    input_Pages_flavor.grid(row=5, column=0)
    input_Pages.grid(row=5, column=3)
    input_paper_submit.grid(row=6)
    return


def submitpaper():
    input_title_flavor.grid_forget()
    input_author_f_flavor.grid_forget()
    input_author_l_flavor.grid_forget()
    input_URL_flavor.grid_forget()
    input_Pages_flavor.grid_forget()

    input_title.grid_forget()
    input_author_f.grid_forget()
    input_author_l.grid_forget()
    input_URL.grid_forget()
    input_Pages.grid_forget()
    input_paper_submit.grid_forget()
    input_pub_flavor.grid_forget()
    input_pub.grid_forget()

    input_title.delete(0, END)
    input_author_f.delete(0, END)
    input_author_l.delete(0, END)
    input_URL.delete(0, END)
    input_Pages.delete(0, END)

    input_successful.grid(row=0)
    enter_back.grid(row=1)
    return


def enter_author():
    enter_label.grid_forget()
    enter_paper.grid_forget()
    enter_author.grid_forget()
    enter_pub.grid_forget()
    enter_back.grid_forget()

    input_author_f1_flavor.grid(row=1, column=0)
    input_author_f1.grid(row=1, column=3)
    input_author_l1_flavor.grid(row=2, column=0)
    input_author_l1.grid(row=2, column=3)
    input_author_affil1_flavor.grid(row=3, column=0)
    input_author_affil1.grid(row=3, column=3)
    input_author_affil2_flavor.grid(row=4, column=0)
    input_author_affil2.grid(row=4, column=3)
    input_author_affil3_flavor.grid(row=5, column=0)
    input_author_affil3.grid(row=5, column=3)
    input_author_submit.grid(row=6)
    return


def submitauthor():
    input_author_f1_flavor.grid_forget()
    input_author_f1.grid_forget()
    input_author_l1_flavor.grid_forget()
    input_author_l1.grid_forget()
    input_author_affil1_flavor.grid_forget()
    input_author_affil1.grid_forget()
    input_author_affil2_flavor.grid_forget()
    input_author_affil2.grid_forget()
    input_author_affil3_flavor.grid_forget()
    input_author_affil3.grid_forget()
    input_author_submit.grid_forget()

    input_author_f1.delete(0, END)
    input_author_l1.delete(0, END)
    input_author_affil1.delete(0, END)
    input_author_affil2.delete(0, END)
    input_author_affil3.delete(0, END)

    input_successful.grid(row=0)
    enter_back.grid(row=1)
    return


def enter_publication():
    enter_label.grid_forget()
    enter_paper.grid_forget()
    enter_author.grid_forget()
    enter_pub.grid_forget()
    enter_back.grid_forget()
    pub_type.grid(row=0)
    input_pub_conference.grid(row=1)
    input_pub_journal.grid(row=2)
    return


def enter_data():
    base_label.grid_forget()
    data_entry_button.grid_forget()
    query_data_button.grid_forget()
    exit_button.grid_forget()

    enter_label.grid(row=0, column=3)

    enter_paper.grid(row=1, column=0, columnspan=4)

    enter_author.grid(row=2, column=0, columnspan=4)

    enter_pub.grid(row=3, column=0, columnspan=4)

    enter_back.grid(row=4, column=0, columnspan=4)

    return


def insertreset():
    enter_label.grid_forget()
    enter_paper.grid_forget()
    enter_author.grid_forget()
    enter_pub.grid_forget()
    enter_back.grid_forget()
    input_successful.grid_forget()

    base_label.grid(row=0, column=3)
    data_entry_button.grid(row=1, column=0, columnspan=4)
    query_data_button.grid(row=2, column=0, columnspan=4)
    exit_button.grid(row=3, column=0, columnspan=4)
    return


def isconference():
    pub_type.grid_forget()
    input_pub_conference.grid_forget()
    input_pub_journal.grid_forget()
    return


def isjournal():
    pub_type.grid_forget()
    input_pub_conference.grid_forget()
    input_pub_journal.grid_forget()

    pub_name_flavor.grid(row=0, column=0)
    pub_name.grid(row=0, column=3)
    pub_year_flavor.grid(row=1, column=0)
    pub_year.grid(row=1, column=3)
    pub_month_flavor.grid(row=2, column=0)
    pub_month.grid(row=2, column=3)
    pub_edition_flavor.grid(row=3, column=0)
    pub_edition.grid(row=3, column=3)
    input_pub_submit.grid(row=4)
    return


def submitpub():
    pub_name_flavor.grid_forget()
    pub_name.grid_forget()
    pub_year_flavor.grid_forget()
    pub_year.grid_forget()
    pub_month_flavor.grid_forget()
    pub_month.grid_forget()
    pub_edition_flavor.grid_forget()
    pub_edition.grid_forget()
    input_pub_submit.grid_forget()
    input_successful.grid(row=0)
    enter_back.grid(row=1)
    return


def query_data():
    base_label.grid_forget()
    data_entry_button.grid_forget()
    query_data_button.grid_forget()
    exit_button.grid_forget()

    query_label.grid(row=0, column=3)

    query_paper.grid(row=1, column=0, columnspan=4)

    query_author.grid(row=2, column=0, columnspan=4)

    query_pub.grid(row=3, column=0, columnspan=4)

    query_back.grid(row=4, column=0, columnspan=4)
    return


def queryreset():
    query_label.grid_forget()
    query_paper.grid_forget()
    query_author.grid_forget()
    query_pub.grid_forget()
    query_back.grid_forget()

    base_label.grid(row=0, column=3)
    data_entry_button.grid(row=1, column=0, columnspan=4)
    query_data_button.grid(row=2, column=0, columnspan=4)
    exit_button.grid(row=3, column=0, columnspan=4)
    return


def query_pap():
    query_label.grid_forget()
    query_paper.grid_forget()
    query_author.grid_forget()
    query_pub.grid_forget()
    query_back.grid_forget()
    query_title_flavor.grid(row=1, column=0)
    query_title.grid(row=2, column=0, columnspan=4)
    query_title_search.grid(row=3)
    return


def query_results():
    query_title_flavor.grid_forget()
    query_title.grid_forget()
    query_title_search.grid_forget()
    query_rs1.grid(row=0)
    # query_rs.grid(row=1)
    enter_back.grid(row=1)
    return


# Basic choices
base_label = Label(root, text="Welcome to the HCAA MongoDB Database. What would you like to do?")
base_label.grid(row=0, column=3)

data_entry_button = Button(root, text="Enter Data", command=enter_data)
data_entry_button.grid(row=1, column=0, columnspan=40)

query_data_button = Button(root, text="Query Data", command=query_data)
query_data_button.grid(row=2, column=0, columnspan=40)

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=5, column=0, columnspan=40)

enter_label = Label(root, text="Would you like to enter a paper, author, or publication?")
enter_paper = Button(root, text="Enter Paper", command=enter_paper)
enter_author = Button(root, text="Enter Author", command=enter_author)
enter_pub = Button(root, text="Enter Publication", command=enter_publication)
enter_back = Button(root, text="Go Back", command=insertreset)

query_label = Label(root, text="What query would you like to run?")
query_paper = Button(root, text="Get Paper by Title", command=query_pap)
query_author = Button(root, text="Get Papers by Author", command=query_pap)
query_pub = Button(root, text="Get Papers by Publication and Years", command=query_pap)
query_back = Button(root, text="Go Back", command=queryreset)

# Enter Paper buttons
no_authors = Label(root, text="One author must be present in the database to insert paper")
no_pubs = Label(root, text="One publication must be present in the database to insert paper")
input_title_flavor = Label(root, text="Insert Paper Title")
input_title = Entry(root, width=50, font=('Helvetica', 30))
dup_title = Label(root, text="Paper with this title already exists")
input_author_f_flavor = Label(root, text="Insert Author First Name")
input_author_f = Entry(root, width=50, font=('Helvetica', 30))
input_author_l_flavor = Label(root, text="Insert Author Last Name")
input_author_l = Entry(root, width=50, font=('Helvetica', 30))
input_pub_flavor = Label(root, text="Insert Publication Name:")
input_pub = Entry(root, width=50, font=('Helvetica', 30))
input_URL_flavor = Label(root, text="Insert URL (optional field):")
input_URL = Entry(root, width=50, font=('Helvetica', 30))
input_Pages_flavor = Label(root, text="Insert Pages (optional field):")
input_Pages = Entry(root, width=50, font=('Helvetica', 30))
input_paper_submit = Button(root, text="Submit", command=submitpaper)
input_successful = Label(root, text="Insert Successful!")

# Enter author buttons
input_author_f1_flavor = Label(root, text="Insert Author First Name")
input_author_f1 = Entry(root, width=50, font=('Helvetica', 30))
input_author_l1_flavor = Label(root, text="Insert Author Last Name")
input_author_l1 = Entry(root, width=50, font=('Helvetica', 30))
input_author_affil1_flavor = Label(root, text="Insert Author Affiliation Name")
input_author_affil1 = Entry(root, width=50, font=('Helvetica', 30))
input_author_affil2_flavor = Label(root, text="Insert Author Affiliation Start Date in YYYY-MM-DD format.")
input_author_affil2 = Entry(root, width=50, font=('Helvetica', 30))
input_author_affil3_flavor = Label(root, text="Insert Author Affiliation End Date in YYYY-MM-DD format.")
input_author_affil3 = Entry(root, width=50, font=('Helvetica', 30))
input_author_submit = Button(root, text="Submit", command=submitauthor)

# Enter publication buttons
pub_type = Label(root, text="Was this publication a conference or journal?")
input_pub_conference = Button(root, text="Conference", command=isjournal)
input_pub_journal = Button(root, text="Journal", command=isjournal)

# conference buttons
pub_name_flavor = Label(root, text="Name of Journal")
pub_name = Entry(root, width=50, font=('Helvetica', 30))
pub_year_flavor = Label(root, text="Year of Journal Publish")
pub_year = Entry(root, width=50, font=('Helvetica', 30))
pub_month_flavor = Label(root, text="Month of Journal Publish")
pub_month = Entry(root, width=50, font=('Helvetica', 30))
pub_edition_flavor = Label(root, text="Journal Edition (Optional)")
pub_edition = Entry(root, width=50, font=('Helvetica', 30))
input_pub_submit = Button(root, text="Submit", command=submitpub)

# query paper buttons
query_title_flavor = Label(root, text="Name of Publication Desired:")
query_title = Entry(root, width=50, font=('Helvetica', 30))
query_title_search = Button(root, text="Search", command=query_results)


# all query results
query_rs1 = Label(root, text="Steven Hill, Steven's Priliminary Findings, Dallas Morning News")
query_rs = Label(root, text="Steven Hill, Steven's Research, SMU Yearbook")
root.mainloop()