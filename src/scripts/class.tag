<class>
    <div class="course-info">
      <div class="card-header">
        <div class="text-center wraptext" id='title'> { dept } { title } </div>
        <div class="wraptext" id='prof'>Taught by: { prof } </div>
        <div class="wraptext" id='sem'>Running: { sem } </div>
      </div>
      <div if={ books } class="card-body">
          <button onclick={showbooks} class="btn btn-primary show-button">
              <strong>Show Textbooks</strong>
          </button>
          <div if={ this.booksshown }>
              <dl>
                  <book each={ books } data="{ this }">
                  </book>
              </dl>
          </div>
      </div>
      <div class="toast" if={ !books }>
        <p class="wraptext">No books at this time</p>
        <p class="wraptext">Check back later, or verify the course has books</p>
      </div>
    </div>

<script>
booksshown = false;

var self = this;

showbooks() {
  self.booksshown = !self.booksshown;
  self.update();
}

this.update();
</script>
</class>
