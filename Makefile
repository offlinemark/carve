all:
	make clean
	make run
	make test

test:
	ls carvings/Maps
	ls carvings/Cookies
	cat carvings/Cookies/cookies_summary.txt

run:
	./carve.py

clean:
	rm -rf carvings
