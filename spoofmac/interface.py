# -*- coding: utf8 -*-
__all__ = (
    'find_interfaces',
    'find_interface',
    'set_interface_mac',
    'wireless_port_names'
)

import re
import subprocess
import sys

if sys.platform == 'win32':
    import _winreg

from spoofmac.util import MAC_ADDRESS_R

# The possible port names for wireless devices as returned by networksetup.
wireless_port_names = ('wi-fi', 'airport')

class OsSpoofer(object): 
    """
    Abstract class for OS level MAC spoofing.
    """ 
    def find_interfaces(self, target):
        raise NotImplementedError("find_interfaces must be implemented") 

    def find_interface(self, target):
        raise NotImplementedError("find_interface must be implemented") 

    def get_interface_mac(self, device):
        raise NotImplementedError("get_interface_mac must be implemented") 

    def set_interface_mac(self, device, mac, port=None):
        raise NotImplementedError("set_interface_mac must be implemented") 


class LinuxSpoofer(OsSpoofer):
    """
    Linux platform specfic implementation for MAC spoofing.
    """
    def get_interface_mac(self, device):
        # TODO implement
        pass

    def set_interface_mac(self, device, mac, port=None):
        # TODO implement
        pass


class WindowsSpoofer(OsSpoofer):
    """
    Windows platform specfic implementation for MAC spoofing.
    """
    WIN_REGISTRY_PATH = "SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    def restart_adapter(self, device):
        """
        Disables and then re-enables device interface
        """
        cmd = "netsh interface set interface \"" + device + "\" disable"
        subprocess.call(cmd, shell=True)
        cmd = "netsh interface set interface \"" + device + "\" enable"
        subprocess.call(cmd, shell=True)

    def get_ipconfig_all(self):
        result = subprocess.check_output(["ipconfig", "/all"], stderr=subprocess.STDOUT)
        return result

    def get_interface_mac(self, device):
        output = self.get_ipconfig_all()

        device = device.lower().strip()

        # search for specific adapter gobble through mac address
        m = re.search("adapter "+device+":[\\n\\r]+(.*?)\\s*Physical Address[^\\d]+(\\s\\S+)", output, re.I | re.DOTALL)
        if not hasattr(m, "group") or m.group(0) == None:
            return None

        adapt_mac = m.group(0)

        # extract physical address then mac
        m = re.search("Physical Address[^\\d]+(\\s\\S+)", adapt_mac)
        phy_addr = m.group(0)
        m = re.search("(?<=:\\s)(.*)", phy_addr)
        if not hasattr(m, "group") or m.group(0) == None:
            return None

        mac = m.group(0)
        return mac

    def find_interfaces(self, targets=None):
        """
        Returns the list of interfaces found on this machine as reported
        by the `ipconfig` command.
        """
        targets = [t.lower() for t in targets] if targets else []
        # Parse the output of `ipconfig /all` which gives
        # us 3 fields used:
        # - the adapter description
        # - the adapter name/device associated with this, if any,
        # - the MAC address, if any

        output = self.get_ipconfig_all()

        # search for specific adapter gobble through mac address
        details = re.findall("adapter (.*?):[\\n\\r]+(.*?)\\s*Physical Address[^\\d]+(\\s\\S+)", output, re.DOTALL)

        # extract out ipconfig results from STDOUT
        for i in range(0, len(details)):
            dns = None
            description = None
            address = None
            adapter_name = details[i][0].strip() 

            # extract DNS suffix
            m = re.search("(?<=:\\s)(.*)", details[i][1])
            if hasattr(m, "group") and m.group(0) != None:
                dns = m.group(0).strip()

            # extract description then strip out value
            m = re.search("Description[^\\d]+(\\s\\S+)", details[i][1])
            if hasattr(m, "group") and m.group(0) != None:
                descript_line = m.group(0)
                m = re.search("(?<=:\\s)(.*)", descript_line)
                if hasattr(m, "group") and m.group(0) != None:
                    description = m.group(0).strip()

            address = details[i][2].strip()

            current_address = self.get_interface_mac(adapter_name)

            if not targets:
                # Not trying to match anything in particular,
                # return everything.
                yield description, adapter_name, address, current_address
                continue

            for target in targets:
                if target in (adapter_name.lower(), adapter_name.lower()):
                    yield description, adapter_name, address, current_address
                    break

    def find_interface(self, target):
        """
        Returns tuple of the first interface which matches `target`.
            adapter description, adapter name, mac address of target, current mac addr
        """
        try:
            return next(self.find_interfaces(targets=[target]))
        except StopIteration:
            pass

    def set_interface_mac(self, device, mac, port=None):
        description, adapter_name, address, current_address = self.find_interface(device)

        # Locate adapter's registry and update network address (mac)
        reg_hdl = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        key = _winreg.OpenKey(reg_hdl, self.WIN_REGISTRY_PATH)
        info = _winreg.QueryInfoKey(key)
        
        # Find adapter key based on sub keys
        adapter_key = None
        adapter_path = None

        for x in range(info[0]):
            subkey = _winreg.EnumKey(key, x)
            path = self.WIN_REGISTRY_PATH + "\\" + subkey

            if subkey == 'Properties':
                break

            # Check for adapter match for appropriate interface
            new_key = _winreg.OpenKey(reg_hdl, path)
            try:
                adapterDesc = _winreg.QueryValueEx(new_key, "AdapterModel")
                if adapterDesc[0] == description:
                    #print adapterDesc[0]
                    adapter_path = path
                    break
                else:
                    _winreg.CloseKey(new_key) 
            except WindowsError, err:
                if err.errno == 2:  # register value not found, ok to ignore
                    pass
                else:
                    raise err

        if adapter_path is None:
            _winreg.CloseKey(key)
            _winreg.CloseKey(reg_hdl)
            return

        # Registry path found update mac addr
        adapter_key = _winreg.OpenKey(reg_hdl, adapter_path, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(adapter_key, "NetworkAddress", 0, _winreg.REG_SZ, mac) 
        _winreg.CloseKey(adapter_key)
        _winreg.CloseKey(key)
        _winreg.CloseKey(reg_hdl)

        # Adapter must be restarted in order for change to take affect
        self.restart_adapter(adapter_name)


class MacSpoofer(OsSpoofer):
    """
    OS X platform specfic implementation for MAC spoofing.
    """

    # Path to Airport binary. This works on 10.7 and 10.8, but might be different
    # on older OS X versions.
    PATH_TO_AIRPORT = (
        '/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport'
    )

    def find_interfaces(self, targets=None):
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

            current_address = self.get_interface_mac(device)

            if not targets:
                # Not trying to match anything in particular,
                # return everything.
                yield port, device, address, current_address
                continue

            for target in targets:
                if target in (port.lower(), device.lower()):
                    yield port, device, address, current_address
                    break


    def find_interface(self, target):
        """
        Returns the first interface which matches `target`.
        """
        try:
            return next(self.find_interfaces(targets=[target]))
        except StopIteration:
            pass


    def set_interface_mac(self, device, mac, port):
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


    def get_interface_mac(self, device):
        """
        Returns currently-set MAC address of given interface. This is
        distinct from the interface's hardware MAC address.
        """

        try:
            result = subprocess.check_output([
                'ifconfig',
                device
            ], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return None

        address = MAC_ADDRESS_R.search(result.upper())
        if address:
            address = address.group(0)

        return address


def get_os_spoofer():
    """
    OsSpoofer factory initializes approach OS platform dependent spoofer.
    """
    spoofer = None

    if sys.platform == 'win32':
        spoofer = WindowsSpoofer()
    elif sys.platform == 'darwin':
	    spoofer = MacSpoofer()
    elif sys.platform.startswith('linux'):
        spoofer = LinuxSpoofer()
    else:
        raise NotImplementedError()

    return spoofer

def find_interfaces(targets=None):
    """
    Returns the list of interfaces found on this machine reported by the OS.

    Target varies by platform:
        MacOS & Linux this is the interface name in ifconfig
        Windows this is the network adapter name in ipconfig
    """
    # Wrapper to interface handles encapsulating objects via Singletons
    spoofer = get_os_spoofer()
    return spoofer.find_interfaces(targets)

def find_interface(targets=None):
    """
    Returns tuple of the first interface which matches `target`.
        adapter description, adapter name, mac address of target, current mac addr

    Target varies by platform:
        MacOS & Linux this is the interface name in ifconfig
        Windows this is the network adapter name in ipconfig
    """
    # Wrapper to interface handles encapsulating objects via Singletons
    spoofer = get_os_spoofer()
    return spoofer.find_interface(targets)

def set_interface_mac(device, mac, port=None):
    """
    Sets the mac address for given `device` to `mac`. 

    Device varies by platform:
        MacOS & Linux this is the interface name in ifconfig
        Windows this is the network adapter name in ipconfig
    """
    # Wrapper to interface handles encapsulating objects via Singletons
    spoofer = get_os_spoofer()
    spoofer.set_interface_mac(device, mac, port)
