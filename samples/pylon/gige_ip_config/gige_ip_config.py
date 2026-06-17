#!/usr/bin/env python3
"""\
Configure the IP settings of a Basler GigE Vision camera.

Usage:
    gige_ip_config.py <MAC> <IP> [MASK] [GATEWAY]

    <MAC> is the MAC address without separators, e.g. 0030531596CF
    <IP> is one of the following:
         - AUTO to use Auto-IP (LLA)
         - DHCP to use DHCP
         - otherwise a dotted IPv4 address, e.g. 192.168.1.1
    [MASK] is optional and defaults to 255.255.255.0
    [GATEWAY] is optional and defaults to 0.0.0.0

This sample prints available GigE Vision devices and then optionally applies a new
startup IP configuration to the selected device.

Note: This sample doesn't support the Basler Stereo Mini cameras because they use
a different network protocol and IP configuration mechanism.
"""

import ipaddress
import sys

from pypylon import pylon


DEFAULT_SUBNET_MASK = "255.255.255.0"
DEFAULT_GATEWAY = "0.0.0.0"


def normalize_mac_address(mac_address: str) -> str:
    return mac_address.replace(":", "").replace("-", "").replace(".", "").upper()


def get_mode(device_info) -> str:
    if device_info.IsPersistentIpActive():
        return "Static"
    if device_info.IsDhcpActive():
        return "DHCP"
    if device_info.IsAutoIpActive():
        return "AutoIP"
    return "Unknown"


def print_usage() -> None:
    print("Usage: gige_ip_config.py <MAC> <IP> [MASK] [GATEWAY]")
    print("       <MAC> is the MAC address without separators, e.g., 0030531596CF")
    print("       <IP> is one of the following:")
    print("            - AUTO to use Auto-IP (LLA).")
    print("            - DHCP to use DHCP.")
    print("            - Everything else is interpreted as a new IP address in dotted notation, e.g., 192.168.1.1")
    print(f"       [MASK] is the network mask in dotted notation. This is optional. {DEFAULT_SUBNET_MASK} is used as default.")
    print(f"       [GATEWAY] is the gateway address in dotted notation. This is optional. {DEFAULT_GATEWAY} is used as default.")
    print("Please note that this is a sample and no sanity checks are made.")
    print()


def print_available_devices(device_infos) -> None:
    print("Available Devices".ljust(95) + "supports")
    print(
        f"{'Friendly Name':<32}  {'MAC':<12}  {'IP Address':<15}  {'Subnet Mask':<15}  "
        f"{'Gateway':<15}  {'Mode':<7} {'IP?':>3} {'DHCP?':>6} {'LLA?':>5}"
    )

    for device_info in device_infos:
        friendly_name = f"{device_info.ModelName} ({device_info.SerialNumber})"
        mac_address = device_info.MacAddress
        ip_address = device_info.IpAddress if device_info.IsIpAddressAvailable() else "N/A"
        subnet_mask = device_info.SubnetMask if device_info.IsSubnetMaskAvailable() else "N/A"
        gateway = device_info.DefaultGateway if device_info.IsDefaultGatewayAvailable() else "N/A"
        mode = get_mode(device_info)

        supports_ip = int(device_info.IsPersistentIpSupported())
        supports_dhcp = int(device_info.IsDhcpSupported())
        supports_auto_ip = int(device_info.IsAutoIpSupported())

        print(
            f"{friendly_name:<32}  {mac_address:<12}  {ip_address:<15}  {subnet_mask:<15}  "
            f"{gateway:<15}  {mode:<7} {supports_ip:>3} {supports_dhcp:>6} {supports_auto_ip:>5}"
        )


def find_device_by_mac(device_infos, mac_address: str):
    normalized_mac_address = normalize_mac_address(mac_address)
    for device_info in device_infos:
        if normalize_mac_address(device_info.MacAddress) == normalized_mac_address:
            return device_info
    return None


def main() -> int:
    with pylon.TlFactory.GetInstance().TransportLayer(pylon.BaslerGigEDeviceClass) as gige_tl:
        if gige_tl is None:
            print("GigE transport layer not found. Please make sure the pylon GigE transport layer is installed.")
            input("Press enter to exit.")
            return 1

        device_infos = [info for info in gige_tl.EnumerateAllDevices() if info.DeviceClass == "BaslerGigE"]

        print_usage()
        print_available_devices(device_infos)
        print()

        if len(sys.argv) == 1:
            input("Press enter to exit.")
            return 0

        if len(sys.argv) not in (3, 4, 5):
            raise ValueError("Invalid number of arguments.")

        mac_address = sys.argv[1]
        requested_ip = sys.argv[2]
        subnet_mask = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_SUBNET_MASK
        gateway = sys.argv[4] if len(sys.argv) >= 5 else DEFAULT_GATEWAY

        selected_device_info = find_device_by_mac(device_infos, mac_address)
        if selected_device_info is None:
            raise RuntimeError(f"No device found for MAC address {mac_address}")

        # Extract user-defined name from device info.
        user_defined_name = selected_device_info.GetUserDefinedName()

        # Determine configuration mode.
        requested_mode = requested_ip.upper()
        is_auto = requested_mode == "AUTO"
        is_dhcp = requested_mode == "DHCP"
        is_static = not is_auto and not is_dhcp

        # Call BroadcastIpConfiguration via GigE transport layer.
        success = gige_tl.BroadcastIpConfiguration(
            mac_address,          # MAC address
            is_static,            # EnablePersistentIp
            is_dhcp,              # EnableDhcp
            requested_ip if is_static else "",  # IpAddress
            subnet_mask if is_static else "",   # SubnetMask
            gateway if is_static else "",       # DefaultGateway
            user_defined_name,    # UserdefinedName
        )

        if success:
            # Restart IP configuration to apply the new settings.
            gige_tl.RestartIpConfiguration(mac_address)
            print(f"Successfully changed IP configuration via broadcast for device {mac_address} to {requested_ip}")
        else:
            print(f"Failed to change IP configuration via broadcast for device {mac_address}")
            print("This is not an error. The device may not support broadcast IP configuration.")

        print()

    input("Press enter to exit.")
    return 0


exit_code = 0
try:
    exit_code = main()
except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)