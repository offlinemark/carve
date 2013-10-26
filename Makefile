all:
	make clean
	make run
	make test

test:
	ls carvings/Cookies

run:
	./carve.py

clean:
	rm -rf carvings
