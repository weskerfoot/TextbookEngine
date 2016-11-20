<book>
  <div class="text-clip toast">
    <p>
      <dt class="book-title text-center">
        <button onclick={getresources} class="btn btn-link">
          { title }
        </button>
      </dt>
      <dd>
        <div if={ loading } class="loading">
        </div>
        <p if={ this.iarchive }>
          <a target="_blank" href="{ iarchive }">
            <button class="centered btn btn-link">
              Internet Archive Result
            </button>
          </a>
        </p>
        <p if={ this.openlib }>
          <a target="_blank" href="{ openlib }">
            <button class="centered btn btn-link">
              Open Library Result
            </button>
          </a>
        </p>
        <p class="centered wraptext" if={ noresources }>
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

getresources() {
  self.loading = true;
  self.update();
  var params = {
      "title" : this.booktitle,
      "author" : this.bookauthor
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

    self.update({"loading" : false});
  });
}


</script>
</book>
