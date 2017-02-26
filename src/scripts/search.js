import riot from 'riot';
import './book.tag';
import './class.tag';
import './results.tag';
import './row.tag';
import './search.tag';

var resultsEv = riot.observable();

function mount() {
  riot.mount("search", {
                      booksLoading : false,
                      resultsEv :  resultsEv
                     });
  riot.mount("results", {notLoading : true, resultsEv : resultsEv});
}

mount();
