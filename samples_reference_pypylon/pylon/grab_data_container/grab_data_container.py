#!/usr/bin/env python3
"""\
This sample illustrates how to grab and process data containers using
InstantCamera and the GenDC (Generic Data Container) API.

A data container holds one or more data components. For 3D cameras such as
Basler blaze, a single grab result can deliver range, intensity, and
confidence data as separate components. This sample grabs results, extracts
the data container from each, and prints metadata for every intensity
component found.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

COUNT_OF_RESULTS_TO_GRAB = 100
TIMEOUT_MS = 5000

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)

        # Demonstrate some feature access.
        new_width = camera.Width.Value - camera.Width.Inc
        if new_width >= camera.Width.Min:
            camera.Width.Value = new_width

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 5

        # Start grabbing. The camera device is parameterized with a default
        # configuration which sets up free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_RESULTS_TO_GRAB)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult()
        # method when COUNT_OF_RESULTS_TO_GRAB results have been retrieved.
        while camera.IsGrabbing():
            with camera.RetrieveResult(
                TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                if grab_result.GrabSucceeded():
                    # Get the grab result as a data container, e.g. when
                    # working with 3D cameras.
                    pylon_data_container = grab_result.DataContainer
                    print("Component count:", pylon_data_container.DataComponentCount)

                    for component_index in range(pylon_data_container.DataComponentCount):
                        with pylon_data_container.GetDataComponentByIndex(
                            component_index
                        ) as component:
                            print(f"Component {component_index}")
                            print(f"  ComponentType : {component.ComponentType}")
                            print(f"  PixelType     : {component.PixelType}")
                            print(f"  SizeX         : {component.Width}")
                            print(f"  SizeY         : {component.Height}")
                            print(f"  OffsetX       : {component.OffsetX}")
                            print(f"  OffsetY       : {component.OffsetY}")
                            print(f"  PaddingX      : {component.PaddingX}")
                            print(f"  DataSize      : {component.DataSize}")
                            print(f"  TimeStamp     : {component.TimeStamp}")
                            print(f"  First pixel   : {component.Array[0, 0]}")
                            print()

                    pylon_data_container.Release()
                else:
                    print("Error:", f"{grab_result.ErrorCode:#x}",
                          grab_result.ErrorDescription)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
