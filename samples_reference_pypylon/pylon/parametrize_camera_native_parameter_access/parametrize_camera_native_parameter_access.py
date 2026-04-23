#!/usr/bin/env python3
"""\
Configure a camera via the 'native' parameter access approach.

The pypylon InstantCamera and its node maps expose a list of known
parameters that can always be accessed as properties. Parameters that are
not implemented by a device are not readable, not writable, and not valid,
so Try* or *OrDefault methods can handle optional availability in a single
line of code.

See also the parametrize_camera_generic_parameter_access sample for the
'generic' approach to configuring a camera.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""

import sys
from pypylon import pylon

exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        # Print the model name of the camera.
        print("Using device:", camera.DeviceInfo.ModelName)

        # Get camera device information.
        print("Camera Device Information")
        print("=========================")
        print("Vendor           : ", camera.DeviceVendorName.Value)
        print("Model            : ", camera.DeviceModelName.Value)
        print("Firmware version : ", camera.DeviceFirmwareVersion.Value)
        print()

        # Camera settings.
        print("Camera Device Settings")
        print("======================")

        # Set the AOI:

        # On some cameras, the offsets are read-only.
        # Therefore, we must use "Try" functions that only perform the action
        # when parameters are writable. Otherwise, we would get an exception.
        camera.OffsetX.TrySetToMinimum()
        camera.OffsetY.TrySetToMinimum()

        # Some properties have restrictions.
        # We use API functions that automatically perform value corrections.
        # Alternatively, you can use .Inc / .Min / .Max to make sure you set a valid value.
        camera.Width.SetValue(202, pylon.IntegerValueCorrection_Nearest)
        camera.Height.SetValue(101, pylon.IntegerValueCorrection_Nearest)

        print("OffsetX          : ", camera.OffsetX.Value)
        print("OffsetY          : ", camera.OffsetY.Value)
        print("Width            : ", camera.Width.Value)
        print("Height           : ", camera.Height.Value)

        # Remember the current pixel format.
        old_pixel_format = camera.PixelFormat.Value
        print("Old PixelFormat  : ", old_pixel_format)

        # Set pixel format to Mono8 if available.
        # camera.PixelFormat.GetAllValues() returns all possible values for this camera.
        if camera.PixelFormat.TrySetValue("Mono8"):
            print("New PixelFormat  : ", camera.PixelFormat.Value)

            # Set the new gain to 50% ->  Min + ((Max-Min) / 2).
            #
            # Note: Some newer camera models may have auto functions enabled.
            #       To be able to set the gain value to a specific value
            #       the Gain Auto function must be disabled first.
            # Access the enumeration type node GainAuto.
            # We use a "Try" function that only performs the action if the parameter is writable.
            camera.GainAuto.TrySetValue("Off")

            # Cameras based on SFNC 2.0 or later, e.g. USB cameras.
            if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
                if camera.Gain.TrySetValuePercentOfRange(50.0):
                    print("Gain (50%)       : ", camera.Gain.Value,
                          " (Min: ", camera.Gain.Min,
                          "; Max: ", camera.Gain.Max,
                          ")")
                else:
                    if camera.GainRaw.TrySetValuePercentOfRange(50.0):
                        print("Gain (50%)       : ", camera.GainRaw.Value,
                              " (Min: ", camera.GainRaw.Min,
                              "; Max: ", camera.GainRaw.Max,
                              "; Inc: ", camera.GainRaw.Inc,
                              ")")

        # Restore the old pixel format.
        camera.PixelFormat.Value = old_pixel_format

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
