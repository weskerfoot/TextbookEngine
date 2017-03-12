<book>
  <li class="menu-item text-ellipsis">
    <p>
      <a href="#" onclick={getresources} class="block">
          { booktitle } {bookauthor !== "Ccw" ? "by " + bookauthor : ""}
      </a>
      <dd>
        <div if={ loading } class="loading">
        </div>
        <p if={ iarchive }>
          <a class="btn" target="_blank" href="{ iarchive }">
            Internet Archive Result
          </a>
        </p>
        <p if={ openlib }>
          <a class="btn" target="_blank" href="{ openlib }">
            Open Library Result
          </a>
        </p>
        <p if={ noresources } class="centered wraptext">
          Couldn't find anything, sorry :(
        </p>
      </dd>
    </p>
  </li>

<script>
import 'whatwg-fetch'
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

  fetch(url, {
    method : "POST",
    body : JSON.stringify(params),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(
  function(response) {
    if (response.ok) {
      return response.json()
    }
  }).then(
  function(results) {
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
  })
}


</script>
</book>
