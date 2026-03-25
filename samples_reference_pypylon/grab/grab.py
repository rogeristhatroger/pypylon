#!/usr/bin/env python3
"""\
This sample illustrates how to grab and process images using InstantCamera.

Images are grabbed and processed asynchronously: while the application handles
one buffer, acquisition of the next buffer can proceed in parallel.

InstantCamera uses a pool of buffers to retrieve image data from the device.
When a buffer is ready, you get a grab result; call Release() on it when
finished so the buffer can be reused.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to CreateFirstDevice: https://docs.baslerweb.com/camera-emulation
"""
import sys

from pypylon import pylon

# Number of images to be grabbed.
count_of_images_to_grab = 100

# The exit code of the sample application.
exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer.Value = 5

    # Start the grabbing of count_of_images_to_grab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(count_of_images_to_grab)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when count_of_images_to_grab images have been retrieved.
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        grab_result = camera.RetrieveResult(
            5000, pylon.TimeoutHandling_ThrowException
        )

        # Image grabbed successfully?
        if grab_result.GrabSucceeded():
            # Access the image data.
            print("SizeX: ", grab_result.Width)
            print("SizeY: ", grab_result.Height)
            img = grab_result.Array
            print("Gray value of first pixel: ", img[0, 0])
        else:
            print("Error: ", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

        grab_result.Release()
    camera.Close()

except BaseException as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
