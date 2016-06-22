#! /usr/bin/python2
from functools import partial

from flask import Blueprint, abort, Flask, render_template, flash, request, send_from_directory
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig

from urllib import unquote
from search import searchTerms

from openlibrary import bookUrls

from archive import searchIA
from urllib import quote, unquote
from json import dumps, loads

from werkzeug.contrib.cache import MemcachedCache
cache = MemcachedCache(['127.0.0.1:11211'])

import os

def predict(fieldtype, term):
    print fieldtype
    print term
    if not term:
        return "[]"
    else:
        try:
            cs = completers[fieldtype](term.lower())
        except KeyError:
            return "[]"
    if cs:
        return cs
    return "[]"

def predictor(fieldtype):
    def inner(request):
        params = dict(request.args.items())
        return predict(fieldtype, params["term"])
    return inner

def cacheit(key, thunk):
    """
    Tries to find a cached version of ``key''
    If there is no cached version then it will
    evaluate thunk (which must be a generator)
    and cache that, then return the result
    """
    cached = cache.get(quote(key))
    if cached is None:
        result = list(thunk())
        cache.set(quote(key), result)
        return result
    return cached

def ClassSearch(configfile=None):
    defaults = {"Day", "Building", "Exact Location", "Department"}
    blueprint = Blueprint("website", __name__, template_folder="templates")
    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/search")
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    app.config["scripts"] = "./scripts"
    app.config["styles"] = "./styles"

    @blueprint.route('/favicon.ico')
    def favicon():
        return send_from_directory("/srv/http/goal/favicon.ico",
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')


    @blueprint.route("/buildpred", methods=("GET", "POST"))
    def buildpred():
        return predictbuild(request)

    @blueprint.route("/locpred", methods=("GET", "POST"))
    def locpred():
        return predictloc(request)

    @blueprint.route("/daypred", methods=("GET", "POST"))
    def daypred():
        return predictday(request)

    @blueprint.route("/deptpred", methods=("GET", "POST"))
    def deptpred():
        return predictdept(request)

    @blueprint.route("/titlepred", methods=("GET", "POST"))
    def titlepred():
        return predicttitle(request)

    @blueprint.route("/", methods=("GET", "POST"))
    def index():
        return render_template("search.html")

    @blueprint.route("/fc", methods=("GET", "POST"))
    def fc():
        """ Filter Courses """
        print "trying to get courses"
        params = dict(request.args.items())
        for key, val in params.iteritems():
            if val in defaults:
                del params[key]
        results = searchTerms(params)
        return results

    @blueprint.route("/resources", methods=("GET", "POST"))
    def resources():
        """ Get Resources """
        notRequired = False
        params = loads(dict(request.args.items())["data"])
        print params
        author = params["author"]
        title = params["title"]

        if ("No Textbooks" in title or
            "No Adoption" in title):
            return dumps("false")

        # Cache the result of the open library search
        openlib = cacheit("openlib"+title+author, lambda : bookUrls(title, author))
        print openlib

        # cache the result of an internet archive search
        iarchive = cacheit("iarchive"+title+author, lambda : searchIA(title, author))
        print iarchive

        if not (any(openlib) or any(iarchive)):
            # We literally could not find ANYTHING
            return dumps("false")
            
        return dumps({
                       "iarchive" : iarchive,
                       "openlib" : openlib
                     })

    @blueprint.route("/scripts/<filename>")
    def send_script(filename):
        return send_from_directory(app.config["scripts"], filename)

    @blueprint.route("/styles/<filename>")
    def send_style(filename):
        return send_from_directory(app.config["styles"], filename)
    return app

if __name__ == "__main__":
    ClassSearch("./appconfig").run(port=8001, debug=True)
