all:
	make clean
	make run
#	make test

test:
	ls carvings/Safari
	ls carvings/Voicemail

run:
	./carve.py

clean:
	rm -rf carvings
