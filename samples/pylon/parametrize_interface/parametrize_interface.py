#!/usr/bin/env python3
"""\
Access interface-level parameters such as Power-over-CXP on a CXP-12 card.

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

exit_code = 0
transport_layer = None
try:
    transport_layer = pylon.TlFactory.GetInstance().CreateTl(pylon.BaslerGenTlCxpDeviceClass)
    if transport_layer is None:
        print("No CXP GenTL producer found. This sample requires a CXP-12 interface card.")
        sys.exit(1)

    interface_list = transport_layer.EnumerateInterfaces()
    if len(interface_list) == 0:
        print("No CXP interface found. This sample requires a CXP-12 interface card.")
        sys.exit(1)

    with transport_layer.InterfaceNodeMap(interface_list[0]) as nodemap:
        print("Interface opened.")

        print(" ExternalPowerPresent:", end=" ")
        if  nodemap.ExternalPowerPresent.IsReadable() and nodemap.ExternalPowerPresent.Value:
            print("yes")

            # Switch power OFF.
            print(" Switching power OFF.")
            nodemap.CxpPoCxpTurnOff.Execute()
            time.sleep(1.0)

            # Switch power ON.
            print(" Switching power ON.")
            nodemap.CxpPoCxpAuto.Execute()
            time.sleep(5.0)

            # Update device list.
            print(" Updating device list.")
            nodemap.DeviceUpdateList.Execute()

            # Read telemetry.
            current = nodemap.CxpPort0Current
            voltage = nodemap.CxpPort0Voltage
            power = nodemap.CxpPort0Power

            print("  Port 0 :")
            if current.IsReadable():
                print(f"   Current {current.Value:.2f} mA")
            if voltage.IsReadable():
                print(f"   Voltage {voltage.Value:.2f} V")
            if power.IsReadable():
                print(f"   Power {power.Value:.2f} W")
        else:
            print("no")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1
finally:
    pylon.TlFactory.GetInstance().ReleaseTl(transport_layer)

sys.exit(exit_code)
