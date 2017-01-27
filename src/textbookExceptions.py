#! /usr/bin/python3

class UnIndexable(Exception):
    def __init__(self, course):
        self.course = course

    @property
    def reason(self):
        course = self.course
        if not course["code"] and not course["title"]:
            message = "there was no course code and no title defined"
        if not course["code"]:
            message = "there was no course code defined"
        if not course["title"]:
            message = "there was no course title defined"
        if not course["sections"]:
            message = "there were no sections defined"
        return """
        There was a problem with indexing this course.
        %s
        There could be several reasons why, my best guess is that %s
        We need at least the course code, title, and one or more sections to index
        """ % (course, message)
