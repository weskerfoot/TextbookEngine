#! /usr/bin/python2

from urllib import quote
from json import loads, dumps

import requests as req

searchUrl = "https://archive.org/advancedsearch.php?q={0}&fl%5B%5D=avg_rating&fl%5B%5D=description&fl%5B%5D=identifier&fl%5B%5D=type&sort%5B%5D=&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes#raw"

def searchIA(title, author):
    """
    Do a search on The Internet Archive for a book
    """
    print "running a search"
    requrl = searchUrl.format(quote(title + " " + author))
    try:
        results = loads(req.get(requrl).text[9:][0:-1])
    except ValueError:
        return []

    rownum = results["responseHeader"]["params"]["rows"]
    if rownum < 1:
        print "Couldn't find results for %s %s" % (title, author)
        return []
    docs = results["response"]["docs"]
    urls = []
    for result in results["response"]["docs"][0:3]:
        urls.append("https://archive.org/details/%s" % result["identifier"])
    return urls


# Example, search for David Hume's Enquiry Concerning Human Understanding
#for url in searchIA("Hume", "Enquiry Concerning Human Understanding"):
    #print url
