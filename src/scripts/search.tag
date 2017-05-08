<search>
  <form class="form-horizontal search-form"
        onsubmit={ submit }
        method="get"
  >
    <div class="form-group">
      <div class="container">
          <div class="columns">
            <div class="search column col-xs-12 col-sm-12 col-md-12 col-lg-12">
              <input onfocus={ showhelp }
                     class="form-input search"
                     placeholder="Course Description (e.g. history)"
                     type="text"
                     ref="title">
              </input>
            </div>

          </div>

          <div class="columns">
            <div class="column col-xs-12 col-sm-12 col-md-12 col-lg-12">
              <button
                class="inline-block search-btn btn btn-primary tooltip tooltip-bottom"
                data-tooltip="Search by keywords"
                type="submit">
                  Search
              </button>
              <select class="inline-block semester form-select" aria-labelledby="dLabel" ref="sem">
                <option value="Fall" selected>Fall</option>
                <option value="Winter">Winter</option>
                <option selected value="Spring/Summer">Spring/Summer</option>
              </select>
            </div>
          </div>
      </div>
    </div>
  </form>

  <div if={ options.booksLoading } class="search-load">
  </div>

<script>

import {filterCourses, groupsof} from './helpers.js';
import 'whatwg-fetch';

var self = this;
self.options = self.opts.opts;

submit(ev) {
    ev.preventDefault();
    self.options.booksLoading = true;
    self.update();
    self.options.resultsEv.trigger("loading");
    console.log(ev);
    fetch("/search/fc?title="+self.refs.title.value+"&sem="+self.refs.sem.value).then(
      function(response) {
        if (response.ok) {
          response.json().then(
            function(courses) {
              var fcourses = filterCourses(courses);
              var cgroups = groupsof(3, fcourses);
              self.options.resultsEv.trigger("newResults", cgroups);
              self.options.booksLoading = false;
              self.update();
          });
        }
    });
}
</script>

</search>
