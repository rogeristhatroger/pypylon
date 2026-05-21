#!/usr/bin/env python3
"""\
Grab and process images using the InstantCamera grab loop thread.

This sample illustrates how to grab and process images using the grab loop thread
provided by the Instant Camera class.  
When run interactively (TTY detected) the user can trigger the camera by 
typing "t" and exit with "e". In non-interactive mode (CI, piped stdin, ``conda run``)
a fixed number of software triggers is issued automatically.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import os
import sys
import time

# Make the shared samples/include/ helpers importable.
_INCLUDE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "include")
)
if _INCLUDE_DIR not in sys.path:
    sys.path.insert(0, _INCLUDE_DIR)

from pypylon import pylon
from configuration_event_printer import ConfigurationEventPrinter
from image_event_printer import ImageEventPrinter

TRIGGER_READY_TIMEOUT_MS = 1000
EVENT_FLUSH_DELAY_MS = 250
CI_TRIGGER_COUNT = 5

exit_code = 0


# Example of an image event handler.
class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grab_result):
        print("SampleImageEventHandler.OnImageGrabbed called.")
        if grab_result.GrabSucceeded():
            print(f"SizeX: {grab_result.Width}; SizeY: {grab_result.Height}")
            pylon.DisplayImage(1, grab_result)
        else:
            print("Error:", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)
        print()


try:
    # Create an instant camera object. The device is attached later so that
    # configuration handlers can be registered before the camera is opened.
    with pylon.InstantCamera() as camera:

        # Register the standard configuration event handler for enabling software triggering.
        # The software trigger configuration handler replaces the default configuration
        # as all currently registered configuration handlers are removed by setting the
        # registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(
            pylon.SoftwareTriggerConfiguration(),
            pylon.RegistrationMode_ReplaceAll,
            pylon.Cleanup_Delete,
        )

        # For demonstration purposes only, registers an event handler configuration to
        # print out information about camera use. The event handler configuration is
        # appended to the registered software trigger configuration handler by setting
        # registration mode to RegistrationMode_Append.
        camera.RegisterConfiguration(
            ConfigurationEventPrinter(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )

        # The image event printer serves as sample image processing.
        # When using the grab loop thread provided by the Instant Camera object, an image
        # event handler processing the grab results must be created and registered.
        camera.RegisterImageEventHandler(
            ImageEventPrinter(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )

        # For demonstration purposes only, register another image event handler.
        camera.RegisterImageEventHandler(
            SampleImageEventHandler(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )

        # Attach the camera device found first.
        camera.Attach(pylon.FirstFound)

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        camera.Open()

        # Can the camera device be queried whether it is ready to accept the next
        # frame trigger?
        if not camera.CanWaitForFrameTriggerReady():
            print(
                "This sample can only be used with cameras that can be queried"
                " whether they are ready to accept the next frame trigger."
            )
            sys.exit(0)

        # Start the grabbing using the grab loop thread, by setting the grabLoopType
        # parameter to GrabLoop_ProvidedByInstantCamera. The grab results are delivered
        # to the image event handlers.
        # The GrabStrategy_OneByOne default grab strategy is used.
        camera.StartGrabbing(
            pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera
        )

        for _ in range(CI_TRIGGER_COUNT):
            if sys.stdin.isatty():
                user_input = input('\nPress ENTER to trigger the camera or Ctrl+C to exit')

            # Execute the software trigger. Wait up to 1000 ms for the camera to be
            # ready for trigger.
            if camera.WaitForFrameTriggerReady(
                TRIGGER_READY_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ):
                camera.ExecuteSoftwareTrigger()

            # Wait some time to allow the OnImageGrabbed handler print its output,
            # so the printed text on the console is in the expected order.
            time.sleep(EVENT_FLUSH_DELAY_MS / 1000.0)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
