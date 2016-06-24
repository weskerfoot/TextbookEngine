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
	sed -i s,NAME_HERE,"$(SRV_NAME)",g ./build/appconfig;
	sed -i s,ROOT_HERE,"$(SRV_PREFIX)",g ./build/appconfig;

clean:
	rm -fr ./build;

install:
	$(MAKE) clean;
	$(MAKE);
	rm -rf /srv/http/build/;
	cp -rT ./build /srv/http/build/;
	cp -rT ./build/scripts/ $(SRV_ROOT)/scripts/;
	cp -rT ./build/styles/ $(SRV_ROOT)/styles/;
	cp search.ini /srv/http/build/;
