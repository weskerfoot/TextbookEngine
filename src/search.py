#! /usr/bin/python2

import elasticsearch

from elasticsearch_dsl import FacetedSearch, Search, Q
from elasticsearch_dsl.aggs import Terms, DateHistogram
from sys import exit, stderr
from json import dumps, loads
from itertools import chain, imap

from hashlib import sha1

from textbookExceptions import UnIndexable

from mcmaster.classes import allCourses

# Generic instance of elasticsearch right now
es = elasticsearch.Elasticsearch()

def summarize(text):
    splitted = text.split(" ")
    if len(splitted) > 4:
        return " ".join(splitted[0:4]) + ".."
    return text

def sectionToJSON(section):
    return {
            "prof" : section.prof,
            "sem"  : section.sem,
            "day"  : section.day
            }

def classToJSON(clss):
    return {
            "title"    : clss.title,
            "sections" : map(sectionToJSON, clss.sections),
            "dept"     : clss.dept,
            "code"     : clss.code,
            "books"    : list(clss.books) if clss.books else []
            }


def truncate(docid):
    """
    Truncate a document id to 12 digits
    The document ID should be based on a
    hash of unique identifiers
    """
    return int(str(docid)[0:12])

def hashsec(course):
    """
    Hash a course into a usable id
    """
    if not course["code"]:
        code = ""
    else:
        code = course["code"]
    if not course["title"]:
        title = ""
    else:
        title = course["title"]

    if not course["sections"] or len(course["sections"]) < 1:
        course["sections"][0] = ""

    if not (code or title):
        raise UnIndexable(course)

    h = sha1()
    h.update(code + title + course["sections"][0]["sem"])
    return int(h.hexdigest(), 16)

def createIndex(name):
    """
    This creates a new index in elasticsearch
    An index is like a schema in a regular database
    Create an elasticsearch index

    """
    indices = elasticsearch.client.IndicesClient(es)

    print indices.create(name)
    with open("../course.json", "r") as mapping:
        print indices.put_mapping("course", loads(mapping.read()), name)

def indexListing(course):
    """
    Index a specific course in the database (using the courses index)
    example,
    {
     'books': [],
     'dept': 'COLLAB',
     'code': '2C03',
     'sections': [
                    {
                     'prof': 'Lisa Pender',
                     'sem': '2015/09/08 - 2015/12/08',
                     'day': 'Mo'
                     },
                     {
                      'prof': 'Staff',
                      'sem': '2015/09/08 - 2015/12/08',
                      'day': 'Th'
                      }
                  ],
     'title': 'COLLAB 2C03 - Sociology I'
     }

    """
    courseID = hashsec(course)
    print es.index(index="oersearch",
            doc_type="course",
            id=courseID,
            body=course)

    # For every course we index, we also create a resource for it
    # This should be an idempotent operation because we're putting it in couchdb
    # And we're using the id obtained from the hash function, so it should just update the document
    # no need to delete anything
    #try:
        #courseDept = course[0]["title"].strip().split(" ")[0].strip()
        #courseCode = course[0]["title"].strip().split(" ")[1].strip()
        #print "DEPARTMENT = \"%s\", COURSECODE = \"%s\"" % (courseDept, courseCode)
        #print createResource(textbookInfo, course[0], courseDept, courseCode, courseID)
    #except:
        #print "Couldn't create the resource associated with %s" % course

def termSearch(field):
    """
    Make a term search (exact match)
    """
    def t(term):
        q = Q("term",
                **{
                    "sections."+field : term
                    })
        return q
    return t

def search(field):
    """
    Make a match search
    """
    def s(term):
        q = Q("match",
                 **{
                     field : term
                    })
        return q
    return s

def join(x, y):
    """
    Join two queries
    """
    return x & y

def filterSections(secs):
    """
    Get rid of tutorial sections
    because they almost always have "Staff" as the instructor
    This is just a heuristic of course
    """
    filtered = [s for s in secs.sections if "Staff" not in s.prof]
    if len(filtered) > 0:
        return filtered
    return False

def searchTerms(terms):
    """
    Run a search for courses
    """

    # A list of all the queries we want to run
    qs = [searchers[field](term) for
            field, term in
            terms.iteritems() if
                term and searchers.has_key(field)]

    if not qs:
        # No queries = no results
        return dumps([])

    # Reduce joins all of the queries into one query
    # It will search for the conjunction of all of them
    # So that means it cares about each query equally
    q = reduce(join, qs)

    s = (Search(using=es, index="oersearch")
        .query(q))[0:100] # only return up to 100 results for now

    results = s.execute()

    filtered = [
                 (secs, filterSections(secs)[0].to_dict()) # get rid of tutorials
                  for secs in results
                    if filterSections(secs)
               ]
    results = []
    for obj, secs in filtered:
        # Add the truncated course id
        # This is used to point to the resource page for that course
        secs["id"] = truncate(obj.meta.id)
        secs["title"] = obj.title
        if obj["dept"] not in secs["title"]:
            secs["dept"] = obj.dept
        if obj.books:
            secs["books"] = [
                             {
                               "booktitle"  : summarize(book[0].encode("ASCII")),
                               "bookauthor" : book[1].encode("ASCII"),
                               "bookprice"  : book[2].encode("ASCII")
                             }
                                for book in obj.books
                            ]
        else:
            secs["books"] = ""
        results.append(secs)

    return dumps(results)


searchers = {
    "title" : search("title"),
    "loc"   : search("loc"),
    "time"  : search("time"),
    "prof"  : search("prof"),
    "day"   : search("day"),
    }

#print searchTerms({"title" : "PHILOS"})
#createIndex("oersearch")
#for c in imap(classToJSON, allCourses()):
    #try:
        #print indexListing(c)
    #except UnIndexable as e:
        ##print e
