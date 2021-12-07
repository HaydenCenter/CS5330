import pymongo
import datetime
from tkinter import *
from PIL import ImageTk, Image


class System:
    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://CenterAbraham:D3Jon69hcMCaEMxe@cluster0.bevht.mongodb.net/projectDatabase?retryWrites=true&w=majority")
        self.db = self.client["projectDatabase"]
        self.papers = self.db["Papers"]
        self.authors = self.db["Authors"]
        self.publications = self.db["Publications"]

    # authors should be an array of existing Author IDs, and publication should be a Publication ID
    def addPaper(self, title, authors, publication, url=None, pages=None):
        paper = {
            "title": title,
            "authors": authors,
            "publication": publication
        }

        if url:
            paper["url"] = url
        if pages:
            paper["pages"] = pages

        return self.papers.insert_one(paper)

    # dates should be formatted as YYYY-MM-DD, e.g. 2006-05-15 for May 15th, 2006
    def createAffiliation(self, employer, start_date, end_date):
        return {
            "employer": employer,
            "start_date": start_date,
            "end_date": end_date
        }

    # affiliations should be an array of affiliation documents
    def addAuthor(self, first, last, affiliations):
        author = {
            "first_name": first,
            "last_name": last,
            "affiliations": affiliations
        }

        return self.authors.insert_one(author)

    def __addPublication(self, name, year, type, other):
        publication = {
            "name": name,
            "year": year,
            "type": type
        }

        return self.publications.insert_one(publication.update(other))

    def addJournal(self, name, year, month, volume=None):
        other = {
            "month": month
        }

        if volume:
            other["volume"] = volume

        return self.__addPublication(name, year, "Journal", other)

    def addConference(self, name, year, times_held, location):
        other = {
            "times_held": times_held,
            "location": location
        }

        return self.__addPublication(name, year, "Conference", other)


system = System()


# ALL BELOW THIS LINE ARE THE NON DATABASE INFO FUNCTIONS
def enterPaper():
    #collections = system.db.list_collection_names()

   # if "Authors" not in collections:
   #     no_authors.grid(row=6, column=3)
   #     return
#
 #   if "Publications" not in collections:
  #      no_pubs.grid(row=6, column=3)
   #     return

        input_title.grid(row=0, column=3)
        result = list(system.papers.find({"title": input_title.get()}))

        if result:
            dup_title.grid(row=0, column=3)


        authors = selectAuthors()
        publication = selectPublication()

        input_URL.grid(row=1,column=3)
        if input_URL.get() == "":
            url = None

        input_Pages.grid(row=1,column=3)
        if input_Pages.get() == "":
            pages = None

        system.addPaper(input_title.get(), authors, publication, input_URL.get(), input_Pages.get())
        return


def selectAuthors():
    authors = list(system.authors.find({}))
    selections = []
    validOptions = list(map(str, list(range(len(authors)))))
    # ^ This is gross, I know. It generates a list of strings from 0 to the max index of authors. This was the simplest way to do it. Sorry.

    while True:
        n = int(input("How many authors does the paper have? "))
        print()
        if n > len(authors):
            print("Not enough authors exist")
            print()
            continue

        print("Select {n} author(s) from the list (You can only select an author once):")
        for i, a in enumerate(authors):
            name = a["first_name"] + " " + a["last_name"]
            print("({i}) {name}")
        print()

        for i in range(n):
            choice = input("Select author {i + 1}: ")
            print()

            while choice not in validOptions:
                print("---- Invalid option ----")
                print()
                choice = input("Select author {i + 1}: ")

            selections.append(choice)
            validOptions.remove(choice)
        break

    return [authors[int(i)]['_id'] for i in selections]


def selectPublication():
    publications = list(system.publications.find({}))
    validOptions = list(map(str, list(range(len(publications)))))
    # ^ This is gross again, sorry

    print("Select publication from the list:")
    for i, p in enumerate(publications):
        name = p["name"]
        print("({i}) {name}")
    print()

    choice = input("Select publication: ")
    print()

    while choice not in validOptions:
        print("---- Invalid option ----")
        print()
        choice = input("Select publication: ")

    return publications[int(choice)]['_id']


def enterAuthor():
    first = input("Enter author first name: ")
    last = input("Enter author last name: ")
    affiliations = createAffiliations()

    system.addAuthor(first, last, affiliations)
    return


def createAffiliations():
    n = int(input("How many affiliations does the author have? "))
    print()
    affiliations = []
    date_ranges = []
    for i in range(n):
        print("Affiliation {i + 1}")
        employer = input("Enter employer name: ")
        valid = False
        while not valid:
            valid = True
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            s = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            e = datetime.datetime.strptime(end_date, "%Y-%m-%d")

            for r in date_ranges:
                if s in r or e in r:
                    print("Invalid date range")
                    valid = False
                    break
            if valid:
                date_range = [s + datetime.timedelta(days=x) for x in range(0, (e - s).days)]
                date_ranges.append(date_range)

        affiliations.append({
            "employer": employer,
            "start_date": start_date,
            "end_date": end_date
        })

        print()

    return affiliations


