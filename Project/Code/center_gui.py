import pymongo
import datetime
from tkinter import *

class System:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://CenterAbraham:D3Jon69hcMCaEMxe@cluster0.bevht.mongodb.net/projectDatabase?retryWrites=true&w=majority")
        self.db = self.client["projectDatabase"]
        self.papers = self.db["Papers"]
        self.authors = self.db["Authors"]
        self.publications = self.db["Publications"]

    # authors should be an array of existing Author IDs, and publication should be a Publication ID
    def addPaper(self, title, authors, publication, url = None, pages = None):
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

    def addJournal(self, name, year, month, volume = None):
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

def raise_frame(frame, prev):
    if(prev):
        prev.grid_forget()
    frame.grid(row=0, column=0, sticky="")
    frame.grid_propagate(False)
    frame.tkraise()

def exit_frame(frame, prev):
    frame.destroy()
    raise_frame(prev, None)

system = System()

root = Tk()
root.geometry("400x600")
root.title("Final Project - Abraham/Center")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

def runDataEntry(prev):
    dataEntry = Frame(root)
    Label(dataEntry, text="What kind of document would you like to enter?", font=20).pack()
    Button(dataEntry, command=lambda: enterPaper(dataEntry), text="Paper", width=10).pack()
    # TODO: Data entry for Author
    # TODO: Data entry for Publication
    Button(dataEntry, text="Go Back", command=lambda: exit_frame(dataEntry, prev)).pack()

    raise_frame(dataEntry, prev)

def enterPaper(prev):
    collections = system.db.list_collection_names()
    allowed = True
    
    paperEntry = Frame(root)

    if "Authors" not in collections:
        allowed = False
        Label(paperEntry, text="At least one author must exist before you can enter a paper", font=20).pack()
    
    if "Publications" not in collections:
        allowed = False
        Label(paperEntry, text="At least one publication must exist before you can enter a paper", font=20).pack()

    if allowed:
        Label(paperEntry, text="Enter paper title:").pack()
        titleEntry = Entry(paperEntry, width=20)
        titleEntry.pack()

        Label(paperEntry, text="Select authors").pack()
        authorSelect = Listbox(paperEntry, exportselection=False, selectmode="multiple")
        authorsList = list(system.authors.find({}))
        for a in authorsList:
            authorSelect.insert(END, a["first_name"] + " " + a["last_name"])
        authorSelect.pack()

        Label(paperEntry, text="Select publication").pack()
        publicationSelect = Listbox(paperEntry, exportselection=False)
        publications = list(system.publications.find({}))
        for p in publications:
            publicationSelect.insert(END, p["name"])
        publicationSelect.pack()

        Label(paperEntry, text="Enter paper url:").pack()
        urlEntry = Entry(paperEntry, width=20)
        urlEntry.pack()
        
        Label(paperEntry, text="Enter paper pages:").pack()
        pagesEntry = Entry(paperEntry, width=20)
        pagesEntry.pack()

        errors = []

        def handleSubmit():
            nonlocal errors
            for e in errors:
                e.destroy()
            errors = []
            title = titleEntry.get()
            existing = list(system.papers.find({"title": title}))
            if(existing):
                errors.append(Label(paperEntry, fg="red", text=("Paper with title \"" + title + "\" already exists")))
                titleEntry.select_clear()
            
            authorSelections = authorSelect.curselection()
            if(not authorSelections):
                errors.append(Label(paperEntry, fg="red", text="No authors selected"))
                authorSelect.select_clear(0, END)

            publicationSelection = publicationSelect.curselection()
            if(not publicationSelection):
                errors.append(Label(paperEntry, fg="red", text="No publication selected"))
                publicationSelect.select_clear(0, END)

            if(not errors):
                nonlocal authorsList
                authors = []
                for authorSelected in authorSelections:
                    authors.append(authorsList[authorSelected]["_id"])

                publication = None
                for publicationSelected in publicationSelection:
                    publication = publications[publicationSelected]
                print(publication)

                url = urlEntry.get()
                if(url == ""):
                    url = None

                pages = pagesEntry.get()
                if(pagesEntry == ""):
                    pages = None

                system.addPaper(title, authors, publication, url, pages)
                exit_frame(paperEntry, prev)
            else:
                for e in errors:
                    e.pack()
        
        Button(paperEntry, text="Submit", command=handleSubmit).pack()
        Button(paperEntry, text="Go Back", command=lambda: exit_frame(paperEntry, prev)).pack()
    
    raise_frame(paperEntry, prev)

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
        print(f"Affilion {i + 1}")
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
                date_range = [s + datetime.timedelta(days = x) for x in range(0, (e-s).days)]
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

def runQueries():
    while True:
        print("What query would you like to run?")
        print("(1) Get paper information by title")
        print("(2) Get papers by author")
        print("(3) Get papers by publication and years")
        print("(0) Go back")
        print()

        choice = input("Select your option: ")
        print()
        if choice not in ["0", "1", "2", "3"]:
            print("---- Invalid option ----")
            print()
            continue
        elif choice == "1":
            byTitle()
        elif choice == "2":
            byAuthor()
        elif choice == "3":
            byPublication()
        else:
            print("Goodbye!")
            break
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

        print(f"Title: {title}")
        print(f"Publication: {publication}")
        print("Authors:")
        for id in authors:
            author = system.authors.find_one({'_id': id})
            name = author["first_name"] + " " + author["last_name"]
            print(f"  {name}")
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
        print(f"Papers for \"{first} {last}\"")
        for author in authors:
            papers = system.papers.find({'authors': author['_id']})
            for paper in papers:
                title = paper['title']
                print(f"  {title}")
        print()
            
    return

def byPublication():
    name = input("Publication name: ")
    start = int(input("Start year: "))
    end = int(input("End year: "))
    print()

    print(f"Papers for {name}:")
    for year in range(start, end + 1):
        publication = system.publications.find_one({'name': name, 'year': year})
        if publication:
            print(f"  {year}")
            papers = system.papers.find({'publication': publication['_id']})
            for paper in papers:
                title = paper['title']
                print(f"    {title}")
    print()
    return


home = Frame(root)
Label(home, text="What would you like to do?", font=20).pack()
Button(home, command=lambda: runDataEntry(home), text="Data Entry", width=10).pack()
# TODO Queries

raise_frame(home, None)

root.mainloop()

