default:
	mkdir build;
	mkdir build/scripts;
	mkdir build/styles;
	mkdir build/templates;
	riot ./src/scripts/ ./build/scripts/tags.js;
	cp -r ./src/scripts/search.js ./build/scripts/;
	cp -r ./src/styles/* ./build/styles/;
	cp -r ./src/templates/search.html ./build/templates/;
	cp -r ./src/{archive.py,openlibrary.py,predictions.py,search.py,website.py,textbookExceptions.py} ./build/;
	cp ./src/appconfig ./build/;

clean:
	rm -r ./build;
