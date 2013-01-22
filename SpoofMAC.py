#! /usr/bin/env python

import re
from subprocess import *
import sys

# Random for MAC value generation
import random

MAC_REGEX = "([0-9a-fA-F]{2}:?){6}"
WIRELESS_INTERFACE = "0123456789ab"
WIRED_INTERFACE = "cdef12345678"

# Path to Airport binary. This works on 10.7 and 10.8, but might be different in older OS X versions.
PATH_TO_AIRPORT = "/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport"

# Return Codes
SUCCESS = 0
WRONG_ARGS = 1001
UNSUPPORTED_PLATFORM = 1002

def randomMAC():
    """Generates random MAC value."""
    mac = [ 0x00, 0x16, 0x3e,
    random.randint(0x00, 0x7f),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def execute(command, shell=False):
    """If shell is true, treat command as string and execute as-is."""
    pipe = Popen(command, stdout=PIPE, shell=shell)
    return pipe.communicate()[0]

def outputResults(spoofer, interface, oldAddress):
    """Print results"""
    newAddress = spoofer.getMACAddress(interface)
    res = "Changed {} MAC from {} to {}."
    res = res.format(interface, oldAddress, newAddress)
    print(res)
    print("If both addresses are the same, run 'ifconfig {} | grep {}' in a few seconds.".format(interface, interface)) 

class OsSpoofer(): 
    """Abstract class for OS level MAC spoofing.""" 
    def getMACAddress(self, interface, hardware=False): 
        raise NotImplementedError("getMACAddress must be implemented") 

    def setMACAddress(self, interface, address): 
        raise NotImplementedError("setMACAddress must be implemented") 

class MacSpoofer(OsSpoofer):
    def getMACAddress(self, interface, hardware=False):
        """Returns current MAC address on given interface.
        If hardware is true, then return the actual hardware MAC address."""

        output = None
        if hardware:
            output = execute(["networksetup", "-getmacaddress", interface])
        else:
            command = "ifconfig {} | grep ether".format(interface)
            output = execute(command, shell=True)

        m = re.search(MAC_REGEX, output)
        return m.group(0)

    def setMACAddress(self, interface, address):
        # Turn airport power on & disassociate from connected network
        # This appears to be required even for wired (en0)
        execute(["networksetup", "-setairportpower", "en1", "on"])
        execute([PATH_TO_AIRPORT, "-z"])

        Popen(["ifconfig", interface, "ether", address]) # Set MAC Address

        # Associate airport with known network (if any)
        execute(["networksetup", "-detectnewhardware"])

class LinuxSpoofer(OsSpoofer):
    def getMACAddress(self, interface, hardware=False):
        command = "ifconfig {} | grep HWaddr".format(interface)
        output = execute(command, shell=True)
        m = re.search(MAC_REGEX, output)
        return m.group(0)

    def setMACAddress(self, interface, address):
        command = "ifconfig {} down hw ether {}".format(interface, address)
        execute(command, shell=True)
        command = "ifconfig {} up".format(interface)
        execute(command, shell=True)

class WindowsSpoofer(OsSpoofer):
    pass

if __name__ == "__main__":
    spoofer = None
    #if (sys.platform == 'win32' or sys.platform == 'cygwin'): # TODO implement for Windoze
        #spoofer = WindowsSpoofer()
    if (sys.platform == 'darwin'):
	spoofer = MacSpoofer()
    elif (sys.platform == 'linux' or sys.platform == 'linux2'):
        spoofer = LinuxSpoofer()
    else:
        print 'Platform not supported'
        sys.exit(UNSUPPORTED_PLATFORM)

    oldAddress  = None
    oldAddress2 = None

    if len(sys.argv) == 1:
	print "Using default MAC adresses for en0 and en1."
        oldAddress = spoofer.getMACAddress("en0")
        spoofer.setMACAddress("en0", WIRED_INTERFACE)
        oldAddress2 = spoofer.getMACAddress("en1")
        spoofer.setMACAddress("en1", WIRELESS_INTERFACE)
    elif sys.argv[1] == "-h":
	print "sudo python SpoofMAC.py <interface> <mac_address> (For <interface>, use en0 for wired or en1 for wireless)"
	print "Example: sudo python SpoofMAC.py en1 12:12:12:12:12:12"
    	sys.exit(SUCCESS)
    elif len(sys.argv) == 2:
        print "Using random MAC address."
	interface = sys.argv[1]
	address = randomMAC()
        oldAddress = spoofer.getMACAddress(interface)
	spoofer.setMACAddress(interface, address)
    elif len(sys.argv) == 3:
	print "Using manual MAC address."
	interface = sys.argv[1]
	address = sys.argv[2]
        oldAddress = spoofer.getMACAddress(interface)
	spoofer.setMACAddress(interface, address)
    else:
	print "Wrong number of arguments."
        sys.exit(WRONG_ARGS)

    if oldAddress2 == None:
        outputResults(spoofer, interface, oldAddress)
    else:
        outputResults(spoofer, "en0", oldAddress)
        outputResults(spoofer, "en1", oldAddress2)
        
    sys.exit(SUCCESS)
