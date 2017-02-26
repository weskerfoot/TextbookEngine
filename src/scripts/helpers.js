import { default as R } from 'ramda';

function realBook(book) {
  var noAdoption = book.booktitle.indexOf("No Adoption");
  var noBooks = book.booktitle.indexOf("No Textbooks");
  return ((noAdoption == -1) &&
          (noBooks == -1));
}

function filterCourses(courses) {
  var books;

  for (var i in courses) {
    books = courses[i].books;
    if ((books.length > 0) &&
        (!realBook(books[0]))) {
      courses[i].books = "";
    }
  }

  return R.filter(
    function (c) {
      return c.prof != "Staff";
    }, courses);
}

function groupsof(n, xs) {
  /* Chunk a list into groups of n size */
  return R.unfold(
    (xs) => {
      if (R.length(xs) > 0) {
        return [{"row" : R.take(n, xs)}, R.drop(n, xs)];
      }
      return false;
    }, xs);
}

export {
  mount,
  realBook,
  filterCourses,
  groupsof
}
