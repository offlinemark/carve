all:
	make clean
	make run
	make test

test:
	cat carvings/SystemConfiguration/wifi_cell_networks.txt

run:
	./carve.py

clean:
	rm -rf carvings
