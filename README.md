carve.py
========

This was my hack for the 2013 [Cipher Tech Mobile Forensics Hackathon](https://sites.google.com/site/cthackathon/), sponsored by [Cipher Tech Solutions, Inc](http://twitter.com/ciphertech) and [NU IEEE](http://www.ieee.neu.edu/). It won first place.

the challenge
-------------

At the beginning of the hackathon, everyone was provided with an iPhone image and it was our task to develop software to "carve out" (extract) as much information as we could from the image and output the data in an easily readable format.

overview
--------

The script is designed to be run in the same directory as the iPhone image. Upon execution, it creates a ```carvings``` directory which contains directories for the piece(s) of information being carved, containing the relevant databases used in extraction, and the final product, typically a text file.

	$ ls
	Makefile                 carve.py                 	iOS4_logical_acquisition image_1.7z               
	README.md                carvings
	$ ls carvings/
	AddressBook         Cookies             Logs                	Maps                Safari              Voicemail
	Calendar            Keyboard            Mail                	SMS                 SystemConfiguration
	$ ls carvings/SMS/
	sms.db          sms_summary.txt

todo
----

Feel free to contribute, as there's plenty more data to carve (and the original code is ~~sort of~~ really messy).  Just [get in touch](http://twitter.com/markmossberg) and I'll be happy to send you the image. Here is a list from the event of data up for grabs:

- [x] Address Book
- [ ] Application List
- [ ] Application Snapshots
- [ ] Bluetooth
- [x] Calendar
- [ ] Call History
- [ ] Cell Towers (maybe?)
- [ ] Clipboard Data
- [x] Cookies
- [x] Email
- [ ] Favorite Numbers
- [ ] Geolocation Data (partial)
- [ ] iPod
- [x] Keyboard Data
- [ ] Keychain
- [x] Messages
- [ ] Notes
- [ ] Pictures
- [x] Safari
- [ ] Synced Pictures
- [ ] System Info (partial)
- [ ] Videos
- [ ] Voice Memos
- [x] Voicemail
- [ ] WiFi Access Points (maybe?)
- [x] WiFi Networks
- [ ] Youtube

