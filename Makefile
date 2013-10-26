all:
	make clean
	make run
	make test

test:
	ls carvings/Safari
	cat carvings/Safari/safari_bookmarks_summary.txt

run:
	./carve.py

clean:
	rm -rf carvings
