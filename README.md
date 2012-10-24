# SpoofMAC - Spoof your MAC address in Mac OS X

### Works on 10.8 (Mountain Lion) and 10.7 (Lion). Probably works on older versions, but not tested.

I made this because changing your MAC address in Mac OS X is harder than it should be. The biggest annoyance is that the Wi-Fi card (Airport) needs to be *manually* disassociated from any connected networks in order for the change to be applied correctly. Doing this manually every time is tedious and lame.

Instead of doing that, just run this Python script and change your MAC address in one command.

## Installation & Usage

### Install by running this in Terminal:

```bash
mkdir ~/Scripts
git clone https://github.com/feross/SpoofMAC.git ~/Scripts/SpoofMAC
cd ~/Scripts/SpoofMAC
```

### Change your MAC address like this:

```sudo python SpoofMAC.py <interface> <mac_address>
```

Substitute `<interface>` with `en0` for ethernet or `en1` for Wi-Fi. Substitute `<mac_address>` with the address you want to set.

**Example:** `sudo python SpoofMAC.py en1 12:12:12:12:12:12`

Note that `sudo` is required because this script runs `ifconfig` which requires admin privledges to change the MAC address.

Also, note that if you're using a **Macbook Air or retina Macbook Pro**, `en0` is Wi-Fi, not `en1`.

## Optional: Run automatically on startup

OS X doesn't let you permanently change your MAC address. Every time you restart your computer, your address gets reset back to whatever it was before. Fortunately, SpoofMAC contains the necessary files for setting this script to run at startup time, so your computer will always have the MAC address you want.

### Startup Installation Instructions

If you want to automatically change your MAC address on computer startup, then run the following commands in Terminal:

```bash
mkdir ~/Scripts
git clone https://github.com/feross/SpoofMAC.git ~/Scripts/SpoofMAC
cd ~/Scripts/SpoofMAC
sudo mkdir /Library/StartupItems/SpoofMAC
sudo cp SpoofMAC StartupParameters.plist /Library/StartupItems/SpoofMAC
cd /Library/StartupItems/SpoofMAC
sudo chown root:wheel SpoofMAC StartupParameters.plist
sudo chmod 0755 SpoofMAC
sudo chmod 0644 StartupParameters.plist
```

This last command will open a text editor. You need to update the path to the location of the SpoofMAC.py file. It will be something like /Users/your_username/Scripts/SpoofMAC/SpoofMAC.py

```bash
sudo nano SpoofMAC
```

Lastly, don't forget to set the `WIRELESS_INTERFACE` and `WIRED_INTERFACE` variables at the top of the `SpoofMac.py` file to whatever you want your MAC address to be! You can open the file for editing with `open ~/Scripts/SpoofMAC/SpoofMAC.py`.

**That's it!** Improvements welcome!

## Handy links for reference

* <http://synergy2.sourceforge.net/autostart.html>
* <http://www.macos.utah.edu/documentation/programming_and_scripting/login_and_logout_scripts/mainColumnParagraphs/00/document/20030219-Scripts.pdf>
* <https://support.apple.com/kb/HT2413>
