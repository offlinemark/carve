all:
	make clean
	make run
	make test

test:
	ls carvings

run:
	./carve.py

clean:
	rm -rf carvings
