<results>
      <div if={notLoading} class="courses container">
       <row class="course-row columns" each={ rows } data="{ this }" classrow={ row }></row>
      </div>
<script>
clicker() {
  alert("clicked");
}
this.rows = [];
var self = this;

results_passer.on("loading",
  function() {
    self.notLoading = false;
    self.update();
  });

results_passer.on("new_results",
  function(data) {
    console.log("new search results detected");
    console.log(data);
    self.rows = data;
    self.notLoading = true;
    self.update();
});
</script>
</results>
