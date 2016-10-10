<class>
    <div class="course-info">
      <div class="card-header">
        <div class="text-center wraptext" id='title'> { dept } { title } </div>
        <div class="wraptext" id='prof'>Taught by: { prof } </div>
        <div class="wraptext" id='sem'>Running: { sem } </div>
      </div>
      <div if={ books } class="card-body">
          <button onclick={ makeShow(this) } class="btn btn-primary show-button">
              <strong>Show Textbooks</strong>
          </button>
          <div if={ showBooks }>
              <dl>
                  <book each={ books }
                        data="{ this }"
                        resources=""
                        title={ booktitle }
                        author={ bookauthor }
                        price={ bookprice }>
                  </book>
              </dl>
          </div>
      </div>
      <div class="toast" if={ !books }>
        <p class="wraptext">No books at this time</p>
        <p class="wraptext">Check back later, or verify the course has books</p>
      </div>
    </div>
</class>

<script>
this.showBooks = false;
this.update();
</script>
