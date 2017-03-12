<class>
    <div class="course-info">
      <div class="card-header">
        <div class="text-center wraptext" id='title'> { dept } { title } </div>
        <div class="wraptext" id='prof'>Taught by: { prof } </div>
        <div class="wraptext" id='sem'>Running: { sem } </div>
      </div>
      <div if={ books } class="card-body">
          <div class="dropdown">
            <button onclick={showbooks} class="btn btn-link dropdown-toggle" tabindex="0">
              Books <i class="icon-caret"></i>
            </button>
            <ul class="menu" if={ this.booksshown }>
              <book each={ this.R.uniq(books) } data="{ this }">
              </book>
            </ul>
          </div>
      </div>
      <div class="toast" if={ !books }>
        <p class="wraptext">No books at this time</p>
        <p class="wraptext">Check back later, or verify the course has books</p>
      </div>
    </div>

<script>
import { default as R } from 'ramda';
this.R = R;
this.booksshown = false;

showbooks() {
  this.booksshown = !this.booksshown;
  this.update();
}

</script>

</class>
