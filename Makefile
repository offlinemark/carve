all:
	make clean
	make run
	make test

test:
	ls carvings/Maps

run:
	./carve.py

clean:
	rm -rf carvings
