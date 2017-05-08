<results>
  <div class="courses container">
    <row
      class="course-row columns"
      each={ this.rows }
      data={ this }
      classrow={ this.row }>
    </row>
    <span if={this.noResults}>
      No Results!
    </span>
  </div>
<script>

this.rows = [];
var self = this;
self.options = self.opts.opts;

self.notLoading = true;
self.noResults = false;

self.options.resultsEv.on("loading",
  function() {
    self.notLoading = false;
    self.update();
  });

self.options.resultsEv.on("newResults",
  function(data) {
    self.rows = data;
    self.notLoading = true;
    if (self.rows.length == 0) {
      self.noResults = true;
    }
    self.update();
});
</script>
</results>
