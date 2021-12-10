import pymongo
import datetime
from tkinter import *
import re

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

        publication.update(other)
        return self.publications.insert_one(publication)

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
    Button(dataEntry, command=lambda: enterAuthor(dataEntry), text="Author", width=10).pack()
    Button(dataEntry, command=lambda: enterPublication(dataEntry), text="Publication", width=10).pack()
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
                titleEntry.delete(0, END)
            
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
                    publication = publications[publicationSelected]["_id"]

                url = urlEntry.get()
                if(url == ""):
                    url = None

                pages = pagesEntry.get()
                if(pages == ""):
                    pages = None

                system.addPaper(title, authors, publication, url, pages)
                exit_frame(paperEntry, prev)
            else:
                for e in errors:
                    e.pack()
        
        Button(paperEntry, text="Submit", command=handleSubmit).pack()
        Button(paperEntry, text="Go Back", command=lambda: exit_frame(paperEntry, prev)).pack()
    
    raise_frame(paperEntry, prev)

def enterAuthor(prev):
    authorEntry = Frame(root)
    
    Label(authorEntry, text="Enter first name:").pack()
    firstEntry = Entry(authorEntry, width=20)
    firstEntry.pack()

    Label(authorEntry, text="Enter last name:").pack()
    lastEntry = Entry(authorEntry, width=20)
    lastEntry.pack()

    affiliationWidgets = []
    errors = {}
    def handleSubmit():
        nonlocal errors
        for (k, e) in errors.items():
            e.destroy()
        errors = {}
        date_ranges = []
        for w in affiliationWidgets:
            startDate = w["startEntry"].get()
            if(not re.search("[1-2][0-9]{3}-((1[0-2])|(0[1-9]))-((0[1-9])|([1-2][0-9])|(3[0-1]))", startDate)):
                errors["invalid start"] = Label(authorEntry, fg="red", text="Invalid start date(s)")
                w["startEntry"].delete(0, END)

            endDate = w["endEntry"].get()
            if(not re.search("[1-2][0-9]{3}-((1[0-2])|(0[1-9]))-((0[1-9])|([1-2][0-9])|(3[0-1]))", endDate)):
                errors["invalid end"] = Label(authorEntry, fg="red", text="Invalid end date(s)")
                w["endEntry"].delete(0, END)

            if(not ("invalid start" in errors or "invalid end" in errors)):  
                s = datetime.datetime.strptime(startDate, "%Y-%m-%d")
                e = datetime.datetime.strptime(endDate, "%Y-%m-%d")

                for r in date_ranges:
                    if s in r or e in r:
                        errors["overlap"] = Label(authorEntry, fg="red", text="Conflicting date ranges")
                        break
                if not "overlap" in errors: 
                    date_range = [s + datetime.timedelta(days = x) for x in range(0, (e-s).days)]
                    date_ranges.append(date_range)
                else:
                    for w in affiliationWidgets:
                        w["startEntry"].delete(0, END)
                        w["endEntry"].delete(0, END)
        if(not errors):
            first = firstEntry.get()
            last = lastEntry.get()
            affiliations = []
            for w in affiliationWidgets:
                employer = w["nameEntry"].get()
                start = w["startEntry"].get()
                end = w["endEntry"].get()
                affiliations.append(system.createAffiliation(employer, start, end))
            system.addAuthor(first, last, affiliations)
            exit_frame(authorEntry, prev)
        else:
            for k, e in errors.items():
                e.pack()
    
    def addAffiliation():
        add.pack_forget()
        delete.pack_forget()
        submit.pack_forget()
        back.pack_forget()
        sep = Frame(authorEntry, bd=10, relief='sunken', height=4)
        label = Label(authorEntry, text=("Affiliation " + str(len(affiliationWidgets) + 1)))
        nameLabel = Label(authorEntry, text="Enter employer name:")
        nameEntry = Entry(authorEntry, width=20)
        startLabel = Label(authorEntry, text="Enter start date:")
        startEntry = Entry(authorEntry, width=20)
        endLabel = Label(authorEntry, text="Enter end date:")
        endEntry = Entry(authorEntry, width=20)
        sep.pack(side='top', fill='x', pady=10)
        label.pack(pady=0)
        nameLabel.pack()
        nameEntry.pack()
        startLabel.pack()
        startEntry.pack()
        endLabel.pack()
        endEntry.pack()
        add.pack()
        delete.pack()
        submit.pack()
        back.pack()

        affiliationWidgets.append({
            "sep": sep,
            "label": label,
            "nameLabel": nameLabel,
            "nameEntry": nameEntry,
            "startLabel": startLabel,
            "startEntry": startEntry,
            "endLabel": endLabel,
            "endEntry": endEntry
        })

    def deleteAffiliation():
        if(len(affiliationWidgets) > 1):
            for (k, v) in affiliationWidgets[-1].items():
                v.destroy()
            affiliationWidgets.pop(-1)

    add = Button(authorEntry, text="Add Affiliation", command=addAffiliation)
    delete = Button(authorEntry, text="Delete Affiliation", command=deleteAffiliation)
    submit = Button(authorEntry, text="Submit", command=handleSubmit)
    back = Button(authorEntry, text="Go Back", command=lambda: exit_frame(authorEntry, prev))

    addAffiliation()

    raise_frame(authorEntry, prev)

    return

