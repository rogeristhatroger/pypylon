#!/usr/bin/env python3
"""\
This sample demonstrates the GigE transport layer methods AnnounceRemoteDevice
and RenounceRemoteDevice.

AnnounceRemoteDevice tells the GigE transport layer to contact a device at a
specific IP address, making it visible for enumeration even if it resides in a
different subnet. RenounceRemoteDevice reverses this operation.

The sample first locates a GigE camera via device enumeration, then uses its
IP address to demonstrate announce/renounce. It also attempts to announce a
non-existent address to show the failure case.

This sample requires a GigE camera connected to the network.
"""
import sys
from pypylon import pylon

NONEXISTENT_ADDRESS = "1.2.3.4"


def announce_renounce(gige_transport_layer, address):
    """Announce and then immediately renounce a remote device by IP address."""
    ok, device_info = gige_transport_layer.AnnounceRemoteDevice(address)
    print(f"Announce {address}: {'ok' if ok else 'failed'}")
    if ok:
        print(f"  Found: {device_info.FullName}")

    ok = gige_transport_layer.RenounceRemoteDevice(address)
    print(f"Renounce {address}: {'ok' if ok else 'failed'}")


exit_code = 0
try:
    tl_factory = pylon.TlFactory.GetInstance()

    # Find the first GigE device.
    camera_info = None
    for device_info in tl_factory.EnumerateDevices():
        if device_info.DeviceClass == "BaslerGigE":
            camera_info = device_info
            print(
                f"Using {camera_info.ModelName} @ {camera_info.IpAddress} "
                f"({camera_info.MacAddress})"
            )
            break

    if camera_info is None:
        raise EnvironmentError("No GigE device found.")

    with tl_factory.CreateTl("BaslerGigE") as gige_transport_layer:
        print(f"\nAnnounce/renounce known device at {camera_info.IpAddress}:")
        announce_renounce(gige_transport_layer, camera_info.IpAddress)

        print(f"\nAnnounce/renounce non-existent device at {NONEXISTENT_ADDRESS}:")
        announce_renounce(gige_transport_layer, NONEXISTENT_ADDRESS)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
