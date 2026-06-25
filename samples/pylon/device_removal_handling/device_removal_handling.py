#!/usr/bin/env python3
"""\
Demonstrate how to detect camera device removal and reconnect to the device.

This sample shows how to register a configuration event handler that is notified
when a camera device is physically removed. It also demonstrates how to wait for
the same device to reappear and reattach the instant camera object.

Attention: If you run this using a GigE camera device in debug mode, pylon will
set the heartbeat timeout to 5 minutes. This would cause a long delay before
the application detects a disconnect. As a workaround, the heartbeat timeout is
explicitly set to 1000 ms in this sample.

Note: The core device-removal and reconnection behavior requires physical
hardware — it cannot be fully exercised under Basler Camera Emulation.
"""
import sys
import time
from pypylon import pylon

# Timeout in seconds for waiting for device removal / reconnection.
WAIT_TIMEOUT_S = 60

# Interval in seconds between polling iterations.
POLL_INTERVAL_S = 0.25

# Heartbeat timeout in milliseconds (short value, so GigE removal is detected quickly).
HEARTBEAT_TIMEOUT_MS = 1000


# When using device-specific instant camera classes, there are specific
# configuration event handler classes available.
class SampleConfigurationEventHandler(pylon.ConfigurationEventHandler):
    """Configuration event handler that reports camera device removal."""

    # This method is called from a different thread when the camera device
    # removal has been detected.
    def OnCameraDeviceRemoved(self, camera):
        print()
        print()
        print("SampleConfigurationEventHandler.OnCameraDeviceRemoved called.")


exit_code = 0

try:
    tl_factory = pylon.TlFactory.GetInstance()

    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:

        print("Using device :", camera.DeviceInfo.ModelName)
        print("Friendly Name:", camera.DeviceInfo.FriendlyName)
        print("Full Name    :", camera.DeviceInfo.FullName)
        print("SerialNumber :", camera.DeviceInfo.SerialNumber)
        print()

        # For demonstration purposes only, register a configuration event
        # handler that handles device removal. This is the cleanest way
        # of detecting a device removal.
        camera.RegisterConfiguration(
            SampleConfigurationEventHandler(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete
        )

        # Now, try to detect that the camera has been removed:

        total_polls = int(WAIT_TIMEOUT_S / POLL_INTERVAL_S)
        print(f"Please disconnect the device (timeout {WAIT_TIMEOUT_S}s)")

        ########################################### don't single step beyond this line

        # Before testing the callbacks, we manually set the heartbeat timeout
        # to a short value when using GigE cameras. Since for debug versions
        # the heartbeat timeout has been set to 5 minutes, it would take up to
        # 5 minutes until detection of the device removal.
        heartbeat = camera.TLNodeMap.HeartbeatTimeout.TrySetValue(
            HEARTBEAT_TIMEOUT_MS, pylon.IntegerValueCorrection_Nearest
        )

        try:
            # The following loop shows another way of how to detect a device
            # removal by accessing the camera. It could also be a loop
            # that is grabbing images. The device removal is handled in the
            # exception handler.
            for i in range(total_polls, 0, -1):
                # Print a "." every few seconds to tell the user we're waiting
                # for the callback.
                if i % 4 == 0:
                    print(".", end="", flush=True)
                time.sleep(POLL_INTERVAL_S)

                # Change the width value in the camera depending on the loop
                # counter. Any access to the camera like setting parameters or
                # grabbing images will fail throwing an exception if the camera
                # has been disconnected.
                camera.Width.SetValue(
                    camera.Width.Max - (camera.Width.Inc * (i % 2))
                )

        except Exception:
            # An exception occurred. Is it because the camera device has been
            # physically removed?

            # Known issue: Wait until the system safely detects a possible
            # removal.
            time.sleep(1.0)

            if camera.IsCameraDeviceRemoved():
                # The camera device has been removed. This caused the exception.
                print()
                print("The camera has been removed from the computer.")
            else:
                # An unexpected error has occurred.
                raise

        if not camera.IsCameraDeviceRemoved():
            print()
            print("Timeout expired")

        ############################################ Safe to use single stepping

        # Now try to find the detached camera after it has been attached again:

        # Create a device info object for remembering the camera properties
        # that allow detecting the same camera again.
        info = pylon.DeviceInfo()
        info.DeviceClass = camera.DeviceInfo.DeviceClass
        info.SerialNumber = camera.DeviceInfo.SerialNumber

        # Destroy the Pylon Device representing the detached camera device.
        # It can't be used anymore.
        camera.DestroyDevice()

        total_polls = int(WAIT_TIMEOUT_S / POLL_INTERVAL_S)
        print()
        print(f"Please connect the same device to the computer again "
              f"(timeout {WAIT_TIMEOUT_S}s)")

        # Create a filter containing the DeviceInfo object which describes
        # the properties of the device we are looking for.
        device_filter = [info]

        for i in range(total_polls, 0, -1):
            # Print a "." every few seconds to tell the user we're waiting for
            # the camera to be attached.
            if i % 4 == 0:
                print(".", end="", flush=True)

            # Try to find the camera we are looking for with filter.
            devices = tl_factory.EnumerateDevices(device_filter)

            if devices:
                print()

                # The camera has been found. Create and attach it to the
                # Instant Camera object.
                camera.Attach(devices[0], pylon.FirstFound)
                
                break

            time.sleep(POLL_INTERVAL_S)

        # If the camera has been found.
        if camera.IsPylonDeviceAttached():
            print()
            print("Using device :", camera.DeviceInfo.ModelName)
            print("Friendly Name:", camera.DeviceInfo.FriendlyName)
            print("Full Name    :", camera.DeviceInfo.FullName)
            print("SerialNumber :", camera.DeviceInfo.SerialNumber)
            print()

            # All configuration objects and other event handler objects are
            # still registered. The configuration objects will parameterize the
            # camera device and the instant camera will be ready for operation
            # again.
            camera.Open()

            # Now the Instant Camera object can be used as before.
        else:
            print()
            print("Timeout expired.")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
