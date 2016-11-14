#! /usr/bin/python3

from json import loads, load
from re import sub, split
from itertools import groupby
from numpy import mean
from operator import attrgetter

import pygal
import csv

class Textbook(object):
    def __init__(self, dept, code, title, author, price):
        self.dept = dept
        self.code = code
        self.title = title
        self.author = author
        self.price = float(price)

    def __repr__(self):
        return "Dept = %s, Code = %s, %s by %s, costs $%s" % (self.dept,
                                                              self.code,
                                                              self.title,
                                                              self.author,
                                                              self.price)


def courses():
    with open("./books.csv", "r") as books:
        booksreader = csv.reader(books)
        for row in booksreader:
            yield row


def groupDept(courselist):
    sortedCourses = sorted(courselist, key=attrgetter("dept"))
    for course in groupby(sortedCourses, attrgetter("dept")):
        yield course[0], list(course[1])

def meanPrice(books):
    return mean([book.price for book in books])

# Questions,
# mean cost per department
# mean cost per faculty
# mean difference between book store copies and other copies per dept and faculty
# number of overlapping books per faculty, do eng students benefit from that?

# maybe a survey for students to see how often they buy books from other sources
# correlate with how much they could be saving?

facultyDesc = {
        "hum" : "Humanities",
        "bus" : "Business",
        "hlth" : "Health Science",
        "eng" : "Engineering",
        "sci" : "Science",
        "socsci" : "Social Sciences",
        "artsci" : "Arts & Sciences",
        "meld" : "MELD"
}

faculties = load(open("./faculties.json"))

def categorize(dept):
    # faculties
    return facultyDesc.get(faculties.get(dept, False), False)

def byFaculty():
    for dept, books in groupDept(courses()):
        yield (categorize(dept), dept, books)

def meanFacultyCosts():
    byfac = list(byFaculty())
    graph = pygal.Bar()
    graph.title = "Mean textbook cost by faculty"
    sortedFacs = sorted(byfac, key=lambda x: x[0])
    for fac in groupby(sortedFacs, lambda x: x[0]):
        graph.add(fac[0], meanPrice(list(fac[1])[0][2]))
    graph.value_formatter = lambda x: '$%.2f' % x if x is not None else "None"
    return graph.render(transpose=True)

def meanCosts():
    cs = groupDept(courses())
    graph = pygal.Bar()
    graph.title = "Mean textbook cost by department"
    for c in cs:
        dept, books = c
        graph.add(dept, meanPrice(books))
    #graph.render_to_file("./test_graph.svg")
    graph.value_formatter = lambda x: '$%.2f' % x if x is not None else "None"
    return graph.render_table(style=True, transpose=True)

for x in courses():
    print(x)
#print meanCosts()
#print meanFacultyCosts()
