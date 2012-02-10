# SpoofMAC - Spoof your MAC address in Mac OS X

### Tested on Lion 10.7, but should work on 10.6 and 10.5 with slight modifications.

I made this because changing your MAC address in Mac OS X is harder than it should be. The biggest annoyance is that the Wi-Fi card (Airport) needs to be *manually* disassociated from any connected networks in order for the change to be applied correctly. Doing this manually every time is tedious and lame.

Instead of doing that, just run this Python script and change your MAC address in one command.

## Usage

### From the terminal, run:

`sudo python SpoofMAC.py <interface> <mac_address>` (For `<interface>`, use `en0` for wired ethernet and `en1` for wireless)

### Example:

`sudo python SpoofMAC.py en1 12:12:12:12:12:12`

## Optional: Run automatically on startup

### Installation Instructions

If you want to automatically change your MAC address on computer startup, then do the following:

1. Make a folder called /Library/StartupItems/SpoofMAC
2. Add `SpoofMAC` and `StartupParameters.plist` to the folder.
3. chown the files to `root:wheel`.
4. chmod `SpoofMAC` to `0755` and `StartupParameters.plist` to 0644.
5. Update the path in `SpoofMAC` to the location of the `SpoofMAC.py` file. (I keep mine in ~/Scripts for easy editing)

Also, don't forget to set the `WIRELESS_INTERFACE` and `WIRED_INTERFACE` variables at the top of `SpoofMac.py`!

**That's it!** Improvements welcome!

## For reference
* <http://synergy2.sourceforge.net/autostart.html>
* <http://www.macos.utah.edu/documentation/programming_and_scripting/login_and_logout_scripts/mainColumnParagraphs/00/document/20030219-Scripts.pdf>
* <https://support.apple.com/kb/HT2413>
