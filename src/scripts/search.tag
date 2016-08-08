<search>
  <form class="form-horizontal search-form" onsubmit={ submit.bind(this) } type="submit"method="get">
    <div class="form-group">
        <div class="col-sm-8 form-item">
            <input class="form-input" placeholder="Description" type="text" name="title"/>
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
  </form>
</search>
function submit(ev) {
    console.log("submitted");
    console.log(this);
    this.opts.booksLoading = true;
    this.update();
    var params = $(ev.currentTarget).serialize();
    $.getJSON("/search/fc?"+params,
        function(courses) {
            var fcourses = filterCourses(courses);
            var cgroups = groupsof(3, fcourses);
            results_passer.trigger("new_results", cgroups);
            this.opts.booksLoading = false;
            this.update();
    });
}
