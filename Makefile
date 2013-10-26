all:
	make clean
	make run
	make test

test:
	ls carvings/Keyboard

run:
	./carve.py

clean:
	rm -rf carvings
