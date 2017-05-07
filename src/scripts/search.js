import riot from 'riot';
import router from 'riot-route/lib/tag';
import './book.tag';
import './class.tag';
import './results.tag';
import './row.tag';
import './search.tag';
import './searchview.tag';
import './aboutview.tag';
import './app.tag';

var resultsEv = riot.observable();

function mount() {
  riot.mount("app", {
                      booksLoading : false,
                      resultsEv :  resultsEv,
                      notLoading: true
                     });
}

mount();
