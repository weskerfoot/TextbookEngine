<class>
    <div class="course-info">
      <div class="card-header">
        <h4 class="course-title card-title text-center wraptext" id='title'> { dept } { title } </h4>
        <h6 class="course-prof wraptext" id='prof'>Taught by: { prof } </h6>
        <h6 class="course-sem wraptext" id='sem'>Running: { sem } </h6>
      </div>
      <div if={ books } class="card-body">
          <div class="dropdown">
            <button onclick={showbooks} class="btn btn-link dropdown-toggle" tabindex="0">
              Find Books <i class="icon-caret"></i>
            </button>
            <ul class="menu" if={ this.booksshown }>
              <li class="menu-header">
                <span class="menu-header-text">
                  Potential finds
                </span>
              </li>
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
