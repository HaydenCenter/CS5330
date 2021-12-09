import pymongo
import datetime

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

system = System()

def runDataEntry():
    while True:
        print("What kind of document would you like to enter?")
        print("(1) Paper")
        print("(2) Author")
        print("(3) Publication (Journal or Conference)")
        print("(0) Go back")
        print()

        choice = input("Select your option: ")
        print()
        if choice not in ["0", "1", "2", "3"]:
            print("---- Invalid option ----")
            print()
            continue
        elif choice == "1":
            enterPaper()
        elif choice == "2":
            enterAuthor()
        elif choice == "3":
            enterPublication()
        else:
            break

    return

def enterPaper():
    collections = system.db.list_collection_names()

    if "Authors" not in collections:
        print("At least one author must exist before you can enter a paper")
        print()
        return
    
    if "Publications" not in collections:
        print("At least one publication must exist before you can enter a paper")
        print()
        return
    
    while True:
        title = input("Enter paper title: ")
        print()
        result = list(system.papers.find({"title": title}))

        if result:
            print(f"Paper with title \"{title}\" already exists")
            print()
            continue
        
        authors = selectAuthors()
        publication = selectPublication()

        url = input("Enter paper url (Optional): ")
        if url == "":
            url = None
        
        pages = input("Enter the number of pages (Optional): ")
        if pages == "":
            pages = None

        system.addPaper(title, authors, publication, url, pages)
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

        print(f"Select {n} author(s) from the list (You can only select an author once):")
        for i, a in enumerate(authors):
            name = a["first_name"] + " " + a["last_name"]
            print(f"({i}) {name}")
        print()

        for i in range(n):
            choice = input(f"Select author {i + 1}: ")
            print()

            while choice not in validOptions:
                print("---- Invalid option ----")
                print()
                choice = input(f"Select author {i + 1}: ")

            selections.append(choice)
            validOptions.remove(choice)
        break
    
    return [authors[int(i)]['_id'] for i in selections]

def selectPublication():
    publications = list(system.publications.find({}))
    validOptions = list(map(str, list(range(len(publications)))))
    # ^ This is gross again, sorry

    print(f"Select publication from the list:")
    for i, p in enumerate(publications):
        name = p["name"]
        print(f"({i}) {name}")
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

print("-----------------------------------------------")
print("-- Welcome to the CLI version of our project --")
print("- Developed by Hayden Center & Austin Abraham -")
print("-----------------------------------------------")
print()

while True:
    print("What would you like to do?")
    print("(1) Data entry")
    print("(2) Queries")
    print("(0) Quit")
    print()

    choice = input("Select your option: ")
    print()
    if choice not in ["0", "1", "2"]:
        print("---- Invalid option ----")
        print()
        continue
    elif choice == "1":
        runDataEntry()
    elif choice == "2":
        runQueries()
    else:
        print("Goodbye!")
        break

