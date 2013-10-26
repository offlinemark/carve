all:
	make clean
	make run
	make test

test:
	ls carvings/Safari

run:
	./carve.py

clean:
	rm -rf carvings
