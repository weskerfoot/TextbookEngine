#! /usr/bin/env python2

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
    new_course = Course(sections=map(toSection, course.sections),
                        books=map(toBook, course.books),
                        title=course.title,
                        dept=course.dept,
                        code=course.code)
    new_course.save()


#if __name__ == "__main__":
    #Course.init()
