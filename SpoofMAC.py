#! /usr/bin/env python
import re
from subprocess import *
import sys

# Random for MAC value generation
import random

# Generates random MAC value
def randomMAC():
	mac = [ 0x00, 0x16, 0x3e,
		random.randint(0x00, 0x7f),
		random.randint(0x00, 0xff),
		random.randint(0x00, 0xff) ]
	return ':'.join(map(lambda x: "%02x" % x, mac))

WIRELESS_INTERFACE = "0123456789ab"
WIRED_INTERFACE = "cdef12345678"

# Path to Airport binary. This works on 10.7 and 10.8, but might be different in older OS X versions.
PATH_TO_AIRPORT = "/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport"

def execute(command, shell=False):
	"""If shell is true, treat command as string and execute as-is."""

	pipe = Popen(command, stdout=PIPE, shell=shell)
	return pipe.communicate()[0]

def getMACAddress(interface, hardware=False):
	"""Returns current MAC address on given interface.
	If hardware is true, then return the actual hardware MAC address."""

	output = None
	if hardware:
		output = execute(["networksetup", "-getmacaddress", interface])
	else:
		command = "ifconfig {} | grep ether".format(interface)
		output = execute(command, shell=True)

	m = re.search("([0-9a-fA-F]{2}:?){6}", output)
	return m.group(0)

def setMACAddress(interface, address):
	oldAddress = getMACAddress(interface)

	# Turn airport power on & disassociate from connected network
	# This appears to be required even for wired (en0)
	execute(["networksetup", "-setairportpower", "en1", "on"])
	execute([PATH_TO_AIRPORT, "-z"])

	Popen(["ifconfig", interface, "ether", address]) # Set MAC Address

	# Associate airport with known network (if any)
	execute(["networksetup", "-detectnewhardware"])

	# Print result
	newAddress = getMACAddress(interface)
	hardwareAddress = getMACAddress(interface, hardware=True)
	res = "Changed {} (h/w: {}) from {} to {}."
	res = res.format(interface, hardwareAddress, oldAddress, newAddress)
	print(res)
	print("If both addresses are the same, run 'ifconfig {} | grep ether' in a few seconds.".format(interface))

if __name__ == "__main__":
	if len(sys.argv) >= 2 and sys.argv[1] == "-h":
		print "sudo python SpoofMAC.py <interface> <mac_address> (For <interface>, use en0 for wired or en1 for wireless)"
		print "Example: sudo python SpoofMAC.py en1 12:12:12:12:12:12"
	elif len(sys.argv) == 1:
		print "Using default MAC adresses for en0 and en1."
		setMACAddress("en0", WIRED_INTERFACE)
		setMACAddress("en1", WIRELESS_INTERFACE)
	elif len(sys.argv) == 2:
		print "Using random MAC address."
		interface = sys.argv[1]
		address = randomMAC()
		setMACAddress(interface, address)
	elif len(sys.argv) == 3:
		print "Using manual MAC address."
		interface = sys.argv[1]
		address = sys.argv[2]
		setMACAddress(interface, address)
	else:
		print "Wrong number of arguments."

