#!/usr/bin/env python3
"""\
Grab and process images using the SmartInstantCamera class.

SmartInstantCamera provides convenient access to a camera device together
with pylon data processing, using a recipe as an appended processing stage.
It extends the InstantCamera class.

Each RetrieveResult() call returns a SmartInstantCameraResult that contains
both the raw grab result and the recipe output container (a dict of Variant
objects keyed by output pin name). For the current recipe, the outputs are
the pins "Barcodes" and "DataMatrixCodes".

Without hardware, configure Basler Camera Emulation:
https://docs.baslerweb.com/camera-emulation
"""
import os
import sys
from pypylon import pylon
from pypylon import pylondataprocessing

COUNT_OF_IMAGES_TO_GRAB = 100


def print_variant_item(data_type, item, index=None):
    """Print a single variant value, with optional array index prefix."""
    prefix = f"      [{index}] " if index is not None else "    "
    if data_type == pylondataprocessing.VariantDataType_Region:
        print(f"{prefix}Region with {item.DataSize} bytes")
    elif data_type == pylondataprocessing.VariantDataType_PylonImage:
        print(f"{prefix}Image {item.Width}x{item.Height}")
    else:
        print(f"{prefix}Data: {item}")


exit_code = 0
try:
    this_dir = os.path.dirname(__file__)
    recipe_file = os.path.join(this_dir, "smartcamera.precipe")

    with pylondataprocessing.SmartInstantCamera(
        pylon.TlFactory.GetInstance().CreateFirstDevice(), recipe_file
    ) as camera:
        print("Using device", camera.DeviceInfo.ModelName)

        # Demonstrate feature access: reduce width by one increment.
        new_width = camera.Width.Value - camera.Width.Inc
        if new_width >= camera.Width.Min:
            camera.Width.Value = new_width

        camera.MaxNumBuffer.Value = 5

        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        while camera.IsGrabbing():
            result = camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            )

            if result.GrabResult.GrabSucceeded():
                img = result.GrabResult.Array
                print(
                    f"SizeX: {result.GrabResult.Width}; "
                    f"SizeY: {result.GrabResult.Height}; "
                    f"Gray value of first pixel: {img[0, 0]}"
                )

                pylon.DisplayImage(1, result.GrabResult)

                # Iterate over all recipe output pins.
                print("Processing recipe outputs:")
                for key, variant in result.Container.items():
                    print(f"  Output pin '{key}':")
                    if not variant.HasError():
                        if variant.IsArray():
                            data_array = variant.ToData()
                            print(f"    Array with {len(data_array)} items:")
                            for i, item in enumerate(data_array):
                                print_variant_item(
                                    variant.DataType, item, i
                                )
                        else:
                            data = variant.ToData()
                            print_variant_item(variant.DataType, data)
                    else:
                        print(f"    Error: {variant.ErrorDescription}")
            else:
                print(
                    "Error:",
                    f"{result.GrabResult.ErrorCode:#x}",
                    result.GrabResult.ErrorDescription,
                )

            result.Release()

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
