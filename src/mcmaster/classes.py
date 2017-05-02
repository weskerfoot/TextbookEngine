#! /usr/bin/python2

from sys import argv
from itertools import chain, islice
from re import search, sub
from functools import total_ordering

from sylla2 import textbookInfo
from collections import MutableMapping

import datetime as dt
import lxml.html as lxh
import requests
import logging
import sys
import copy

fall = "2169"
spring_summer = "2175"
winter = "2171"

# threading stuff
import Queue as q
import threading as thd

baseurl = "https://applicants.mcmaster.ca/psp/prepprd/EMPLOYEE/PSFT_LS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL"

searchurl = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/PSFT_LS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL"

custom_headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        }

courseCodes1 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH%240&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=5tq9x%2Fjt42mf62Sh5z%2BrjxT0gT15kiIyQ2cecCSmRB4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={1}"

courseCodes2 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=SSR_CLSRCH_WRK2_SSR_ALPHANUM_{1}&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=vIUgl6ZXw045S07EPbQw4RDzv7NmKCDdJFdT4CTRQNM%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={2}"

payload2 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=%23ICSave&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=aWx3w6lJ6d2wZui6hwRVSEnzsPgCA3afYJEFBLLkxe4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={1}"

payload = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=aWx3w6lJ6d2wZui6hwRVSEnzsPgCA3afYJEFBLLkxe4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&SSR_CLSRCH_WRK_SUBJECT$75$$0={1}&CLASS_SRCH_WRK2_STRM$45$={2}"


year = dt.date.today().year
month = dt.date.today().month

days = {
        "Mo" : 0,
        "Tu" : 1,
        "We" : 2,
        "Th" : 3,
        "Fr" : 4,
        "Sa" : 5,
        "Su" : 6
        }

day_descs = {
        "Mo" : "Monday Mon Mo",
        "Tu" : "Tuesday Tues Tu Tue",
        "We" : "Wednesday Wed We",
        "Th" : "Thursday Th Thurs",
        "Fr" : "Friday Fr Fri",
        "Sa" : "Saturday Sat Sa",
        "Su" : "Sunday Su Sun",
        "T"  : "TBA"
        }

def timeparse(time):
    """
    Parse the time into numbers
    """
    if len(time) == 7:
        hour = int(time[0:2])
        minutes = int(time[3:5])
        half = time[5:7]
    else:
        hour = int(time[0])
        minutes = int(time[2:4])
        half = time[4:6]
    if half == "PM":
        if hour < 12:
            hour = hour + 12

    return (str(hour), str(minutes), half)

class Class(object):
    def __init__(self, dept, title, sections):
        self.title = title.encode("UTF-8")
        self.sections = sections
        self.dept = dept

    def __repr__(self):
        return repr((self.title, self.sections))

    def __iter__(self):
        return iter((self.title, sec) for sec in self.sections)

    def hasCode(self):
        splitted = self.title.strip().split(" ")
        return ((len(splitted) >= 2) and
                (splitted[0].upper() == splitted[0]) and
                (splitted[1].upper() == splitted[1]))

    @property
    def code(self):
        if self.hasCode():
            return self.title.strip().split(" ")[1].strip()
        return False

    @property
    def books(self):
        if self.dept and self.code:
            print "tryna get some textbooks man"
            return textbookInfo(self.dept, self.code, withPrices=True)
        return False

@total_ordering
class Section(dict):
    def __init__(self, time, loc, prof, sem):
        self.time = time.encode("UTF-8")
        self.loc = loc.encode("UTF-8")
        self.prof = prof.encode("UTF-8")
        self._sem = sem.encode("UTF-8")
        self._date = False
        self._day = False

    @property
    def sem(self):
        if self._sem == fall:
            return "Fall"
        elif self._sem == winter:
            return "Winter"
        else:
            return "Spring/Summer"

    @property
    def date(self):
        if self.time != "TBA":
            day, start, _, end = self.time.split()

            if self._day:
                assert len(self._day) == 2
                day = self._day
            else:
                day = [day[n:n+2] for n in range(0, len(day)-1, 2)]

            self._date = (day, timeparse(start), timeparse(end))

            return self._date

        return self.time

    @property
    def day(self):
        return self.date[0]

    @property
    def start(self):
        return self.date[1][0] + self.date[1][1]

    def __repr__(self):
        return ("""
                Time = %s, Location = %s, Instructor = %s, Semester Running = %s
                 """ % (self.date, self.loc, self.prof, self.sem))
    def __gt__(self, x):
        if isinstance(self.day, list):
            raise NotImplementedError

        if (self.date == "TBA" or
            x.date == "TBA"):
            return False

        return ((days[self.day] > days[x.day]) or
                ((self.day == x.day) and
                 (self.start > x.start)))

    def __eq__(self, x):
        return (x.date == self.date and
                x.prof == self.prof and
                x.loc == self.loc and
                x.sem == self.sem)


def getStateNum(html):
    """
    Get the state num from Mosaic
    This is unique to each requester
    """
    parsed = lxh.fromstring(html)
    return parsed.xpath(".//input[@name=\"ICStateNum\"]")[0].value

def parseSection(section):
    cols = section.xpath(".//td")
    assert len(cols) == 4
    time, loc, prof, sem = [col.text_content().encode("UTF-8").strip() for col in cols]

    classinfo = Section(time, loc, prof, sem)
    return classinfo

