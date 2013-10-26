all:
	make clean
	make run
	make test

test:
	find carvings/SMS
	cat carvings/sms/sms_summary.txt

run:
	./carve.py

clean:
	rm -rf carvings
