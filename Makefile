all:
	make clean
	make run
	make test

test:
	ls carvings/Mail
	cat carvings/Mail/mail_summary.txt

run:
	./carve.py

clean:
	rm -rf carvings
