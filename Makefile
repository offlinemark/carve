all:
	make clean
	make run
	make test

test:
	find carvings

run:
	./carve.py

clean:
	rm -rf carvings
