#!/usr/bin/env python3
"""\
Access interface-level parameters such as Power-over-CXP on a CXP-12 card.

The C++ pylon SDK provides CUniversalInstantInterface for convenient
access to interface parameters: you supply a CInterfaceInfo filter
(e.g. BaslerGenTlCxpDeviceClass) and the class finds, opens, and
exposes all GenICam nodes as named properties in one step.

In pypylon this wrapper is not yet available, so this sample performs
the equivalent steps manually:
  1. Enumerate transport layers and their interfaces.
  2. Filter by device class string to locate a CXP interface.
  3. Open the interface and obtain its raw GenICam node map.
  4. Access parameters via pylon.*Parameter wrappers.

Using the Basler CXP-12 interface card as an example, the sample shows how
to toggle Power-over-CXP and read current/voltage/power telemetry. The same
pattern works for any transport layer interface that exposes GenICam nodes.

This sample requires a CXP-12 interface card. If no CXP interface is found,
the sample prints a message and exits cleanly.

NOTE: pypylon does not currently expose CInstantInterface / CUniversalInstantInterface.
This is a known binding gap. This sample demonstrates the closest available
alternative using pylon.TlFactory interface enumeration.
"""
import sys
import time
from pypylon import pylon


def find_cxp_interface(tl_factory):
    """Locate a CXP transport layer and interface.

    Returns (transport_layer, interface_info) or None if no CXP
    interface is available. The caller takes ownership of the returned
    transport layer and must release it via tl_factory.ReleaseTl().
    Non-CXP transport layers are released during the search.
    """
    for tl_info in tl_factory.EnumerateTls():
        tl = tl_factory.CreateTl(tl_info)
        found = False
        try:
            for interface_info in tl.EnumerateInterfaces():
                device_class = getattr(interface_info, "DeviceClass", "")
                if "cxp" in device_class.lower():
                    found = True
                    return tl, interface_info
        finally:
            if not found:
                tl_factory.ReleaseTl(tl)
    return None


exit_code = 0
try:
    tl_factory = pylon.TlFactory.GetInstance()

    result = find_cxp_interface(tl_factory)
    if result is None:
        print("No CXP interface found. This sample requires a CXP-12 interface card.")
        sys.exit(1)

    tl, interface_info = result
    try:
        with tl.InterfaceNodeMap(interface_info) as nodemap:
            print("Interface opened.")

            external_power = pylon.BooleanParameter(nodemap, "ExternalPowerPresent")

            print(" ExternalPowerPresent:", end=" ")
            if external_power.IsReadable() and external_power.Value:
                print("yes")

                # Switch power OFF.
                print(" Switching power OFF.")
                pylon.CommandParameter(nodemap, "CxpPoCxpTurnOff").Execute()
                time.sleep(1.0)

                # Switch power ON.
                print(" Switching power ON.")
                pylon.CommandParameter(nodemap, "CxpPoCxpAuto").Execute()
                time.sleep(5.0)

                # Update device list.
                print(" Updating device list.")
                pylon.CommandParameter(nodemap, "DeviceUpdateList").Execute()

                # Read telemetry.
                current = pylon.FloatParameter(nodemap, "CxpPort0Current")
                voltage = pylon.FloatParameter(nodemap, "CxpPort0Voltage")
                power = pylon.FloatParameter(nodemap, "CxpPort0Power")

                print("  Port 0 :")
                if current.IsReadable():
                    print(f"   Current {current.Value:.2f} mA")
                if voltage.IsReadable():
                    print(f"   Voltage {voltage.Value:.2f} V")
                if power.IsReadable():
                    print(f"   Power {power.Value:.2f} W")
            else:
                print("no")
    finally:
        tl_factory.ReleaseTl(tl)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
