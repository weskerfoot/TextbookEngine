<book>
  <div class="text-clip toast">
    <p>
      <button onclick={getresources} class="btn btn-link">
        { booktitle } {bookauthor !== "Ccw" ? "by " + bookauthor : ""}
      </button>
      <dd>
        <div if={ loading } class="loading">
        </div>
        <p if={ iarchive }>
          <a target="_blank" href="{ iarchive }">
            <button class="centered btn">
              Internet Archive Result
            </button>
          </a>
        </p>
        <p if={ openlib }>
          <a target="_blank" href="{ openlib }">
            <button class="centered btn">
              Open Library Result
            </button>
          </a>
        </p>
        <p if={ noresources } class="centered wraptext">
          Couldn't find anything, sorry :(
        </p>
      </dd>
    </p>
  </div>

<script>
this.iarchive = false;
this.openlib = false;
this.noresources = false;

var self = this;

getresources(ev) {
  ev.preventDefault();
  self.loading = true;
  self.update();
  var params = {
      "title" : self.booktitle,
      "author" : self.bookauthor
  };
  var url = "/search/resources";

  $.getJSON(url, {
    data : encodeURIComponent(JSON.stringify(params))
  }).done(function(results) {
    if (results.iarchive) {
      self.iarchive = results.iarchive[0];
    }

    if (results.openlib) {
      self.openlib = results.openlib[0];
    }

    if (!(results.openlib && results.iarchive)) {
      self.noresources = true;
    }

    self.loading = false;
    self.update();
  });
}


</script>
</book>
