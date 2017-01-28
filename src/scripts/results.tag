<results>
      <div if={notLoading} class="courses container">
       <row if={rows.length > 0} class="course-row columns" each={ rows } data="{ this }" classrow={ row }></row>
       <div if={rows.length <= 0} class="empty">
        No Results, Sorry!
       </div>
      </div>
<script>
clicker() {
  alert("clicked");
}
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
</script>
</results>
