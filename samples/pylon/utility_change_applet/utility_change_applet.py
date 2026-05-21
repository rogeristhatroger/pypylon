#!/usr/bin/env python3
"""\
Change the active applet on a Basler CXP frame grabber.

This sample shows two different methods for changing an applet on a
Basler CXP frame grabber. An applet reconfigures the on-board logic,
e.g., switching from a monochrome stream to a Bayer-demosaicing
pipeline. It only becomes active after all devices using the applet
have been closed and the hardware has been enumerated again.

This sample requires a CXP-12 interface card. If no CXP interface is
found, the sample prints a message and exits cleanly.

NOTE: pypylon does not currently expose CInstantInterface /
CUniversalInstantInterface. This sample uses pylon.TlFactory interface
enumeration as a workaround.
"""
import sys
from pypylon import pylon


def find_cxp_interface(tl_factory):
    """Locate a CXP transport layer and interface.

    Returns (transport_layer, interface_info) or None if no CXP
    interface is available. The caller takes ownership of the returned
    transport layer and must release it via tl_factory.ReleaseTl().
    Non-CXP transport layers are released during the search.
    """
    for tl_info in tl_factory.EnumerateTls():
        if tl_info.TLType == "CXP" and tl_info.VendorName == "Basler":
            tl = tl_factory.CreateTl(tl_info)
            interface_info_list = tl.EnumerateInterfaces()
            if len(interface_info_list) > 0:
                return tl, interface_info_list[0]
            else:
                tl_factory.ReleaseTl(tl)
    return None


def print_applets(applet_entries):
    """Print all applets available on the interface."""
    print("-  Available applets:")
    for entry in applet_entries:
        print(f"  {entry}")


def select_first_different_applet(applet_node, applet_entries, current_applet):
    """Select the first applet that differs from *current_applet*."""
    for entry in applet_entries:
        if entry != current_applet:
            print(f"- Requesting switch to: {entry}")
            applet_node.Value = entry
            break


exit_code = 0
try:
    tl_factory = pylon.TlFactory.GetInstance()

    # Verify the required hardware is connected before doing anything else.
    result = find_cxp_interface(tl_factory)
    if result is None:
        print("No CXP interface found. This sample requires a CXP-12 interface card.")
        sys.exit(1)

    # ======================================================
    # First method for changing an applet:
    #     - Load a different applet.
    #     - Close devices and update the device list.
    # ======================================================
    print("First method for changing an applet")

    tl, interface_info = result
    try:
        with tl.InterfaceNodeMap(interface_info) as nodemap:
            print("Interface opened.")

            # List the available applets.
            applet_entries = nodemap.InterfaceApplet.GetSettableValues()
            print_applets(applet_entries)

            current_applet = nodemap.InterfaceApplet.Value
            print(f"- Current applet: {current_applet}")

            # Report the status.
            print(f"- Applet status: {nodemap.InterfaceAppletStatus.Value}")

            # Select the first different applet.
            select_first_different_applet(
                nodemap.InterfaceApplet, applet_entries, current_applet
            )

            # Update device list.
            print("Update device list with all the devices closed so that the applet change takes effect.")
            nodemap.DeviceUpdateList.Execute()

            # Report the new status.
            print(f"- Applet status: {nodemap.InterfaceAppletStatus.Value}")
            print()
    finally:
        tl_factory.ReleaseTl(tl)

    # ======================================================
    # Second method for changing an applet:
    #     - Load a different applet.
    #     - Close everything and reopen it again.
    # ======================================================
    print("Second method for changing an applet.")

    result = find_cxp_interface(tl_factory)
    tl, interface_info = result
    try:
        with tl.InterfaceNodeMap(interface_info) as nodemap:
            print("Interface opened.")

            # List the available applets.
            applet_entries = nodemap.InterfaceApplet.GetSettableValues()

            current_applet = nodemap.InterfaceApplet.Value
            print(f"- Current applet: {current_applet}")

            # Report the status.
            print(f"- Applet status: {nodemap.InterfaceAppletStatus.Value}")

            # Select the first different applet.
            select_first_different_applet(
                nodemap.InterfaceApplet, applet_entries, current_applet
            )
    finally:
        tl_factory.ReleaseTl(tl)

    print("- Closed pylon libraries")
    print("- Reopening pylon libraries again")

    result = find_cxp_interface(tl_factory)
    tl, interface_info = result
    try:
        with tl.InterfaceNodeMap(interface_info) as nodemap:
            print("Interface opened.")

            # List the available applets.
            applet_entries = nodemap.InterfaceApplet.GetSettableValues()

            current_applet = nodemap.InterfaceApplet.Value
            print(f"- Current applet: {current_applet}")
            print(f"- Applet status: {nodemap.InterfaceAppletStatus.Value}")
    finally:
        tl_factory.ReleaseTl(tl)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
