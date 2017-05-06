from oersearch import Search
from classes import getCourses
from sylla import getTextbooks

mcmasterSearch = Search("McMaster")

mcmasterSearch.setup(getCourses)

mcmasterSearch.run()