def enterPublication():
    name = input("Enter publication name: ")
    year = int(input("Enter publication year: "))
    type = ""
    while True:
        print("What is the publication type?")
        print("(0) Journal")
        print("(1) Conference")
        print()
        type = input("Select your option: ")
        if type not in ["0", "1"]:
            print("---- Invalid option ----")
            print()

        break

    if type == 0:
        month = input("Enter the journal month: ")
        volume = input("Enter the journal volume (Optional): ")

        if volume == "":
            volume = None

        system.addJournal(name, year, month, volume)
    else:
        times_held = input("Enter the number of times the conference has been held: ")
        location = input("Enter the location of the conference")

        system.addConference(name, year, times_held, location)

    return


def byTitle():
    title = input("Title: ")
    print()

    paper = system.papers.find_one({"title": title})

    if not paper:
        print("Paper not found")
        print()
    else:
        title = paper["title"]
        authors = paper["authors"]
        publication = paper["publication"]
        publication = system.publications.find_one({'_id': publication})['name']

        print("Title: {title}")
        print("Publication: {publication}")
        print("Authors:")
        for id in authors:
            author = system.authors.find_one({'_id': id})
            name = author["first_name"] + " " + author["last_name"]
            print("  {name}")
        print()
    return


def byAuthor():
    first = input("Author first name: ")
    last = input("Author last name: ")
    print()

    authors = system.authors.find({'first_name': first, 'last_name': last})
    if not authors:
        print("Author not found")
        print()
    else:
        print("Papers for \"{first} {last}\"")
        for author in authors:
            papers = system.papers.find({'authors': author['_id']})
            for paper in papers:
                title = paper['title']
                print("  {title}")
        print()

    return


def byPublication():
    name = input("Publication name: ")
    start = int(input("Start year: "))
    end = int(input("End year: "))
    print()

    print("Papers for {name}:")
    for year in range(start, end + 1):
        publication = system.publications.find_one({'name': name, 'year': year})
        if publication:
            print("  {year}")
            papers = system.papers.find({'publication': publication['_id']})
            for paper in papers:
                title = paper['title']
                print("    {title}")
    print()
    return


root = Tk()
root.title('File Management GUI')
root.geometry("400x400")


# Displays buttons for insert data
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


# Resets after you press back from insert data
def insertreset():
    enter_label.grid_forget()
    enter_paper.grid_forget()
    enter_author.grid_forget()
    enter_pub.grid_forget()
    enter_back.grid_forget()

    base_label.grid(row=0, column=3)
    data_entry_button.grid(row=1, column=0, columnspan=4)
    query_data_button.grid(row=2, column=0, columnspan=4)
    exit_button.grid(row=3, column=0, columnspan=4)
    return


# Displays buttons for query
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


# Resets after you press back from query
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


# Initial Setup Buttons
base_label = Label(root, text="What would you like to do?")
base_label.grid(row=0, column=3)

data_entry_button = Button(root, text="Enter Data", command=enter_data)
data_entry_button.grid(row=1, column=0, columnspan=4)

query_data_button = Button(root, text="Query Data", command=query_data)
query_data_button.grid(row=2, column=0, columnspan=4)

exit_button = Button(root, text="Exit", command=root.destroy)
exit_button.grid(row=5, column=0, columnspan=4)

# Enter data buttons
enter_label = Label(root, text="Would you like to enter a paper, author, or publication?")
enter_paper = Button(root, text="Enter Paper", command=enterPaper)
enter_author = Button(root, text="Enter Author", command=enterAuthor)
enter_pub = Button(root, text="Enter Publication", command=enterPublication)
enter_back = Button(root, text="Go Back", command=insertreset)

# Enter Query buttons
query_label = Label(root, text="What query would you like to run?")
query_paper = Button(root, text="Get Paper by Title", command=byTitle)
query_author = Button(root, text="Get Papers by Author", command=byAuthor)
query_pub = Button(root, text="Get Papers by Publication and Years", command=byPublication)
query_back = Button(root, text="Go Back", command=queryreset)

# Enter Paper buttons
no_authors = Label(root, text="One author must be present in the database to insert paper")
no_pubs = Label(root, text="One publication must be present in the database to insert paper")
input_title = Entry(root, width=50, font=('Helvetica', 30))
dup_title = Label(root, text="Paper with this title already exists")
input_URL = Entry(root, width=50, font=('Helvetica', 30))
input_Pages = Entry(root, width=50, font=('Helvetica', 30))

root.mainloop()
