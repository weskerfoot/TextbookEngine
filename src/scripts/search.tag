<search>
  <form class="form-horizontal search-form" onsubmit={ submit } type="submit"method="get">

    <div class="form-group">
      <div class="container">
        <div class="columns">
          <div if={ false }
             class="help-toast toast toast-primary">
          <button onclick={ clearhelp }
                  class="btn btn-clear float-right">
          </button>
          Type keywords of your course's name or the course code (e.g. PSYCH 2B03)
        </div>
      </div>
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
                  <option value="Fall">Fall</option>
                  <option value="Winter" selected>Winter</option>
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
    var params = $(ev.currentTarget).serialize();
    $.getJSON("/search/fc?"+params,
        (function(courses) {
            var fcourses = filterCourses(courses);
            var cgroups = groupsof(3, fcourses);
            results_passer.trigger("new_results", cgroups);
            this.opts.booksLoading = false;
            this.update();
    }).bind(this));
}
</script>

</search>
