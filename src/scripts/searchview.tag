<searchview>
  <div class="animated fadeIn">
    <section class="page-top navbar-section">
      <div class="container">
       <div class="columns">
         <div class="column">
           <h1 class="title inline-block">TextBook Commons</h1>
           <figure class="inline-block avatar-icon avatar avatar-xl">
             <img class="logo" src="/goal.png" />
           </figure>
         </div>
       </div>
       <div class="columns">
         <div class="title column col-sm-12 col-md-12 col-lg-12">
           <h4>Search for a course and find your books</h4>
           <h6>Currently indexes courses for McMaster University.
               <span>Created By <a href="https://twitter.com/weskerfoot">@weskerfoot</a></span>
           </h6>
         </div>
       </div>
       <search opts={this.opts.opts}></search>
      </div>
    </section>
    <results opts={this.opts.opts}></results>
  </div>
</searchview>
