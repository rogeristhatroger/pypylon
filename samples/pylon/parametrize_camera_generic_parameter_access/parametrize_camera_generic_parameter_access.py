#!/usr/bin/env python3
"""\
Demonstrate generic node-map based camera parameter access using pylon parameter wrappers.

For camera configuration and for accessing other parameters, the pylon API
uses the technologies defined by the GenICam standard. The GenICam specification
defines a format for camera description files. These files describe the
configuration interface of GenICam compliant cameras. The elements of a camera
description file are represented as software objects called Nodes. The complete
set of nodes is stored in a data structure called Node Map.

This sample shows the 'generic' approach for configuring a camera using the
node map. Nodes are wrapped in pylon parameter objects (IntegerParameter,
FloatParameter, EnumParameter) to use the convenience API: print device
information, adjust AOI, switch pixel format to Mono8 when possible, set gain
to 50 % of range, and restore the original pixel format.

See also the parametrize_camera_native_parameter_access sample for the 'native'
approach for configuring a camera.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        nodemap = camera.NodeMap

        # Get camera device information.
        print("Camera Device Information")
        print("=========================")
        print("Vendor           :", pylon.StringParameter(nodemap, "DeviceVendorName").Value)
        print("Model            :", pylon.StringParameter(nodemap, "DeviceModelName").Value)
        print("Firmware version :", pylon.StringParameter(nodemap, "DeviceFirmwareVersion").Value)
        print()

        # Camera settings.
        print("Camera Device Settings")
        print("======================")

        # Set the AOI:

        # Get the integer nodes describing the AOI.
        offset_x = pylon.IntegerParameter(nodemap, "OffsetX")
        offset_y = pylon.IntegerParameter(nodemap, "OffsetY")
        width = pylon.IntegerParameter(nodemap, "Width")
        height = pylon.IntegerParameter(nodemap, "Height")

        # On some cameras, the offsets are read-only.
        # Therefore, we must use "Try" functions that only perform the action
        # when parameters are writable. Otherwise, we would get an exception.
        offset_x.TrySetToMinimum()
        offset_y.TrySetToMinimum()

        # Some properties have restrictions.
        # We use API functions that automatically perform value corrections.
        # Alternatively, you can use the Inc / Min / Max properties to make sure
        # you set a valid value.
        width.SetValue(202, pylon.IntegerValueCorrection_Nearest)
        height.SetValue(101, pylon.IntegerValueCorrection_Nearest)

        print("OffsetX          :", offset_x.Value)
        print("OffsetY          :", offset_y.Value)
        print("Width            :", width.Value)
        print("Height           :", height.Value)

        # Access the PixelFormat enumeration type node.
        pixel_format = pylon.EnumParameter(nodemap, "PixelFormat")

        # Remember the current pixel format.
        old_pixel_format = pixel_format.Value
        print("Old PixelFormat  :", old_pixel_format)

        # Set the pixel format to Mono8 if available.
        if pixel_format.TrySetValue("Mono8"):
            print("New PixelFormat  :", pixel_format.Value)

        # Set the new gain to 50% ->  Min + ((Max-Min) / 2).
        #
        # Note: Some newer camera models may have auto functions enabled.
        #       To be able to set the gain value to a specific value
        #       the Gain Auto function must be disabled first.
        # Access the enumeration type node GainAuto.
        # We use a "Try" function that only performs the action if the parameter
        # is writable.
        gain_auto = pylon.EnumParameter(nodemap, "GainAuto")
        gain_auto.TrySetValue("Off")

        # Check to see which Standard Feature Naming Convention (SFNC) is used by
        # the camera device.
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # Access the Gain float type node. This node is available for USB camera
            # devices. USB camera devices are compliant to SFNC version 2.0.
            gain = pylon.FloatParameter(nodemap, "Gain")
            if gain.TrySetValuePercentOfRange(50.0):
                print(
                    "Gain (50%)       :",
                    gain.Value,
                    f"(Min: {gain.Min}; Max: {gain.Max})"
                )
        else:
            # Access the GainRaw integer type node. This node is available for GigE
            # camera devices.
            gain_raw = pylon.IntegerParameter(nodemap, "GainRaw")
            if gain_raw.TrySetValuePercentOfRange(50.0):
                print(
                    "Gain (50%)       :",
                    gain_raw.Value,
                    f"(Min: {gain_raw.Min}; Max: {gain_raw.Max}; Inc: {gain_raw.Inc})"
                )

        # Restore the old pixel format.
        pixel_format.SetValue(old_pixel_format)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
