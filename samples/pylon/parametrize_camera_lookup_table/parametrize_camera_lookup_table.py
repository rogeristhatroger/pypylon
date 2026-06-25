#!/usr/bin/env python3
"""\
Demonstrate the use of the Luminance Lookup Table feature.

This sample shows how to enable and configure the camera's luminance lookup
table (LUT). The LUT maps input pixel values to output pixel values and can
be used for operations like contrast enhancement or value inversion.

In this example an inversion LUT is written: The brightest input value is
mapped to 0 and the darkest to the maximum, effectively creating a negative
of the captured image. The LUT is enabled, a few frames are grabbed to show
the effect, and then the LUT is disabled again.

Note: Not all camera models support the LUT feature. Cameras that lack
LUTSelector, LUTIndex, or LUTValue nodes will cause this sample to print
a message and exit cleanly.
"""
import sys
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 50

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        if not camera.LUTSelector.IsWritable():
            print("The LUT feature is not available for this camera.")
            sys.exit(0)

        print("Writing LUT...")

        # Select the luminance lookup table.
        camera.LUTSelector.Value = "Luminance"

        # Determine the LUT size. Some cameras have 10-bit (1024 entries)
        # and others have 12-bit (4096 entries) lookup tables.
        num_values = camera.LUTIndex.Max + 1
        if num_values == 4096:
            inc = 8
        elif num_values == 1024:
            inc = 2
        else:
            raise pylon.RuntimeException(
                f"LUT size {num_values} is not supported by this sample."
            )

        # Write an inversion LUT: map each input value to (max - input).
        for i in range(0, num_values, inc):
            camera.LUTIndex.Value = i
            camera.LUTValue.Value = num_values - 1 - i

        print("done")

        # Enable the lookup table.
        camera.LUTEnable.Value = True
        print("LUT enabled — grabbing inverted images.")

        # Grab a few frames to demonstrate the effect.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)
        while camera.IsGrabbing():
            with camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                if grab_result.GrabSucceeded():
                    # Some camera models use a GenICam Generic Data Container (GenDC) format.
                    # For single grabbed images, a data component is emulated automatically.
                    # pylon provides a data component wrapper to handle both cases uniformly.
                    with grab_result.GetFirstImageDataComponent() as image_data_component:
                        img = image_data_component.Array
                        print(
                            f"SizeX: {image_data_component.Width}; SizeY: {image_data_component.Height}; "
                            f"Gray value of first pixel: {img[0, 0]}"
                        )
                        pylon.DisplayImage(1, image_data_component)
                else:
                    print("Error:", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

        # Disable the lookup table.
        camera.LUTEnable.Value = False
        print("LUT disabled.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
