<search>
  <form class="form-horizontal search-form" onsubmit={ submit.bind(this) } type="submit"method="get">
    <div class="form-group">
        <div class="container">
          <div class="columns">
            <div class="col-sm-8 form-item">
              <input onfocus={ showHelp }
                     class="form-input"
                     placeholder="Description"
                     type="text"
                     name="title"/>
            </div>
            <div class="col-sm-2 form-item">
              <select class="form-select" aria-labelledby="dLabel" name="sem">
                <option value="Fall">Fall</option>
                <option value="Winter" selected>Winter</option>
                <option value="Summer">Summer</option>
              </select>
            </div>
            <div class="col-sm-2 form-item">
              <button class="btn btn-primary" type="submit">Search</button>
            </div>
          </div>
        </div>
    </div>
  </form>
  <div if={ opts.showHelp }
       class="help-toast toast toast-primary">
    <button onclick={ clearHelp }
            class="btn btn-clear float-right">
    </button>
    Type keywords of your course's name or the course code (e.g. PSYCH 2B03)
  </div>
  <div if={ opts.booksLoading } class="search-load">
  </div>
</search>

this.showedHelp = false;
this.waiting = false;

function showHelp() {
  if (!this.showedHelp) {
    this.opts.showHelp = true;
    this.update();
    if (!waiting) {
      waiting = true;
      window.setTimeout(
      (function() {
        this.waiting = false;
        clearHelpTemp.bind(this)();
      }).bind(this), 10000);
    }
  }
}

function clearHelp() {
  this.showedHelp = true;
  this.opts.showHelp = false;
  this.update();
}

function clearHelpTemp() {
  this.opts.showHelp = false;
  this.update();
}

function submit(ev) {
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
