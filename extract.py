#!/usr/bin/env python
# coding: utf-8
# Helps you to run the Steam LucasArts Adventure Pack in ScummVM
# Licence: GPL

import zlib
import os
import sys
import struct

pc = {
    'atlantis': {
        'name': 'Indiana Jones and the Fate of Atlantis',
        'source_binary': 'Indiana Jones and the Fate of Atlantis.exe',
        'source_dir': 'indiana jones and the fate of atlantis',
        'destination_file': 'ATLANTIS.000',
        'destination_dir': 'ATLANTIS',
        'checksum': '60e9988f',
        'offset': 224336,
        'size': 12035
    },
    'indy3': {
        'name': 'Indiana Jones and the Last Crusade',
        'source_binary': 'Indiana Jones and the Last Crusade.exe',
        'source_dir': 'indiana jones and the last crusade',
        'destination_file': '00.LFL',
        'destination_dir': 'INDY3',
        'checksum': '4f179478',
        'offset': 162056,
        'size': 6295
    },
    'loom': {
        'name': 'Loom',
        'source_binary': 'Loom.exe',
        'source_dir': 'loom',
        'destination_file': '000.LFL',
        'destination_dir': 'LOOM',
        'checksum': '3ef3e225',
        'offset': 187248,
        'size': 8307
    },
    'loom_audio': {
        'name': 'Loom Audio',
        'source_binary': 'CDDA.SOU',
        'source_dir': 'loom\loom',
        'destination_file': 'Track1.wav',
        'destination_dir': 'LOOM',
        'checksum': 'a3362c72',
        'offset': 800,
        'size': 289808002
    },
    'thedig': {
        'name': 'The Dig',
        'source_binary': 'The Dig.exe',
        'source_dir': 'the dig',
        'destination_file': 'DIG.LA0',
        'destination_dir': 'DIG',
        'checksum': '95af95ad',
        'offset': 340632,
        'size': 16304
    }
}

mac = {
    'atlantis': {
        'name': 'Indiana Jones and the Fate of Atlantis',
        'source_binary': 'The Fate of Atlantis',
        'source_dir': 'indiana jones and the fate of atlantis/The Fate of Atlantis.app/Contents/MacOS',
        'destination_file': 'ATLANTIS.000',
        'destination_dir': 'ATLANTIS',
        'checksum': '60e9988f',
        'offset': 260224,
        'size': 12035
    },
    'indy3': {
        'name': 'Indiana Jones and the Last Crusade',
        'source_binary': 'The Last Crusade',
        'source_dir': 'indiana jones and the last crusade/The Last Crusade.app/Contents/MacOS',
        'destination_file': '00.LFL',
        'destination_dir': 'INDY3',
        'checksum': '4f179478',
        'offset': 150368,
        'size': 6295
    },
    'loom': {
        'name': 'Loom',
        'source_binary': 'Loom',
        'source_dir': 'loom/Loom.app/Contents/MacOS',
        'destination_file': '000.LFL',
        'destination_dir': 'LOOM',
        'checksum': '3ef3e225',
        'offset': 170464,
        'size': 8307
    },
    'loom_audio': {
        'name': 'Loom Audio',
        'source_binary': 'CDDA.SOU',
        'source_dir': 'loom/Loom.app/Contents/Resources',
        'destination_file': 'Track1.wav',
        'destination_dir': 'LOOM',
        'checksum': 'a3362c72',
        'offset': 800,
        'size': 289808002
    },
    'thedig': {
        'name': 'The Dig',
        'source_binary': 'The Dig',
        'source_dir': 'the dig/The Dig.app/Contents/MacOS',
        'destination_file': 'DIG.LA0',
        'destination_dir': 'DIG',
        'checksum': '95af95ad',
        'offset': 339744,
        'size': 16304
    }
}


