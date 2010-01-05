#!/usr/bin/python
# Allow Steam LucasArts Adventure Pack to work in ScummVM

import zlib

atlantis = { 'source' : 'Indiana Jones and the Fate of Atlantis.exe', 'destination': 'ATLANTIS.000', 'checksum': '60e9988f', 'offset': 224336, 'size': 12035 }
loom     = { 'source' : 'Loom.exe',                                   'destination': '000.LFL',      'checksum': '3ef3e225', 'offset': 187248, 'size': 8307  }
indy3    = { 'source' : 'Indiana Jones and the Last Crusade.exe',     'destination': '00.LFL',       'checksum': '4f179478', 'offset': 162056, 'size': 6295  }
thedig   = { 'source' : 'The Dig.exe',                                'destination': 'DIG.LA0',      'checksum': '95af95ad', 'offset': 340632, 'size': 16304 }


def extract(game):
	f = open(game['source'],"rb")
	r = open(game['destination'],"wb")

	f.seek(game['offset'])
	extract = f.read(game['size'])
	extract_checksum = zlib.crc32(extract) & 0xffffffff

	if "%x" % extract_checksum == game['checksum'] :
		print "%s matches %s, dumping to file" % (game['checksum'], game['destination'])
		r.write(extract)
	else:
		print "Extracted data checksum %x didn't match %s :(" % (extract_checksum, game['checksum'])

	f.close()
	r.close()

extract(indy3)
extract(atlantis)
extract(loom)
extract(thedig)
raw_input("Press ENTER to exit")
