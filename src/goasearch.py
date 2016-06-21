#! /usr/bin/python2
from search import indexListing
from textbookExceptions import UnIndexable
from mcmaster.classes import allCourses, classToJSON, indexListing
from itertools import imap

try:
    print "Trying to create the index if it does not exist already"
    createIndex("oersearch")
except Exception as e:
    print e

print "Downloading course info"
for c in imap(classToJSON, allCourses()):
    try:
        print indexListing(c)
    except UnIndexable as e:
        print e
