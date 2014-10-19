# SpoofMAC - Spoof your MAC address

### For OS X, Windows, and Linux (most flavors)

I made this because changing your MAC address in Mac OS X is harder than it
should be. The biggest annoyance is that the Wi-Fi card (Airport) needs to be
*manually* disassociated from any connected networks in order for the change
to be applied correctly. Doing this manually every time is tedious and lame.

Instead of doing that, just run this Python script and change your MAC address
in one command. *Now for Windows and Linux, too!*

## Installation

You can install from [PyPI](https://pypi.python.org/pypi/SpoofMAC/) using `pip` or `easy_install`:

```
pip install SpoofMAC
easy_install SpoofMAC
```

or clone/download the repository and install with `setup.py`. Ex:

```
git clone git://github.com/feross/SpoofMAC.git
cd SpoofMAC
python setup.py install
```

If you're not using the system Python (because you use Homebrew, for example), make sure you add '/usr/local/share/python/' (or equivalent) to your path.

Or, consider using **[spoof](https://github.com/feross/spoof)**, a node.js port of this package.

## Usage

SpoofMAC installs a command-line script called `spoof-mac.py`. You can always
see up-to-date usage instructions by typing `spoof-mac.py --help`.

### Examples

Some short usage examples.

#### List available devices:

```bash
spoof-mac.py list
- "Ethernet" on device "en0" with MAC address 70:56:51:BE:B3:00
- "Wi-Fi" on device "en1" with MAC address 70:56:51:BE:B3:01 currently set to 70:56:51:BE:B3:02
- "Bluetooth PAN" on device "en1"
```

#### List available devices, but only those on wifi:

```bash
spoof-mac.py list --wifi
- "Wi-Fi" on device "en0" with MAC address 70:56:51:BE:B3:6F
```

#### Randomize MAC address *(requires root)*

You can use the hardware port name, such as:

```bash
spoof-mac.py randomize wi-fi
```

or the device name, such as:

```bash
spoof-mac.py randomize en0
```

#### Set device MAC address to something specific *(requires root)*

```bash
spoof-mac.py set 00:00:00:00:00:00 en0
```

#### Reset device to its original MAC address *(requires root)*

While not always possible (because the original physical MAC isn't
available), you can try setting the MAC address of a device back
to its burned-in address using `reset`:

```bash
spoof-mac.py reset wi-fi
```

(older versions of OS X may call it "airport" instead of "wi-fi")

Another option to reset your MAC address is to simply restart your computer.
OS X doesn't store changes to your MAC address between restarts. If you want
to make change your MAC address and have it persist between restarts, read
the next section.


## Optional: Run automatically at startup

OS X doesn't let you permanently change your MAC address. Every time you restart your computer, your address gets reset back to whatever it was before. Fortunately, SpoofMAC can easily be set to run at startup time so your computer will always have the MAC address you want.

### Startup Installation Instructions

First, make sure SpoofMAC is [installed](#installation). Then, run the following commands in Terminal:

```bash
# Clone the code
mkdir ~/Scripts
git clone https://github.com/feross/SpoofMAC.git ~/Scripts/SpoofMAC

# Customize location of `spoof-mac.py` to match your system
cd ~/Scripts/SpoofMAC
cat misc/local.macspoof.plist | sed "s|/usr/local/bin/spoof-mac.py|`which spoof-mac.py`|" | tee misc/local.macspoof.plist

# Copy file to the OS X launchd folder
sudo cp misc/local.macspoof.plist /Library/LaunchDaemons

# Set file permissions
cd /Library/LaunchDaemons
sudo chown root:wheel local.macspoof.plist
sudo chmod 0644 local.macspoof.plist

# Delete
rm -rf ~/Scripts/SpoofMAC
```

By default, the above will randomize your MAC address on computer startup. You can change the command that gets run at startup by editing the `/Library/LaunchDaemons/local.macspoof.plist` file.

```bash
sudo vim /Library/LaunchDaemons/local.macspoof.plist
```

## Changelog

- **2.0.0 - Python 3 support**
- 1.2.2 - Fix for Ubuntu 14.04
- 1.2.1 - Fix line endings (dos2unix)
- **1.2.0 - Add Windows and Linux support (thanks CJ!)**
- 1.1.1 - Fix "ValueError: too many values to unpack" error
- 1.1.0 - Fix regression: List command now shows current MAC address
- **1.0.0 - Complete rewrite to conform to PEP8 (thanks Tyler!)**
- **0.0.0 - Original version (by Feross)**

## Contributors

- Feross Aboukhadijeh [http://feross.org]
- Tyler Kennedy [http://www.tkte.ch]
- CJ Barker [cjbarker@gmail.com]

*Improvements welcome! (please add yourself to the list)*

## Ports

- [spoof](https://github.com/feross/spoof) - node.js

## MIT License

Copyright (c) 2011-2013

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
