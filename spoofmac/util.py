# -*- coding: utf-8 -*-
__all__ = ('MAC_ADDRESS_R', 'random_mac_address')
import re
import random

# Regex to validate a MAC address, as 00-00-00-00-00-00 or
# 00:00:00:00:00:00 or 000000000000.
MAC_ADDRESS_R = re.compile(r"""
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})[:-]?
    ([0-9A-F]{1,2})
    """,
    re.I | re.VERBOSE
)
# Regex to validate a MAC address in cisco-style, such as
# 0123.4567.89ab
CISCO_MAC_ADDRESS_R = re.compile(
    r'([0-9A-F]{,4})\.([0-9A-F]{,4})\.([0-9A-F]{,4})',
    re.I
)


def _chunk(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def random_mac_address(local_admin=True):
    """
    Generates and returns a random MAC address.
    """
	# Randomly assign a Vendors VM MAC address.
    # Which should decrease chance of colliding
    # with existing devices.
	vendor = random.SystemRandom().choice((
		(0x00,0x05,0x69), #VMware MACs
		(0x00,0x50,0x56), #VMware MACs
		(0x00,0x0C,0x29), #VMware MACs
		(0x00,0x16,0x3E), #Xen VMs
		(0x00,0x03,0xFF), #Microsoft Hyper-V, Virtual Server, Virtual PC
		(0x00,0x1C,0x42), #Parallells 
		(0x00,0x0F,0x4B), #Virtual Iron 4
		(0x08,0x00,0x27)) #Sun Virtual Box
	)
		
	mac = [
		vendor[0],
		vendor[1],
		vendor[2],
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]

    if local_admin:
        # Universally administered and locally administered addresses are
        # distinguished by setting the second least significant bit of the
        # most significant byte of the address. If the bit is 0, the address
        # is universally administered. If it is 1, the address is locally
        # administered. In the example address 02-00-00-00-00-01 the most
        # significant byte is 02h. The binary is 00000010 and the second
        # least significant bit is 1. Therefore, it is a locally administered
        # address.[3] The bit is 0 in all OUIs.
        mac[0] |= 2

    return ':'.join('{0:02X}'.format(o) for o in mac)


def normalize_mac_address(mac):
    """
    Takes a MAC address in various formats:

        - 00:00:00:00:00:00,
        - 00.00.00.00.00.00,
        - 0000.0000.0000

    ... and returns it in the format 00:00:00:00:00:00.
    """
    m = CISCO_MAC_ADDRESS_R.match(mac)
    if m:
        new_mac = ''.join([g.zfill(4) for g in m.groups()])
        return ':'.join(_chunk(new_mac, 2)).upper()

    m = MAC_ADDRESS_R.match(mac)
    if m:
        return ':'.join([g.zfill(2) for g in m.groups()]).upper()

    return None

def normalise_mac_address_windows(mac):
    """
    Takes a MAC address in various formats:

        - 00:00:00:00:00:00,
        - 00-00-00-00-00-00,
        - 00.00.00.00.00.00,
        - 0000.0000.0000

    ... and returns it in the format 00-00-00-00-00-00.
    """
    m = CISCO_MAC_ADDRESS_R.match(mac)
    if m:
        new_mac = ''.join([g.zfill(4) for g in m.groups()])
        return '-'.join(_chunk(new_mac, 2)).upper()

    m = MAC_ADDRESS_R.match(mac)
    if m:
        return '-'.join([g.zfill(2) for g in m.groups()]).upper()

    return None
