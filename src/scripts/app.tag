<app>
  <ul class="tab tab-block">
    <li class={"tab-item " + this.searchActive}>
      <a onclick={toSearch} href="">Search</a>
    </li>
    <li class={"tab-item " + this.aboutActive}>
      <a onclick={toAbout} href="/about">About</a>
    </li>
  </ul>
  <router>
    <route path="/">
      <div class="animated fadeIn">
        <searchview></searchview>
      </div>
    </route>
    <route path="/about">
      <div class="animated fadeIn">
        <aboutview></aboutview>
      </div>
    </route>
  </router>
<script>
import route from 'riot-route';
this.route = route;

this.searchActive = "";
this.aboutActive = "";
var self = this;

this.route("about",
  function() {
    self.aboutActive = "active";
    self.searchActive = "";
    self.update();
  });

this.route("/",
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
  this.route("");
  return;
}


</script>
</app>