def getSectionInfo(table):
    trs = table.xpath(".//tr")
    for tr in trs:
        if tr.xpath("@id") and search(r"SSR_CLSRCH", tr.xpath("@id")[0]):
            yield parseSection(tr)

def parseColumns(subject, html):
    print type(html)
    parsed = lxh.fromstring(html)

    classInfo = (list(getSectionInfo(table)) for table in
                  islice((table for table in parsed.xpath(".//table")
                    if table.xpath("@id") and
                    search(r"ICField[0-9]+\$scroll", table.xpath("@id")[0])), 1, sys.maxsize))

    classNames = ((subject, span.text_content().strip()) for span in parsed.xpath(".//span")
                    if span.xpath("@id") and
                       search(r"DERIVED_CLSRCH_DESCR", span.xpath("@id")[0]))

    return list(zip(classNames, classInfo))

def getCodes(html):
    parsed = lxh.fromstring(html)

    return (code.text_content().encode("UTF-8") for code in
                parsed.xpath("//span")
                if code.xpath("@id") and
                   search(r"SSR_CLSRCH_SUBJ_SUBJECT\$[0-9]+", code.xpath("@id")[0]))

class MosReq(object):
    def __init__(self, semester):
        self.semester = semester
        s = requests.Session()
        resp = s.get(baseurl, allow_redirects=True, headers=custom_headers).content

        # Let the server set some cookies before doing the searching
        cookies = {}
        for key, val in s.cookies.items():
            cookies[key] = val
        self.cookies = cookies
        self.statenum = False
        self.codes_ = []

    def getlist(self, subject):
        sys.stderr.write("Getting %s\n" % subject.decode("UTF-8"))
        first_req = requests.get(searchurl, cookies=self.cookies)
        # for some reason Mosaic wants us to request it twice, ??????????????????
        self.statenum = getStateNum(first_req.content)
        first_req = requests.post(searchurl,
                                  data=payload.format(self.statenum, subject, self.semester),
                                  cookies=self.cookies,
                                  allow_redirects=False,
                                  headers=custom_headers)

        # we make a first request to get the ICStateNum in case it thinks there are too many results
        try:
            self.statenum = getStateNum(first_req.content)
        except IndexError:
            pass
        if b"Your search will return over" in first_req:

            return requests.post(searchurl,
                                 data=payload2.format(self.statenum, self.semester),
                                 cookies=self.cookies,
                                 allow_redirects=False,
                                 headers=custom_headers).content
        else:
            return first_req.content

    def classes(self, subject):
        return list(parseColumns(subject, self.getlist(subject)))

    def getCodes(self, letter):
        sys.stderr.write("Getting letter " + letter + "\n")
        first_req = requests.get(searchurl, cookies=self.cookies).content
        self.statenum = getStateNum(first_req)

        self.statenum = getStateNum(requests.post(searchurl,
                                    data=courseCodes1.format(self.statenum, self.semester),
                                    cookies=self.cookies,
                                    headers=custom_headers).content)

        return getCodes(requests.post(searchurl,
                             data=courseCodes2.format(self.statenum, letter, self.semester),
                             cookies=self.cookies,
                             allow_redirects=False,
                             headers=custom_headers).content)
    @property
    def codes(self):
        if not self.codes_:
            self.codes_ = list(chain.from_iterable(
                                list(map((lambda l:
                                    self.getCodes(chr(l))),
                                    range(65, 91)))))
        return self.codes_

def request(codes, lists, semester):
    requester = MosReq(semester)
    while not codes.empty():
        code = codes.get()
        lists.put(requester.classes(code))
        codes.task_done()
        print "WHUT"
    print "DONE"

class CourseInfo(object):
    def __init__(self, threadcount, semester):
        self._codes = False
        self.threadcount = threadcount
        self.semester = semester

    @property
    def codes(self):
        if not self._codes:
            req = MosReq(self.semester)
            self._codes = req.codes
        return self._codes

    def classes(self):
        qcodes = q.Queue()
        for code in self.codes:
            qcodes.put(code)
        lists = q.Queue()
        threads = []
        thread = None
        for i in range(self.threadcount):
            thread = thd.Thread(group=None, target=request, args=(qcodes, lists, self.semester))
            threads.append(thread)
            thread.start()
        qcodes.join()
        for t in threads:
            print t
            t.join()

        print "finished getting courses"

        sections = []
        while not lists.empty():
            sections.append(lists.get())

        for cl in chain.from_iterable(sections):
            new_sections = []
            for sec in cl[1]:
                if len(sec.day) > 1:
                    for day in sec.day:
                        new_sections.append(copy.deepcopy(sec))
                        new_sections[-1]._day = day
                else:
                    sec._day = sec.day[0]
                    new_sections.append(sec)
            yield Class(cl[0][0], sub("\xa0+", "", cl[0][1]), sorted(new_sections))

def getCourses(semester, threadcount=10):
    return CourseInfo(threadcount, semester).classes()

def allCourses():
    return chain.from_iterable(
     (getCourses(sem, threadcount=25)
        for sem in (fall, winter, spring_summer)))

if __name__ == "__main__":
    for course in allCourses():
        sys.stdout.write("%s, %s, %s, %s\n" % (course.title, course.code, course.dept, list(chain.from_iterable(course.books) if course.books else [])))
