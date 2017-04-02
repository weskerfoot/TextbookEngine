from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Object

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=["localhost"])

class TextBook(InnerObjectWrapper):
    pass

class Section(InnerObjectWrapper):
    pass

class Course(DocType):
    textbook = Object(
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
                "title" : Text(),
                "prof" : Text(),
                "loc" : Text(),
                "time" : Text(),
                "day" : Text()
                }
            )

    class Meta:
        index = "course_test"
