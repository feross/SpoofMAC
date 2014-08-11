#!/usr/bin/env python
# -*- coding: utf8 -*-
"""SpoofMAC

Usage:
    spoof-mac list [--wifi]
    spoof-mac randomize [--local] <devices>...
    spoof-mac set <mac> <devices>...
    spoof-mac reset <devices>...
    spoof-mac normalize <mac>
    spoof-mac -h | --help
    spoof-mac --version

Options:

    -h --help       Shows this message.
    --version       Show package version.
    --wifi          Try to only show wireless interfaces.
    --local         Set the locally administered flag on randomized MACs.
"""
import sys
import os

if sys.platform == 'win32':
    import ctypes

from docopt import docopt

from spoofmac.version import __version__
from spoofmac.util import random_mac_address, MAC_ADDRESS_R, normalize_mac_address

from spoofmac.interface import (
    wireless_port_names,
    find_interfaces,
    find_interface,
    set_interface_mac,
    get_os_spoofer
)

# Return Codes
SUCCESS = 0
INVALID_ARGS = 1001
UNSUPPORTED_PLATFORM = 1002
INVALID_TARGET = 1003
INVALID_MAC_ADDR = 1004
NON_ROOT_USER = 1005


def list_interfaces(args, spoofer):
    targets = []

    # Should we only return prospective wireless interfaces?
    if args['--wifi']:
        targets += wireless_port_names

    for port, device, address, current_address in spoofer.find_interfaces(targets=targets):
        line = []
        line.append('- "{port}"'.format(port=port))
        line.append('on device "{device}"'.format(device=device))
        if address:
            line.append('with MAC address {mac}'.format(mac=address))
        if current_address and address != current_address:
            line.append('currently set to {mac}'.format(mac=current_address))
        print((' '.join(line)))


def main(args, root_or_admin):
    spoofer = None

    try:
        spoofer = get_os_spoofer()
    except NotImplementedError:
        return UNSUPPORTED_PLATFORM

    if args['list']:
        list_interfaces(args, spoofer)
    elif args['randomize'] or args['set'] or args['reset']:
        for target in args['<devices>']:
            # Fill out the details for `target`, which could be a Hardware
            # Port or a literal device.
            #print("Debuf:",target)
            result = find_interface(target)
            if result is None:
                print(('- couldn\'t find the device for {target}'.format(
                    target=target
                )))
                return INVALID_TARGET

            port, device, address, current_address = result
            if args['randomize']:
                target_mac = random_mac_address(args['--local'])
            elif args['set']:
                target_mac = args['<mac>']
            elif args['reset']:
                if address is None:
                    print(('- {target} missing hardware MAC'.format(
                        target=target
                    )))
                    continue
                target_mac = address

            if not MAC_ADDRESS_R.match(target_mac):
                print(('- {mac} is not a valid MAC address'.format(
                    mac=target_mac
                )))
                return INVALID_MAC_ADDR

            if not root_or_admin:
                if sys.platform == 'win32':
                    print('Error: Must run this with administrative privileges to set MAC addresses')
                    return NON_ROOT_USER
                else:
                    print('Error: Must run this as root (or with sudo) to set MAC addresses')
                    return NON_ROOT_USER

            set_interface_mac(device, target_mac, port)
    elif args['normalize']:
        print((normalize_mac_address(args['<mac>'])))

    else:
        print('Error: Invalid arguments - check help usage')
        return INVALID_ARGS

    del spoofer

    return SUCCESS


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    try:
        root_or_admin = os.geteuid() == 0
    except AttributeError:
        root_or_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    sys.exit(main(arguments, root_or_admin))
