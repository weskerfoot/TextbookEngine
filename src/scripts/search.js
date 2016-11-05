function makeResourceGetter(self) {
    function getResources(ev) {
        ev.preventDefault();
        self.loading = true;
        self.update();
        var params = {
            "title" : this.booktitle,
            "author" : this.bookauthor
        };
        var url = "/search/resources";

        $.getJSON(url, {
            data : JSON.stringify(params)
            }).done(function(results) {
            if (results.iarchive) {
                self.iarchive = results.iarchive[0];
            }

            if (results.openlib) {
                self.openlib = results.openlib[0];
            }

            if (!(results.openlib && results.iarchive)) {
                self.noResources = true;
            }

            self.update({"loading" : false});
            });
    }
    return getResources;
}

function makeShow(self) {
    return function() {
        if (!self.showBooks) {
            self.showBooks = true;
        }
        else {
            self.showBooks = false;
        }
        self.update();
    };
}

function ResultsPasser() {
    riot.observable(this);
    return this;
}

var results_passer = new ResultsPasser();

riot.mount("search", {
                      showHelp : false,
                      booksLoading : false
                     });

riot.mount("results", {notLoading : true});

function realBook(book) {
  var noAdoption = book.booktitle.indexOf("No Adoption");
  var noBooks = book.booktitle.indexOf("No Textbooks");
  return ((noAdoption == -1) &&
          (noBooks == -1));
}

function filterCourses(courses) {
  var books;

  for (var i in courses) {
    books = courses[i].books;
    if ((books.length > 0) &&
        (!realBook(books[0]))) {
      courses[i].books = "";
    }
  }

  return R.filter(
    function (c) {
      return c.prof != "Staff";
    }, courses);
}

function groupsof(n, xs) {
  return R.unfold(
    function(xs) {
      if (R.length(xs) > 0) {
        return [{"row" : R.take(n, xs)}, R.drop(n, xs)];
      }
      return false;
    }, xs);
}
