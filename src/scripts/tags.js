riot.tag2('book', '<div class="text-clip toast"> <p> <button onclick="{getresources}" class="btn btn-link"> {booktitle} {bookauthor !== ⁗Ccw⁗ ? ⁗by ⁗ + bookauthor : ⁗⁗} </button> <dd> <div if="{loading}" class="loading"> </div> <p if="{iarchive}"> <a target="_blank" href="{iarchive}"> <button class="centered btn"> Internet Archive Result </button> </a> </p> <p if="{openlib}"> <a target="_blank" href="{openlib}"> <button class="centered btn"> Open Library Result </button> </a> </p> <p if="{noresources}" class="centered wraptext"> Couldn\'t find anything, sorry :( </p> </dd> </p> </div>', '', '', function(opts) {
this.iarchive = false;
this.openlib = false;
this.noresources = false;

var self = this;

this.getresources = function(ev) {
  ev.preventDefault();
  self.loading = true;
  self.update();
  var params = {
      "title" : self.booktitle,
      "author" : self.bookauthor
  };
  var url = "/search/resources";

  fetch(url, {
    method : "POST",
    body : JSON.stringify(params),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(
  function(response) {
    if (response.ok) {
      return response.json()
    }
  }).then(
  function(results) {
    if (results.iarchive) {
      self.iarchive = results.iarchive[0];
    }
    if (results.openlib) {
      self.openlib = results.openlib[0];
    }
    if (!(results.openlib && results.iarchive)) {
      self.noresources = true;
    }
    self.loading = false;
    self.update();
  })
}.bind(this)

});

riot.tag2('class', '<div class="course-info"> <div class="card-header"> <div class="text-center wraptext" id="title"> {dept} {title} </div> <div class="wraptext" id="prof">Taught by: {prof} </div> <div class="wraptext" id="sem">Running: {sem} </div> </div> <div if="{books}" class="card-body"> <button onclick="{showbooks}" class="btn btn-primary show-button"> <strong>Show Textbooks</strong> </button> <div if="{this.booksshown}"> <dl> <book each="{R.uniq(books)}" data="{this}"> </book> </dl> </div> </div> <div class="toast" if="{!books}"> <p class="wraptext">No books at this time</p> <p class="wraptext">Check back later, or verify the course has books</p> </div> </div>', '', '', function(opts) {
booksshown = false;

var self = this;

this.showbooks = function() {
  self.booksshown = !self.booksshown;
  self.update();
}.bind(this)

this.update();
});

riot.tag2('results', '<div if="{notLoading}" class="courses container"> <row if="{rows.length > 0}" class="course-row columns" each="{rows}" data="{this}" classrow="{row}"></row> <div if="{rows.length <= 0}" class="empty"> No Results, Sorry! </div> </div>', '', '', function(opts) {
this.clicker = function() {
  alert("clicked");
}.bind(this)
this.rows = [];
var self = this;

resultsEv.on("loading",
  function() {
    self.notLoading = false;
    self.update();
  });

resultsEv.on("newResults",
  function(data) {
    console.log("new search results detected");
    console.log(data);
    self.rows = data;
    self.notLoading = true;
    self.update();
});
});

riot.tag2('row', '<class class="course text-ellipsis text-justify rounded card column col-md-4" each="{classrow}" data="{this}"> </class>', '', '', function(opts) {
this.classrow = opts.classrow
});


riot.tag2('search', '<form class="form-horizontal search-form" onsubmit="{submit}" type="submit" method="get"> <div class="form-group"> <div class="container"> <div class="columns"> <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12"> <input onfocus="{showhelp}" class="form-input search" placeholder="Course Description" type="text" name="title"> </input> </div> </div> <div class="columns"> <div class="col-sm-6 col-md-6 col-lg-6"> <select class="semester form-select float-right" aria-labelledby="dLabel" name="sem"> <option value="Fall" selected>Fall</option> <option value="Winter">Winter</option> <option value="Spring/Summer">Spring/Summer</option> </select> </div> <div class="col-sm-6 col-md-6 col-lg-6"> <button class="search-btn btn btn-primary float-left tooltip tooltip-bottom" data-tooltip="Search by keywords" type="submit"> Search </button> </div> </div> </div> </div> </form> <div if="{opts.booksLoading}" class="search-load"> </div>', '', '', function(opts) {
var self = this;

this.submit = function(ev) {
    ev.preventDefault();
    this.showedHelp = true;
    this.opts.showHelp = false;
    console.log("submitted");
    this.opts.booksLoading = true;
    this.update();
    resultsEv.trigger("loading");
    console.log(ev);
    fetch("/search/fc?title="+this.title.value+"&sem="+this.sem.value).then(
      function(response) {
        if (response.ok) {
          response.json().then(
            function(courses) {
              var fcourses = filterCourses(courses);
              var cgroups = groupsof(3, fcourses);
              resultsEv.trigger("newResults", cgroups);
              self.opts.booksLoading = false;
              self.update();
          });
        }
    });
}.bind(this)
});
