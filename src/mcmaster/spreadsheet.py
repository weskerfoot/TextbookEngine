#! /usr/bin/python2

from classes import fallCourses
import csv

def getCourses():
    for course in fallCourses():
        for (_, section) in course:
            try:
                day, start, end = section.date
            except:
                continue
            if section.prof != "Staff":
                try:
                    startTime = "%s:%s %s" % (start[0], start[1], start[2])
                    endTime = "%s:%s %s" % (end[0], end[1], end[2])
                    yield (course.title, course.dept, course.code, day, startTime, endTime, section.loc, section.prof)
                except:
                    continue

with open("./courses.csv", "wb") as coursefile:
    writer = csv.writer(coursefile)
    writer.writerows(getCourses())
