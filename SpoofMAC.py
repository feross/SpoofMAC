#! /usr/bin/env python
import re
from subprocess import *
import sys

WIRELESS_INTERFACE = "0123456789ab"
WIRED_INTERFACE = "cdef12345678"

# Path to Airport binary differs between OS X 10.6 and 10.7.
# This is the 10.7 path.
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
	if len(sys.argv) == 1:
		print "Using default MAC adresses for en0 and en1."
		setMACAddress("en0", WIRED_INTERFACE)
		setMACAddress("en1", WIRELESS_INTERFACE)

	elif len(sys.argv) == 3:
		print "Using manual MAC address."
		interface = sys.argv[1]
		address = sys.argv[2]
		setMACAddress(interface, address)

	else:
		print "Wrong number of arguments."

