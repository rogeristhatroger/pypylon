#!/usr/bin/env python3
"""\
This sample illustrates how to grab and process images using InstantCamera.

Images are grabbed and processed asynchronously: while the application handles
one buffer, acquisition of the next buffer can proceed in parallel.

InstantCamera uses a pool of buffers to retrieve image data from the device.
When a buffer is ready, you get a grab result. Use a context manager (with
statement) to ensure it is released automatically so the buffer can be reused.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 100

# The exit code of the sample application.
exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        # Print the model name of the camera.
        print("Using device:", camera.DeviceInfo.ModelName)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 5

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            with camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                # Image grabbed successfully?
                if grab_result.GrabSucceeded():
                    # Access the image data.
                    img = grab_result.Array
                    print(f"SizeX: {grab_result.Width}; SizeY: {grab_result.Height}; "
                        f"Gray value of first pixel: {img[0, 0]}")

                    pylon.DisplayImage(1, grab_result)
                else:
                    print("Error: ", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
