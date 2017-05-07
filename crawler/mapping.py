#! /usr/bin/env python2

from hashlib import sha256
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Object

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

class TextBook(InnerObjectWrapper):
    pass

class Section(InnerObjectWrapper):
    pass

class Course(DocType):
    title = Text()
    dept = Text()
    code = Keyword()

    books = Object(
        doc_class=TextBook,
        properties = {
            "author" : Text(),
            "title" : Text(),
            "price" : Text()
        }
    )

    sections = Object(
            doc_class=Section,
            properties = {
                "sem" : Keyword(),
                "prof" : Text(),
                "loc" : Text(),
                "time" : Text(),
                "day" : Text()
                }
            )

    class Meta:
        index = "course_test"

def toSection(section):
    return {
             "sem" : section.sem,
             "prof" : section.prof,
             "loc" : section.loc,
             "time" : section.time,
             "day" : section.day
           }


def toBook(book):
    title, author, price = book
    return {
            "title"  : title,
            "author" : author,
            "price"  : price
            }

def indexCourse(course):
    print "Trying to index course %s" % course
    print course.books
    new_course = Course(sections=map(toSection, course.sections),
                        books=map(toBook, course.books if course.books else []),
                        title=course.title,
                        dept=course.dept,
                        code=course.code)

    if course.title and course.dept and course.code:
        _id = course.title+course.dept+course.code+course.sections[0].sem
    elif course.title and course.dept:
        _id = course.title+course.dept+course.sections[0].sem
    else:
        _id = course.title+course.sections[0].sem

    new_course.save(id=sha256(_id).hexdigest())


if __name__ == "__main__":
    Course.init()
