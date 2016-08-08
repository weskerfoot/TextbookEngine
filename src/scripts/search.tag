<search>
  <form class="form-horizontal search-form" onsubmit={ submit.bind(this) } type="submit"method="get">
    <div class="form-group">
        <div class="container">
          <div class="columns">
            <div class="col-sm-8 form-item">
              <input
                class="tooltip tooltip-bottom form-input"
                data-tooltip="Type in a couple keywords or the course code (e.g. PSYCH 2B03)"
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
  <div if={ booksLoading } class="search-load">
  </div>
</search>
function submit(ev) {
    ev.preventDefault();
    console.log("submitted");
    this.booksLoading = true;
    this.update();
    results_passer.trigger("loading");
    var params = $(ev.currentTarget).serialize();
    $.getJSON("/search/fc?"+params,
        (function(courses) {
            var fcourses = filterCourses(courses);
            var cgroups = groupsof(3, fcourses);
            results_passer.trigger("new_results", cgroups);
            this.booksLoading = false;
            this.update();
    }).bind(this));
}
