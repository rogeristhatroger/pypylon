#!/usr/bin/env python3
"""\
Demonstrate user-managed buffers with pre-allocated NumPy arrays.

This sample demonstrates how to use a user-provided buffer factory.
Using a buffer factory is optional and intended for advanced use cases only.
A buffer factory is only necessary if you want to grab into externally
supplied buffers.

pypylon does not expose the IBufferFactory / SetBufferFactory API. This sample
documents that limitation and shows the closest workaround: pre-allocated NumPy
buffers that receive copied image data after each grab.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon
import numpy as np

COUNT_OF_IMAGES_TO_GRAB = 5
RETRIEVE_TIMEOUT_MS = 5000

exit_code = 0
try:
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = COUNT_OF_IMAGES_TO_GRAB

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        user_buffers = []

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                # Image grabbed successfully?
                if grab_result.GrabSucceeded():
                    # Access the image data.
                    image = grab_result.Array
                    # Copying into a new NumPy buffer.
                    user_buffer = np.empty(image.shape, dtype=image.dtype)
                    user_buffer[...] = image
                    user_buffers.append(user_buffer)

                    print(f"SizeX: {grab_result.Width}; SizeY: {grab_result.Height}; "
                        f"First value of pixel data: {int(user_buffer.flat[0])}")

                    pylon.DisplayImage(1, grab_result)
                else:
                    print("Error: ", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

        print("Allocated", len(user_buffers), "Python-managed buffers.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
