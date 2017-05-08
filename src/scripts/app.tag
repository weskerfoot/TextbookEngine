<app>
  <ul class="navigate tab tab-block">
    <li class={"tab-item " + this.searchActive}>
      <a onclick={toSearch} href="#">Search</a>
    </li>
    <li class={"tab-item " + this.aboutActive}>
      <a onclick={toAbout} href="#">About</a>
    </li>
  </ul>
  <searchview
    if={this.searchActive}
    ref="searchview"
    opts={this.opts}
  >
  </searchview>
  <aboutview
    if={this.aboutActive}
    ref="aboutview"
  >
  </aboutview>
<script>
import route from 'riot-route';
this.route = route;
this.riot = riot;

this.searchActive = "active";
this.aboutActive = "";
var self = this;

this.route("about",
  function() {
    self.aboutActive = "active";
    self.searchActive = "";
    self.update();
  });

this.route("search",
  function() {
    self.aboutActive = "";
    self.searchActive = "active";
    self.update();
  });


toAbout(e) {
  e.preventDefault();
  this.route("about");
  return;
}

toSearch(e) {
  e.preventDefault();
  this.route("search");
  return;
}


</script>
</app>
