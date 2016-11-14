#! /usr/bin/python3

from sys import argv
from itertools import chain, islice, zip_longest
from re import search, sub
from functools import total_ordering
from re import sub

import datetime as dt
import lxml.html as lxh
import requests

# Purpose of this module is to download and parse syllabi from various departments
# In order to be corellated with individual courses

class Price(object):
    def __init__(self, amnt, status):
        self.dollars = float(amnt[1:])
        self.status = status

    def __repr__(self):
        return "$%s %s" % (repr(self.dollars), self.status)


class Book(object):
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __repr__(self):
        return '["%s", "%s"]' % (self.title, repr(self.price))


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

searchUrl = "https://campusstore.mcmaster.ca/cgi-mcm/ws/txsub.pl?wsDEPTG1=%s&wsDEPTDESC1=&wsCOURSEG1=%s&crit_cnt=1"

def normalize(word):
    if len(word) > 1:
        return ("%s%s" %
                (word[0].upper(),
                "".join(word[1:]).lower()))
    return word

def parseAuthor(author):
    split = author.split(" ")
    if len(split) <= 1:
        return author
    lastname = split[0]
    firstname = split[1]
    return "%s %s" % (firstname, lastname)

def normwords(phrase):
    words = phrase.split(" ")
    return " ".join(map(normalize, words))

def books(dept, code, withPrices):
    """
    Snatch me up a book title or three
    """
    req = searchUrl % (dept, code)

    html = requests.get(req).text

    parsed = lxh.fromstring(html)

    pricelist = prices(parsed)

    for div in parsed.xpath(".//div"):
        if ("id" in div.attrib and
            "prodDesc" in div.attrib["id"]):

            textbook = div.text_content()
            author = sub(r',', '',
                           "".join(
                            (div.getparent()
                            .xpath(".//span[@class='inline']")
                            [0].text_content()
                            .split(":")[1:])).strip())
            price = pricelist.pop()
            if withPrices:
                yield (normwords(textbook), normwords(author), repr(price))
            else:
                yield (normwords(textbook), normwords(author))

def prices(html):
    """
    Get the prices from a search result page
    """
    ps = [
           p.getparent().text_content().split()[0]
             for p in html.xpath("//p/input[@type='checkbox']")
         ]

    try:
        amts, stats = zip(*list(reversed(list(grouper(2, ps)))))
        return map(Price, amts, stats)
    except ValueError:
        return []

def textbookInfo(dept, code, withPrices=False):
    """
    Return all the textbooks for a course
    """
    return list(books(dept, code, withPrices))

def humanities():
    """
    Download humanities syllabi
    """
    return []

# Example, getting the course info for Personality Theory (PSYCH = Department, 2B03 = Course code)
# print list(courseInfo("PSYCH", "2B03"))
