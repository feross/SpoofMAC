# -*- coding: utf8 -*-
__all__ = ('MAC_ADDRESS_R', 'random_mac_address')
import re
import random

# Regex to validate a MAC address, as either 00-00-00-00-00-00
# or 00:00:00:00:00:00.
MAC_ADDRESS_R = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})')


def random_mac_address(local_admin=True):
    """
    Generates and returns a random MAC address.
    """
    # By default use a random address in VMWare's MAC address
    # range used by VMWare VMs, which has a very slim chance of colliding
    # with existing devices.
    mac = [
        0x00,
        0x05,
        0x69,
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
