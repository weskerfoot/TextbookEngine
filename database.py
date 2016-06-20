#! /usr/bin/python2

from sys import argv
from hashlib import sha1

def truncate(docid):
    """
    Truncate a document id to 12 digits
    The document ID should be based on a
    hash of unique identifiers
    """
    return int(str(docid)[0:12])

def createResource(textbookInfo, course, dept, coursecode, docid):
    """
    Create a document associated with a course
    This document contains any/all resources associated
    with that course

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
    textbooks = textbookInfo(dept.strip(), coursecode.strip())

    # We truncate the id so we can have nicer looking URLs
    # Since the id will be used to point to the resource page for that course
    _id = str(truncate(docid))

    fields = {
            "_id" : _id,
            "textbooks" : textbooks,
            "coursetitle" : "%s %s" % (dept.strip(), coursecode.strip()),
            "courseinfo" : course
            #"Syllabus" : "blah"
            }
    try:
        revisions = list(localdb.revisions(_id))
        if not revisions:
            return localdb.save(fields)
        else:
            rev = dict(revisions[0])["_rev"]
            fields["_rev"] = rev
            return localdb.save(fields)
    except ResourceConflict:
        print "Resource for %s already exists, not creating a new one" % (docid)