def extract_game_data(extract_information, steam_path, destination_directory):
    game_binary = "%s/%s/%s" % (steam_path,
                                extract_information['source_dir'],
                                extract_information['source_binary'])
    if not os.path.isfile(game_binary):
        print ("\033[91m✘\033[0m %s Does not appear to be installed"
               % (extract_information['name']))
        return False

    f = open(game_binary, "rb")
    f.seek(extract_information['offset'])
    extract = f.read(extract_information['size'])
    extract_checksum = zlib.crc32(extract) & 0xffffffff
    f.close()

    if "%x" % extract_checksum != extract_information['checksum']:
        print (
            "\033[91m✘\033[0m Failed to extract %s (%s) - checksum mismatch" %
            (extract_information['name'], extract_information['destination_file']))
        return False

    if not os.path.exists(
            destination_directory +
            '/' +
            extract_information['destination_dir']):
        os.mkdir(
            destination_directory +
            '/' +
            extract_information['destination_dir'])
    target = destination_directory + '/' + \
        extract_information['destination_dir'] + '/' + extract_information['destination_file']
    r = open(target, "wb")

    if extract_information['name'] == 'Loom Audio':
        print 'Extracting Loom audio, process takes several minutes...'
        r.write(struct.pack('BBBB', 0x52, 0x49, 0x46, 0x46))
        r.write(struct.pack('I', 579123588))
        r.write(struct.pack('BBBB', 0x57, 0x41, 0x56, 0x45))
        r.write(struct.pack('BBBB', 0x66, 0x6D, 0x74, 0x20))
        r.write(struct.pack('BBBB', 16, 0, 0, 0))
        r.write(struct.pack('BB', 1, 0))
        r.write(struct.pack('BB', 2, 0))
        r.write(struct.pack('I', 44100))
        r.write(struct.pack('I', 176400))
        r.write(struct.pack('BB', 4, 0))
        r.write(struct.pack('BB', 16, 0))
        r.write(struct.pack('BBBB', 0x64, 0x61, 0x74, 0x61))
        r.write(struct.pack('I', 579123552))
        extract = extract_loom_audio(extract)
        # TODO: check datafile. should have crc32 e9dee869

    r.write(extract)
    r.close()
    print ("\033[92m✔\033[0m Extracted %s"
           % (extract_information['name']))


def extract_loom_audio(extract):
    frame = 0
    new_extract = ""
    data = enumerate(extract)

    for byte in data:
        if not (byte[0] % 1177):
            frame += 1
            bits = (ord(b) for b in byte[1])
            for b in bits:
                lshift = b >> 4
            bits = (ord(b) for b in byte[1])
            for b in bits:
                rshift = b & 0x0F
        else:
            if (byte[0] %
                2 == 0 and frame %
                2 == 0) or (byte[0] %
                            2 == 1 and frame %
                            2 == 1):
                shift_by = lshift
            else:
                shift_by = rshift
            new_byte = struct.unpack('b', byte[1])[0]
            new_byte = new_byte << shift_by
            if(new_byte & 0x8):
                new_byte = -0x0 + new_byte
            new_extract += struct.pack('<h', new_byte)
        if frame % 2000 == 0:
            sys.stdout.write(
                "%s %s %s\r" %
                ("Frame", frame, "of 246227."))
            sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()

    return new_extract


def get_banner():
    return """                   ___     ___  __        __  ___
|     /\   /\     |__  \_/  |  |__)  /\  /  `  |
|___ /~~\ /~~\    |___ / \  |  |  \ /~~\ \__,  |
        """

if __name__ == "__main__":
    print get_banner()

    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        home_dir = os.path.expanduser("~")

        if len(sys.argv) > 1:
            print "Using steam directory: %s" % sys.argv[1]
            source = sys.argv[1]
        elif sys.platform == "darwin":
            source = home_dir + \
                "/Library/Application Support/Steam/SteamApps/common"
        else:
            print "Usage: %s <path>" % sys.argv[0]
            print "Where <path> is your SteamApps/common folder"
            exit(1)

        if not os.path.exists(source):
            print "ERROR: Could not find your steam app folder at %s" % source
            exit(1)

        destination = home_dir + "/LAAextract"
        if not os.path.exists(destination):
            os.mkdir(destination)
        print "The game files will be extracted to: " + destination + '\n'

        if sys.platform == "darwin":
            for game in mac:
                extract_game_data(mac[game], source, destination)
        else:
            for game in pc:
                extract_game_data(pc[game], source, destination)

        print "\nDon't forget to convert the Loom Track1.wav to flac, ogg, or mp3!"

    elif sys.platform == "win32" or sys.platform == "cygwin":
        import win32gui
        from win32com.shell import shell, shellcon
        desktop_pidl = shell.SHGetFolderLocation(
            0,
            shellcon.CSIDL_DESKTOP,
            0,
            0)
        pidl, display_name, image_list = shell.SHBrowseForFolder(
            win32gui.GetDesktopWindow(),
            desktop_pidl,
            "Select your Steam Apps/common folder",
            0,
            None,
            None
        )
        for game in pc:
            extract_game_data(
                pc[game],
                shell.SHGetPathFromIDList(pidl),
                shell.SHGetPathFromIDList(pidl))
        raw_input("Press Enter to continue...")
