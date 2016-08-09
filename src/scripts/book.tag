<book>
  <div class="text-clip toast" if={ opts.title && opts.author }>
    <p>
      <dt class="book-title text-center">
        <button onclick={ makeResourceGetter(this) } class="btn tooltip tooltip-top">
          { opts.title }
        </button>
      </dt>
      <dd>
        <div if={ loading } class="loading">
        </div>
        <p if={ iarchive }>
          <a target="_blank" href="{ iarchive }">
            <button class="centered btn btn-link">
              Internet Archive Result
            </button>
          </a>
        </p>
        <p if={ openlib }>
          <a target="_blank" href="{ openlib }">
            <button class="centered btn btn-link">
              Open Library Result
            </button>
          </a>
        </p>
        <p class="centered" if={ noResources }>
          Couldn't find anything, sorry :(
        </p>
      </dd>
    </p>
  </div>
this.iarchive = false;
this.openlib = false;
this.noResources = false;
</book>
