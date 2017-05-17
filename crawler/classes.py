#! /usr/bin/env python2

from mapping import indexCourse
from sys import argv
from itertools import chain, islice
from re import search, sub
from functools import total_ordering

from books import textbookInfo

import datetime as dt
import lxml.html as lxh
import requests
import logging
import sys
import copy

# threading imports
import Queue as q
import threading as thd

# Codes for semesters
# The first three digits of the year, followed by the month the semester starts
fall = "2179"
spring_summer = "2175"
winter = "2181"

baseurl = "https://applicants.mcmaster.ca/psp/prepprd/EMPLOYEE/PSFT_LS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL"

searchurl = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/PSFT_LS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL"

custom_headers = {
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        }

# format strings to build GET requests, taken from an actual browser session
courseCodes1 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=CLASS_SRCH_WRK2_SSR_PB_SUBJ_SRCH%240&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=5tq9x%2Fjt42mf62Sh5z%2BrjxT0gT15kiIyQ2cecCSmRB4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={1}"

courseCodes2 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=SSR_CLSRCH_WRK2_SSR_ALPHANUM_{1}&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=vIUgl6ZXw045S07EPbQw4RDzv7NmKCDdJFdT4CTRQNM%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={2}"

payload2 = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=%23ICSave&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=aWx3w6lJ6d2wZui6hwRVSEnzsPgCA3afYJEFBLLkxe4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&CLASS_SRCH_WRK2_STRM$45$={1}"

payload = "ICAJAX=1&ICNAVTYPEDROPDOWN=1&ICType=Panel&ICElementNum=0&ICStateNum={0}&ICAction=CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH&ICXPos=0&ICYPos=0&ResponsetoDiffFrame=-1&TargetFrameName=None&FacetPath=None&ICFocus=&ICSaveWarningFilter=0&ICChanged=-1&ICResubmit=0&ICSID=aWx3w6lJ6d2wZui6hwRVSEnzsPgCA3afYJEFBLLkxe4%3D&ICActionPrompt=false&ICFind=&ICAddCount=&ICAPPCLSDATA=&SSR_CLSRCH_WRK_SUBJECT$75$$0={1}&CLASS_SRCH_WRK2_STRM$45$={2}"

days = {
        "Mo" : 0,
        "Tu" : 1,
        "We" : 2,
        "Th" : 3,
        "Fr" : 4,
        "Sa" : 5,
        "Su" : 6
        }

def parse_semester(sem):
    """
    Take a semester and try to parse it into the numeral format
    """
    try:
        splitted = sem.split("/")
        year = splitted[0]
        month = splitted[1]
        return "%s%s%s" % (year[0], year[2:4], month[1])
    except IndexError:
        return sem

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

    @property
    def code(self):
        """
        Heuristic for checking if a course has a code associated with it
        Checks if it has more than two words and if they start with uppercase letters
        """
        splitted = self.title.strip().split(" ")
        if ((len(splitted) >= 2) and
            (splitted[0].upper() == splitted[0]) and
            (splitted[1].upper() == splitted[1])):
            return splitted

        return False

    @property
    def books(self):
        """
        Get textbooks for the course
        """
        if self.dept and self.code:
            return textbookInfo(self.dept, self.code, withPrices=True)
        return False

@total_ordering
class Section(dict):
    """
    This represents a section of a course
    """
    def __init__(self, time, loc, prof, sem):
        self.time = time

        # Location of the course (building)
        self.loc = loc

        self.prof = prof
        self._sem = sem
        self._date = False
        self._day = False

    @property
    def sem(self):
        """
        Return the semester the course runs
        """
        parsed = parse_semester(self._sem)
        if parsed == fall:
            return "Fall"
        elif parsed == winter:
            return "Winter"
        else:
            return "Spring/Summer"

    @property
    def date(self):
        """
        Return the day(s) of the week the section runs and the start and end times
        """
        if self.time != "TBA":
            day, start, _, end = self.time.split()

            # Assuming that each day is two characters, create a list of them
            day = [day[n:n+2] for n in range(0, len(day)-1, 2)]

            self._date = (day, timeparse(start), timeparse(end))

            return self._date
        return self.time

    @property
    def day(self):
        """
        Return just the day(s) the section runs
        """

        # This is set when the section is duplicated (then it would have a single day)
        if self._day:
            return self._day

        # Otherwise return the list of days from the date property
        if self.date != "TBA":
            return self.date[0]
        return "TBA"

    @property
    def start(self):
        """
        Return the starting time of this section
        """
        if self.date != "TBA":
            return self.date[1][0] + self.date[1][1]
        return "TBA"

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
    """
    Extract section information from the parsed course table
    """
    trs = table.xpath(".//tr")
    for tr in trs:
        if tr.xpath("@id") and search(r"SSR_CLSRCH", tr.xpath("@id")[0]):
            yield parseSection(tr)

def parseColumns(subject, html):
    """
    Extract class columns
    """
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
    """
    Get department course codes
    """
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
        """
        Gets a list of all course codes available
        """
        if not self.codes_:
            self.codes_ = list(
                            chain.from_iterable(
                                self.getCodes(chr(l)) for l in range(65, 91)))
        return self.codes_

def request(codes, lists, semester):
    requester = MosReq(semester)
    while not codes.empty():
        code = codes.get()
        lists.put(requester.classes(code))
        codes.task_done()

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
        """
        Returns a generator of all courses and textbooks
        """

        # Queue of letters to process
        course_codes = q.Queue()

        # Initialize the queue with all codes
        for code in self.codes:
            course_codes.put(code)

        lists = q.Queue()
        threads = []
        thread = None

        # Spawn threads that pull from the queue of course codes
        for i in range(self.threadcount):
            thread = thd.Thread(group=None, target=request, args=(course_codes, lists, self.semester))
            threads.append(thread)
            thread.start()

        # Block until all queue tasks are done
        course_codes.join()

        # Block until all threads have exited
        for t in threads:
            t.join()

        sections = []

        # Empty the queue of sections and put it into the list
        while not lists.empty():
            sections.append(lists.get())

        # This creates a section for each day, so that each section has only one day
        for cl in chain.from_iterable(sections):
            new_sections = []
            for sec in cl[1]:
                # sec.day is a list of days
                # if there is more than one day, we want to split this up into multiple sections
                if len(sec.day) > 1:
                    for day in sec.day:
                        new_sections.append(copy.deepcopy(sec))
                        new_sections[-1]._day = day
                else:
                    sec._day = sec.day[0]
                    new_sections.append(sec)

            # cl[0][0] is the subject code/department scraped from the page
            # cl[0][1] is the subject name scraped from the page
            # regex substitution is to get rid of erroneous characters (due to an encoding problem with the page)

            yield Class(cl[0][0], sub("\xa0+", "", cl[0][1]), sorted(new_sections))

def getCourses(semester, threadcount=10):
    """
    Gets all the courses for a given semester
    """
    return CourseInfo(threadcount, semester).classes()

def allCourses():
    """
    Gets all the courses for all three semesters
    """
    courses = map(getCourses, [spring_summer, fall, winter])
    return chain.from_iterable(courses)

if __name__ == "__main__":
    for course in allCourses():
        print course
        #indexCourse(course)
