from db.db_handler import db
from db.models import Paper
from sqlalchemy.sql.expression import func
from tools import cache_load, cache_save
import csv

class MockPaper():
    def __init__(self, obj):
        self.id = obj.id
        self.title = obj.title
        self.DOI = obj.DOI
        self.text = obj.text
        self.clean_text = obj.clean_text
        self.year = obj.year

        self.authors = [MockPaperAuthor(o) for o in obj.paper_authors]


class MockPaperAuthor():
    def __init__(self, obj):
        self.id = obj.id
        self.rank = obj.rank

        if obj.author:
            self.name = obj.author.name
            self.affiliation = obj.author.affiliation
        else:
            self.name = None
            self.affiliation = None


def get_citations():
    res = {}
    with open('etc/citations.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        linecount = -1
        for row in csv_reader:
            # header
            linecount += 1
            if linecount == 0:
                continue
            
            # DOI;Title;Year;Timestamp;ScholarID;ScholarURL;Citations
            doi = row[0]
            citations = row[-1]

            res[doi.lower()] = int(citations)

    return res


def get_interactions():
    res = {}
    with open('etc/interactions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        linecount = -1
        for row in csv_reader:
            # header
            linecount += 1
            if linecount == 0:
                continue
            
            # word, occ, #papers, category, appeared_first
            res[row[0].lower()] = row

    return res



def get_proceedings(min_year=1981, max_year=2018):
    ''' we need to fetch the data one
        year at a time, otherwise
        mysql will not work (too much data)
    '''
    data = []
    for i in range(min_year, max_year + 1):
        try:
            my_year = cache_load("proceedings_"+str(i))
        except:
            continue
        data.extend(my_year)

    return data


def get_paper(id):
    p = db.query(Paper).filter(Paper.id == id).one()
    return MockPaper(p)


def get_paper_title(title):
    p = db.query(Paper).filter(Paper.title.like("%"+title+"%")).all()[0]

    return MockPaper(p)
