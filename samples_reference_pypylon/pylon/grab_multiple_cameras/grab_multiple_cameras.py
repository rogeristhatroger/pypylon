#!/usr/bin/env python3
"""\
Grab and process images from multiple cameras using InstantCameraArray.

InstantCameraArray holds several InstantCamera instances and exposes a single
RetrieveResult for all of them in one thread. Each grab result carries a camera
context (index in the array) so you know which device produced the image.

Without hardware, configure Basler Camera Emulation. To use two virtual devices
with the default MAX_CAMERAS_TO_USE, set environment variable PYLON_CAMEMU to at
least 2 before starting Python (the transport layer reads it at init):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 100

# Limits the amount of cameras used for grabbing.
# It is important to manage the available bandwidth when grabbing with multiple cameras.
# This applies, for instance, if two GigE cameras are connected to the same network adapter via a switch.
# To manage the bandwidth, the GevSCPD interpacket delay parameter and the GevSCFTD transmission delay
# parameter can be set for each GigE camera device.
# The "Controlling Packet Transmission Timing with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
# Application Notes (AW000649xx000)
# provide more information about this topic.
# The bandwidth used by a GigE camera device can be limited by adjusting the packet size.
MAX_CAMERAS_TO_USE = 2

RETRIEVE_TIMEOUT_MS = 5000

exit_code = 0

try:
    tl_factory = pylon.TlFactory.GetInstance()

    devices = tl_factory.EnumerateDevices()
    if len(devices) < MAX_CAMERAS_TO_USE:
        raise pylon.RuntimeException(
            f"This sample needs at least {MAX_CAMERAS_TO_USE} camera(s); "
            f"enumerated {len(devices)}. Add devices or configure Basler Camera "
            "Emulation (virtual devices) - e.g. set PYLON_CAMEMU before starting Python; see "
            "https://docs.baslerweb.com/camera-emulation"
        )

    with pylon.InstantCameraArray(MAX_CAMERAS_TO_USE) as cameras:
        for i, cam in enumerate(cameras):
            cam.Attach(tl_factory.CreateDevice(devices[i]))
            print("Using device:", cam.DeviceInfo.ModelName)

        print()

        # Starts grabbing for all cameras starting with index 0. The grabbing
        # is started for one camera after the other. That's why the images of all
        # cameras are not taken at the same time.
        # However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
        # According to their default configuration, the cameras are
        # set up for free-running continuous acquisition.
        cameras.StartGrabbing()

        for iteration in range(COUNT_OF_IMAGES_TO_GRAB):
            print("Grabbing result...", iteration)
            if not cameras.IsGrabbing():
                break

            with cameras.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                if grab_result.GrabSucceeded():
                    # Camera context is set to the index of the camera in the array.
                    camera_context_value = grab_result.GetCameraContext()

                    pylon.DisplayImage(camera_context_value, grab_result)

                    print(f"Camera {camera_context_value}: "
                        f"{cameras[camera_context_value].DeviceInfo.ModelName}")

                    img = grab_result.Array
                    print(
                        f"GrabSucceeded: {grab_result.GrabSucceeded()} "
                        f"SizeX: {grab_result.Width} SizeY: {grab_result.Height} "
                        f"Gray value of first pixel: {img[0, 0]}\n"
                    )
                else:
                    print("Error:", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
