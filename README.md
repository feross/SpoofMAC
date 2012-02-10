# SpoofMAC - Spoof your MAC address in Mac OS X

### Tested on Lion 10.7, but should work on 10.6 and 10.5 with slight modifications.

Something I've needed to do from time to time is **spoof my computer's MAC address**. This is useful for debugging network issues or temporarily getting onto the Stanford Wi-Fi network when my physical MAC address changes, such as when [Apple replaced my logic board](http://www.quora.com/Is-AppleCare-worth-the-$350/answer/Feross-Aboukhadijeh) (motherboard).

For the uninitiated, a **Media Access Control address** (MAC address) is "a unique identifier assigned to network interfaces for communications on the physical network segment". You can [read more on Wikipedia](http://en.wikipedia.org/wiki/MAC_address).

Despite the fact that all network devices (laptops, iPhones, routers, etc.) have physical MAC addresses burned into the hardware, you can actually change (or spoof) your MAC address **completely in software**, and other network devices will only see your spoofed address.

# Other Solutions Sucked

I was disappointed with the Mac OS X offering in this area. None of the existing stuff worked well. The biggest annoyance with most of the solutions I found was that the Wi-Fi card (Airport) needs to be *manually* disassociated from any connected networks, in order for the change to be applied correctly. Doing this manually every time is annoying.

# My Solution

So, I made a Python script that lets you change your MAC address in one command. **[Check it out and download it from Github.](https://github.com/feross/SpoofMAC)** Improvements welcome!

I tested it on Lion 10.7, but should work on 10.6 and 10.5 with slight modifications.

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
