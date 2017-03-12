#! /usr/bin/python3
from functools import partial
from urllib.parse import quote, unquote
from json import loads

from flask import Blueprint, Flask, render_template, request, send_from_directory, jsonify
from flask_bootstrap import Bootstrap
from werkzeug.contrib.cache import MemcachedCache

from search import search_courses
from openlibrary import bookUrls
from archive import searchIA

cache = MemcachedCache(['127.0.0.1:11211'])

def predict(fieldtype, term):
    if not term:
        return jsonify([])
    else:
        try:
            cs = completers[fieldtype](term.lower())
        except KeyError:
            return jsonify([])
    if cs:
        return cs
    return jsonify([])

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
    blueprint = Blueprint("TextBookSearch", __name__, template_folder="templates")

    @blueprint.route('/favicon.ico')
    def favicon():
        return send_from_directory("/srv/http/goal/favicon.ico",
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @blueprint.route("/", methods=("GET", "POST"))
    def index():
        return render_template("search.html")

    @blueprint.route("/fc", methods=("GET", "POST"))
    def fc():
        """ Filter Courses """
        print("trying to get courses")
        params = dict(request.args.items())
        for key, val in params.items():
            if val in defaults:
                del params[key]
        return jsonify(search_courses(params))

    @blueprint.route("/resources", methods=("GET", "POST"))
    def resources():
        """ Get Resources """
        notRequired = False
        params = request.json
        if params is None:
            return jsonify(False)
        author = params["author"]
        title = params["title"]

        if ("No Textbooks" in title or
            "No Adoption" in title):
            return jsonify(False)

        # Cache the result of the open library search
        openlib = cacheit("openlib"+title+author, lambda : bookUrls(title, author))

        # cache the result of an internet archive search
        iarchive = cacheit("iarchive"+title+author, lambda : searchIA(title, author))

        if not (any(openlib) or any(iarchive)):
            # We literally could not find ANYTHING
            return jsonify(False)

        return jsonify({
                       "iarchive" : iarchive,
                       "openlib" : openlib
                     })

    #@blueprint.route("/scripts/<filename>")
    #def send_script(filename):
        #return send_from_directory(app.config["scripts"], filename)

    #@blueprint.route("/styles/<filename>")
    #def send_style(filename):
        #return send_from_directory(app.config["styles"], filename)

    app = Flask(__name__)
    app.register_blueprint(blueprint, url_prefix="/search")
    #app.config["scripts"] = "./scripts"
    #app.config["styles"] = "./styles"
    return app

app = ClassSearch("./appconfig")

if __name__ == "__main__":
    ClassSearch("./appconfig").run(host="localhost", port=8001, debug=True)
