all:
	make clean
	make run
	make test

test:
	ls carvings/Mail

run:
	./carve.py

clean:
	rm -rf carvings
