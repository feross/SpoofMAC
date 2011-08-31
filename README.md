# SpoofMAC - Spoof your MAC address in Mac OS X

### Tested on Lion 10.7, but should work on 10.6 and 10.5 with slight modifications.

## Usage

**Note:** Use `en0` for wired ethernet and `en1` for wireless

### From the terminal, run:

`sudo python SpoofMAC.py <interface> <mac_address>`

### Example:

`sudo python SpoofMAC.py en1 12:12:12:12:12:12`

## Optional: Run automatically on startup

### Installation Instructions

If you want to automatically change your MAC address on computer startup, then do the following:

1. Make a folder called /Library/StartupItems/SpoofMAC
2. Add `SpoofMAC`, `SpoofMAC.py`, and `StartupParameters.plist` to the folder.
3. chown all three files to `root:wheel`.
4. chmod `SpoofMAC` and `SpoofMAC.py` to `0755`.
5. chmod `StartupParameters.plist` to 0644.

Also, don't forget to set the `WIRELESS_INTERFACE` and `WIRED_INTERFACE` variables at the top of `SpoofMac.py`!

**That's it!**

## For reference
* <http://synergy2.sourceforge.net/autostart.html>
* <http://www.macos.utah.edu/documentation/programming_and_scripting/login_and_logout_scripts/mainColumnParagraphs/00/document/20030219-Scripts.pdf>
* <https://support.apple.com/kb/HT2413>
