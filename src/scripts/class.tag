<class>
    <div class="course-info">
      <div class="card-header">
        <h4 class="course-title card-title text-center wraptext" id='title'> { dept } { title } </h4>
        <h6 class="course-prof wraptext" id='prof'>Taught by: { prof } </h6>
        <h6 class="course-sem wraptext" id='sem'>Running: { sem } </h6>
      </div>
      <div if={ books } class="card-body">
          <div class="dropdown">
            <a
              class="btn btn-link dropdown-toggle tooltip tooltip-bottom"
              tabindex="0"
              data-tooltip={`${this.books.length} ${this.books.length > 1 ? "books" : "book"}`}
            >
              Find Books <i class="icon-caret"></i>
            </a>
            <ul class="menu">
              <li class="menu-header">
                <span class="menu-header-text">
                  Potential finds
                </span>
              </li>
              <li data-is="book" each={ this.R.uniq(books) } data="{ this }">
              </li>
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
</script>

</class>
