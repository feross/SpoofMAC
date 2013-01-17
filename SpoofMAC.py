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

# Regex to validate a MAC address, as either 00-00-00-00-00-00
# or 00:00:00:00:00:00.
mac_r = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})')

# The possible port names for wireless devices as returned by networksetup.
wireless_port_names = ('wi-fi', 'airport')


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


def find_interfaces(targets=None):
    """
    Returns the list of interfaces found on this machine as reported
    by the `networksetup` command.
    """
    targets = [t.lower() for t in targets] if targets else []
    # Parse the output of `networksetup -listallhardwareports` which gives
    # us 3 fields per port:
    # - the port name,
    # - the device associated with this port, if any,
    # - The MAC address, if any, otherwise 'N/A'
    details = re.findall(
        r'^(?:Hardware Port|Device|Ethernet Address): (.+)$',
        subprocess.check_output((
            'networksetup',
            '-listallhardwareports'
        )), re.MULTILINE
    )
    # Split the results into chunks of 3 (for our three fields) and yield
    # those that match `targets`.
    for i in range(0, len(details), 3):
        port, device, address = details[i:i + 3]

        address = mac_r.match(address.upper())
        if address:
            address = address.group(0)

        if not targets:
            # Not trying to match anything in particular,
            # return everything.
            yield port, device, address
            continue

        for target in targets:
            if target in (port.lower(), device.lower()):
                yield port, device, address
                break


def find_interface(target):
    """
    Returns the first interface which matches `target`.
    """
    try:
        return next(find_interfaces(targets=[target]))
    except StopIteration:
        pass


def set_mac(port, device, address, mac):
    """
    Sets the mac address for `device` to `mac`.
    """
    if port.lower() in wireless_port_names:
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


def list_interfaces(args):
    targets = []

    # Should we only return prospective wireless interfaces?
    if args['--wifi']:
        targets += wireless_port_names

    for port, device, address in find_interfaces(targets=targets):
        line = []
        line.append('- "{port}"'.format(port=port))
        line.append('on device "{device}"'.format(device=device))
        if address:
            line.append('with MAC address {mac}'.format(mac=address))

        print(' '.join(line))


def main(args):
    if args['list']:
        list_interfaces(args)
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
