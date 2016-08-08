<results>
      <div class="courses container">
       <row class="course-row columns" each={ rows } data="{ this }" classrow={ row }></row>
      </div>
this.rows = [];
var self = this;
results_passer.on("new_results",
  function(data) {
    console.log("new search results detected");
    console.log(data);
    self.rows = data;
    self.update();
});
</results>
