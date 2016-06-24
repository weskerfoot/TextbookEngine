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
        console.log(params);
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
            self.loading = false;
            self.update();
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

riot.mount("search");
riot.mount("results");

function autocomplete(element, endpoint) {
  // The element should be an input class
  $(element).autocomplete({
    source : endpoint,
    my : "right top",
    at : "left bottom",
    collision : "none",
    autofocus : true,
    delay     : 100
  });
}

function filterCourses(courses) {
  return courses.filter(
    function (c) {
      return c.prof != "Staff";
    });
}

function take(n, xs) {
  return xs.slice(0, n);
}

function drop(n, xs) {
  return xs.slice(n, xs.length);
}

function groupsof(n, xs) {
  var groups = [];
  while (xs.length != 0) {
    if (xs.length < n) {
      groups.push({"row" : take(xs.length, xs)} );
      xs = drop(xs.length, xs);
    }
    else {
      groups.push({"row" : take(n, xs)});
      xs = drop(n, xs);
    }
  }
  return groups;
}
