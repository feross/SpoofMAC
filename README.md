# SpoofMAC - Spoof your MAC address in Mac OS X

I made this because changing your MAC address in Mac OS X is harder than it
should be. The biggest annoyance is that the Wi-Fi card (Airport) needs to be
*manually* disassociated from any connected networks in order for the change
to be applied correctly. Doing this manually every time is tedious and lame.

Instead of doing that, just run this Python script and change your MAC address
in one command.

# Installation

You can install from pypi using `easy_install` or `pip` (COMING SOON):

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

# Usage

SpoofMAC installs a command-line script called `spoof-mac`. You can always
see up-to-date usage instructions by typing `spoof-mac --help`.

## Examples

Some short usage examples.

### List available devices, but only those on wifi:

```
spoof-mac list --wifi
- "Wi-Fi" on device "en0" with MAC address 70:56:51:BE:B3:6F
```

### Randomize Wireless MAC address

You can use the hardware port name, such as:
```
spoof-mac randomize wi-fi
```

or the device name, such as:

```
spoof-mac randomize en0
```

### Reset device to its original MAC address

While not always possible (because the original physical MAC isn't
available), you can try setting the MAC address of a device back
to its burned-in address using `reset`:

```
spoof-mac reset wi-fi
```

(older versions of OS X may call it "airport" instead of "wi-fi")

## Changelog

- 1.0.0 Rewritten by Tyler to conform to PEP8.
- pre-1.0 original version by Feross.

## Contributors

- Feross Aboukhadijeh <http://feross.org>
- Tyler Kennedy <http://www.tkte.ch>

## MIT License

Copyright (c) 2011-2013

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
