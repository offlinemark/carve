all:
	make clean
	make run
	make test

test:
	ls carvings/AddressBook
	cat carvings/AddressBook/addressbook_summary.txt

run:
	./carve.py

clean:
	rm -rf carvings
