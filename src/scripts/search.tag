<search>
  <form class="form-horizontal search-form" onsubmit={ submit } type="submit" method="get">
    <div class="form-group">
      <div class="container">
          <div class="columns">

            <div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
              <input onfocus={ showhelp }
                     class="form-input search"
                     placeholder="Course Description"
                     type="text"
                     name="title">
              </input>
            </div>

          </div>

          <div class="columns">
            <div class="col-sm-6 col-md-6 col-lg-6">
              <select class="semester form-select float-right" aria-labelledby="dLabel" name="sem">
                <option value="Fall" selected>Fall</option>
                <option value="Winter">Winter</option>
                <option value="Spring/Summer">Spring/Summer</option>
              </select>
            </div>
            <div class="col-sm-6 col-md-6 col-lg-6">

              <button
                class="search-btn btn btn-primary float-left tooltip tooltip-bottom"
                data-tooltip="Search by keywords"
                type="submit">
                  Search
              </button>

            </div>
          </div>
      </div>
    </div>
  </form>

  <div if={ opts.booksLoading } class="search-load">
  </div>

<script>
var self = this;
this.showedHelp = false;
this.waiting = false;

showhelp() {
  if (!this.showedHelp) {
    this.opts.showHelp = true;
    this.update();
    if (!this.waiting) {
      this.waiting = true;
      window.setTimeout(
      (function() {
        this.waiting = false;
        clearHelpTemp.bind(this)();
      }).bind(this), 10000);
    }
  }
}

clearhelp() {
  this.showedHelp = true;
  this.opts.showHelp = false;
  this.update();
}

function clearHelpTemp() {
  this.opts.showHelp = false;
  this.update();
}

submit(ev) {
    ev.preventDefault();
    this.showedHelp = true;
    this.opts.showHelp = false;
    console.log("submitted");
    this.opts.booksLoading = true;
    this.update();
    results_passer.trigger("loading");
    console.log(ev);
    fetch("/search/fc?title="+this.title.value+"&sem="+this.sem.value).then(
      function(response) {
        if (response.ok) {
          response.json().then(
            function(courses) {
              var fcourses = filterCourses(courses);
              var cgroups = groupsof(3, fcourses);
              results_passer.trigger("new_results", cgroups);
              self.opts.booksLoading = false;
              self.update();
          });
        }
    });
}
</script>

</search>
