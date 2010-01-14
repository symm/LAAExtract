#!/usr/bin/python
# Allow Steam LucasArts Adventure Pack to work in ScummVM
import zlib,os

__program__   = "LAAExtract"
__copyright__ = "Copyright (c) 2010"
__license__   = "GPLv3"

atlantis = { 'source' : 'Indiana Jones and the Fate of Atlantis.exe', 'destination': 'ATLANTIS.000', 'dir': 'ATLANTIS', 'checksum': '60e9988f', 'offset': 224336, 'size': 12035 }
loom     = { 'source' : 'Loom.exe',                                   'destination': '000.LFL',      'dir': 'LOOM',     'checksum': '3ef3e225', 'offset': 187248, 'size': 8307  }
indy3    = { 'source' : 'Indiana Jones and the Last Crusade.exe',     'destination': '00.LFL',       'dir': 'INDY3',    'checksum': '4f179478', 'offset': 162056, 'size': 6295  }
thedig   = { 'source' : 'The Dig.exe',                                'destination': 'DIG.LA0',      'dir': 'DIG',      'checksum': '95af95ad', 'offset': 340632, 'size': 16304 }


def extract(game):
    if not os.path.isfile(game['source']): 
        print "Couldn't find '%s' in the current directory. Did you copy the .exe here?" % (game['source'])
        return False

    f = open(game['source'],"rb")
    f.seek(game['offset'])
    extract = f.read(game['size'])
    extract_checksum = zlib.crc32(extract) & 0xffffffff
    f.close()

    if "%x" % extract_checksum == game['checksum'] :
        if not os.path.exists(game['dir']):
            os.mkdir(game['dir'])
        r = open(game['dir'] + "/" + game['destination'],"wb")
        r.write(extract)
        r.close()
        print "Found and wrote to disk: %s (%s)" % (game['destination'], game['checksum'])
    else:
        print "Unable to extract %s from %s (checksum %x didn't match %s)" % (game['destination'],game['source'],extract_checksum, game['checksum'])


if __name__ == "__main__":
    extract(indy3)
    extract(atlantis)
    extract(loom)
    extract(thedig)
