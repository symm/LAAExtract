#!/usr/bin/python
# Allow Steam LucasArts Adventure Pack to work in ScummVM
import zlib,os

__program__   = "LAAExtract"
__copyright__ = "Copyright (c) 2010"
__license__   = "GPLv3"

atlantis = { 'binary' : 'Indiana Jones and the Fate of Atlantis.exe', 'destination': 'ATLANTIS/ATLANTIS.000', 'dir': 'indiana jones and the fate of atlantis', 'checksum': '60e9988f', 'offset': 224336, 'size': 12035 }
loom     = { 'binary' : 'Loom.exe',                                   'destination': 'LOOM/000.LFL', 'dir': 'loom', 'checksum': '3ef3e225', 'offset': 187248, 'size': 8307  }
indy3    = { 'binary' : 'Indiana Jones and the Last Crusade.exe',     'destination': 'INDY3/00.LFL', 'dir': 'indiana jones and the last crusade',    'checksum': '4f179478', 'offset': 162056, 'size': 6295  }
thedig   = { 'binary' : 'The Dig.exe',                                'destination': 'DIG/DIG.LA0', 'dir': 'the dig', 'checksum': '95af95ad', 'offset': 340632, 'size': 16304 }


def extract(game,path):
    game_binary = "%s/%s/%s" % (path,game['dir'],game['binary'])
    game_dir = "%s/%s/" % (path,game['dir'])
    if not os.path.isfile(game_binary):
        print "Couldn't find '%s'. Did you specify the correct path to your steamapps/common folder?" % (game_binary)
        return False

    f = open(game_binary,"rb")
    f.seek(game['offset'])
    extract = f.read(game['size'])
    extract_checksum = zlib.crc32(extract) & 0xffffffff
    f.close()

    if "%x" % extract_checksum == game['checksum'] :
        r = open(game_dir + "/" + game['destination'],"wb")
        r.write(extract)
        r.close()
        print "Found and wrote to disk: %s (%s)" % (game['destination'], game['checksum'])
    else:
        print "Unable to extract %s from %s (checksum %x didn't match %s)" % (game['destination'],game_binary,extract_checksum, game['checksum'])


if __name__ == "__main__":
    #path = "C:\Windows\Program Files\Steam\SteamApps\common"
    path = "/opt/scummvm-games/"
    games = [indy3,atlantis,loom, thedig]
    for game in games:
        extract(game,path)