def enterPublication(prev):
    publicationEntry = Frame(root)
    
    Label(publicationEntry, text="What is the publication type?").pack()
    Button(publicationEntry, command=lambda: enterJournal(publicationEntry), text="Journal", width=10).pack()
    Button(publicationEntry, command=lambda: enterConference(publicationEntry), text="Conference", width=10).pack()
    Button(publicationEntry, text="Go Back", command=lambda: exit_frame(publicationEntry, prev)).pack()

    raise_frame(publicationEntry, prev)

def enterJournal(prev):
    journalEntry = Frame(root)

    Label(journalEntry, text="Enter journal name:").pack()
    nameEntry = Entry(journalEntry, width=20)
    nameEntry.pack()
    
    Label(journalEntry, text="Enter journal year:").pack()
    yearEntry = Entry(journalEntry, width=20)
    yearEntry.pack()

    Label(journalEntry, text="Enter journal month:").pack()
    monthEntry = Entry(journalEntry, width=20)
    monthEntry.pack()

    Label(journalEntry, text="Enter journal volume:").pack()
    volumeEntry = Entry(journalEntry, width=20)
    volumeEntry.pack()

    errors = []

    def handleSubmit():
        nonlocal errors
        for e in errors:
            e.destroy()
        errors = []

        name = nameEntry.get()
        existing = list(system.publications.find({"name": name, "type": "Journal"}))
        if(existing):
            errors.append(Label(journalEntry, fg="red", text=("Journal with name \"" + name + "\" already exists")))
            nameEntry.delete(0, END)

        year = yearEntry.get()
        month = monthEntry.get()
        volume = volumeEntry.get()
        if(volume == ""):
            volume = None

        if(not errors):
            system.addJournal(name, year, month, volume)
            exit_frame(journalEntry, prev)
        else:
            for e in errors:
                e.pack()
        
    Button(journalEntry, text="Submit", command=handleSubmit).pack()
    Button(journalEntry, text="Go Back", command=lambda: exit_frame(journalEntry, prev)).pack()

    raise_frame(journalEntry, prev)

def enterConference(prev):
    conferenceEntry = Frame(root)

    Label(conferenceEntry, text="Enter conference name:").pack()
    nameEntry = Entry(conferenceEntry, width=20)
    nameEntry.pack()
    
    Label(conferenceEntry, text="Enter conference year:").pack()
    yearEntry = Entry(conferenceEntry, width=20)
    yearEntry.pack()

    Label(conferenceEntry, text="Enter number of times conference was held:").pack()
    timesHeldEntry = Entry(conferenceEntry, width=20)
    timesHeldEntry.pack()

    Label(conferenceEntry, text="Enter conference location:").pack()
    locationEntry = Entry(conferenceEntry, width=20)
    locationEntry.pack()

    errors = []

    def handleSubmit():
        nonlocal errors
        for e in errors:
            e.destroy()
        errors = []

        name = nameEntry.get()
        existing = list(system.publications.find({"name": name, "type": "Conference"}))
        if(existing):
            errors.append(Label(conferenceEntry, fg="red", text=("Conference with name \"" + name + "\" already exists")))
            nameEntry.delete(0, END)
        name = nameEntry.get()
        year = yearEntry.get()
        times_held = timesHeldEntry.get()
        location = locationEntry.get()

        if(not errors):
            system.addConference(name, year, times_held, location)
            exit_frame(conferenceEntry, prev)
        else:
            for e in errors:
                e.pack()

    Button(conferenceEntry, text="Submit", command=handleSubmit).pack()
    Button(conferenceEntry, text="Go Back", command=lambda: exit_frame(conferenceEntry, prev)).pack()

    raise_frame(conferenceEntry, prev)

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

