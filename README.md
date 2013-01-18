# SpoofMAC - Spoof your MAC address in Mac OS X

I made this because changing your MAC address in Mac OS X is harder than it
should be. The biggest annoyance is that the Wi-Fi card (Airport) needs to be
*manually* disassociated from any connected networks in order for the change
to be applied correctly. Doing this manually every time is tedious and lame.

Instead of doing that, just run this Python script and change your MAC address
in one command.

# Installation

You can install from pypi using `easy_install` or `pip`:

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