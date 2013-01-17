#!/usr/bin/env python
# -*- coding: utf8 -*-
"""SpoofMAC

Usage:
  SpoofMAC.py list [--wifi]
  SpoofMAC.py randomize <devices>...
  SpoofMAC.py set <mac> <devices>...
  SpoofMAC.py reset <devices>...

"""
import re
import sys
import random
import subprocess

from docopt import docopt

# Path to Airport binary. This works on 10.7 and 10.8, but might be different
# on older OS X versions.
PATH_TO_AIRPORT = (
    '/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport'
)


mac_r = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})')


def random_mac():
    """
    Generates and returns a random MAC address.
    """
    #Taken from the CentOS Virtualization Guide.
    mac = [
        0x00,
        0x16,
        0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join('{0:02X}'.format(o) for o in mac)


def get_interfaces():
    """
    Returns the list of interfaces found on this machine as reported
    by the `networksetup` command.
    """
    details = re.findall(
        r'^(?:Hardware Port|Device|Ethernet Address): (.+)$',
        subprocess.check_output((
            'networksetup',
            '-listallhardwareports'
        )), re.MULTILINE
    )
    for i in range(0, len(details), 3):
        port, device, address = details[i:i + 3]
        address = mac_r.match(address.upper())
        if address:
            address = address.group(0)

        yield (port, device, address)


def find_interface(target):
    """
    Returns the interface for `device`.
    """
    for port, device, address in get_interfaces():
        if target.lower() in (port.lower(), device.lower()):
            return port, device, address
    return None


def set_mac(port, device, address, mac):
    """
    Sets the mac address for `device` to `mac`.
    """
    if port.lower() in ('wi-if', 'airport'):
        # Turn on the device, assuming it's an airport device.
        subprocess.call([
            'networksetup',
            '-setairportpower',
            device,
            'on'
        ])

    # For some reason this seems to be required even when changing a
    # non-airport device.
    subprocess.check_call([
        PATH_TO_AIRPORT,
        '-z'
    ])

    # Change the MAC.
    subprocess.check_call([
        'ifconfig',
        device,
        'ether',
        mac
    ])

    # Associate airport with known network (if any)
    subprocess.check_call([
        'networksetup',
        '-detectnewhardware'
    ])


def list_devices(args):
    for port, device, address in get_interfaces():
        if args['--wifi'] and port.lower() not in ('wi-fi', 'airport'):
            continue

        line = []
        line.append('- "{port}"'.format(port=port))
        line.append('on device "{device}"'.format(device=device))
        if address:
            line.append('with MAC address {mac}'.format(mac=address))

        print(' '.join(line))


def main(args):
    if args['list']:
        list_devices(args)
    elif args['randomize'] or args['set'] or args['reset']:
        for target in args['<devices>']:
            # Fill out the details for `target`, which could be a Hardware
            # Port or a literal device.
            result = find_interface(target)
            if result is None:
                print('- couldn\'t find the device for {target}'.format(
                    target=target
                ))
                return 1

            port, device, address = result
            if args['randomize']:
                target_mac = random_mac()
            elif args['set']:
                target_mac = args['<mac>']
            elif args['reset']:
                if address is None:
                    print('- {target} missing hardware MAC'.format(
                        target=target
                    ))
                    continue
                target_mac = address

            if not mac_r.match(target_mac):
                print('- {mac} is not a valid MAC address'.format(
                    mac=target_mac
                ))
                return 1

            set_mac(port, device, address, target_mac)

    return 1


if __name__ == '__main__':
    arguments = docopt(__doc__)
    sys.exit(main(arguments))
