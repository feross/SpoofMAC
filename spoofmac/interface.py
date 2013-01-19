# -*- coding: utf8 -*-
__all__ = (
    'find_interfaces',
    'find_interface',
    'set_interface_mac',
    'wireless_port_names'
)
import re
import subprocess

from spoofmac.util import MAC_ADDRESS_R

# Path to Airport binary. This works on 10.7 and 10.8, but might be different
# on older OS X versions.
PATH_TO_AIRPORT = (
    '/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport'
)

# The possible port names for wireless devices as returned by networksetup.
wireless_port_names = ('wi-fi', 'airport')


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

        address = MAC_ADDRESS_R.match(address.upper())
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


def set_interface_mac(port, device, address, mac):
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
