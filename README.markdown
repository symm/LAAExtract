LAAExtract
==========

This tool will help you run the Steam version of [**LucasArts Adventure Pack**](http://store.steampowered.com/sub/2102/) in [**ScummVM**](http://www.scummvm.org/) by
extracting the missing files and converting Loom audio (CDDA.SOU).


How to use
----------

MacOS: simply run `./extract`

Linux: run `./extract </path/to/steam apps/common>`

Windows: Make sure you have [Python for Windows extensions](http://sourceforge.net/projects/pywin32/) installed. Choose your Steam Apps directory in the popup dialog


Checksums
---------

    1875b90fade138c9253a8e967007031a *00.LFL  
    5d88b9d6a88e6f8e90cded9d01b7f082 *000.LFL  
    182344899c2e2998fca0bebcd82aa81a *ATLANTIS.000  
    d8323015ecb8b10bf53474f6e6b0ae33 *DIG.LA0

Thanks
------

[somaen](https://github.com/somaen) for the offset in MacOS version of "Fate of Atlantis"

apprentice_fu for figuring out the format of CDDA.SOU

TODO
----
+ Code needs refactoring  
+ Auto detect SteamApps folder in Windows
+ Testing of CDDA.SOU conversion in Windows
