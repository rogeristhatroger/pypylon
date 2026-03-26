#!/usr/bin/env python3
"""\
Demonstrate InstantCamera grab strategies: OneByOne, LatestImageOnly, LatestImages,
and (non-USB only) UpcomingImage.

The grab engine can queue buffers in different ways: strict ordering, only the latest
image, a bounded queue of recent images, or “next upcoming” image per RetrieveResult.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to CreateFirstDevice: https://docs.baslerweb.com/camera-emulation
"""

import os
import sys
import time

# Repo root on path so we can use the same demo handlers as samples/grabstrategies.py
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from pypylon import pylon
from samples.configurationeventprinter import ConfigurationEventPrinter
from samples.imageeventprinter import ImageEventPrinter

# Timeouts and sleeps (milliseconds)
FRAME_TRIGGER_READY_TIMEOUT_MS = 1000
POST_TRIGGER_SLEEP_MS = 3 * 1000 
UPCOMING_RETRIEVE_TIMEOUT_MS = 5000
UPCOMING_POST_RETRIEVE_SLEEP_MS = 1000

# Printed before each strategy block.
STRATEGY_SECTION_RULE = "-" * 56

# The exit code of the sample application.
exit_code = 0

try:
    # Create an instant camera object for the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Register the standard configuration event handler for enabling software triggering.
    # The software trigger configuration handler replaces the default configuration
    # as all currently registered configuration handlers are removed by setting the
    # registration mode to RegistrationMode_ReplaceAll.
    camera.RegisterConfiguration(
        pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
        pylon.Cleanup_Delete)

    # For demonstration purposes only, add sample configuration event handlers to print out information
    # about camera use and image grabbing.
    camera.RegisterConfiguration(
        ConfigurationEventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)
    camera.RegisterImageEventHandler(
        ImageEventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer.Value = 15

    # Open the camera.
    camera.Open()

    print(STRATEGY_SECTION_RULE)
    print("Grab using the GrabStrategy_OneByOne default strategy:")

    # The GrabStrategy_OneByOne strategy is used. The images are processed
    # in the order of their arrival.
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    # In the background, the grab engine thread retrieves the
    # image data and queues the buffers into the internal output queue.

    # Issue software triggers. For each call, wait up to FRAME_TRIGGER_READY_TIMEOUT_MS
    # until the camera is ready for triggering the next image.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(
                FRAME_TRIGGER_READY_TIMEOUT_MS,
                pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()

    # For demonstration purposes, wait for the last image to appear in the output queue.
    time.sleep(POST_TRIGGER_SLEEP_MS / 1000.0)

    # Check that grab results are waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("Grab results wait in the output queue.")

    # All triggered images are still waiting in the output queue
    # and are now retrieved.
    # The grabbing continues in the background, e.g. when using hardware trigger mode,
    # as long as the grab engine does not run out of buffers.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        buffers_in_queue += 1
        grab_result.Release()

    print("Retrieved ", buffers_in_queue, " grab results from output queue.")

    # Stop the grabbing.
    camera.StopGrabbing()

    print(STRATEGY_SECTION_RULE)
    print("Grab using strategy GrabStrategy_LatestImageOnly:")

    # The GrabStrategy_LatestImageOnly strategy is used. The images are processed
    # in the order of their arrival but only the last received image
    # is kept in the output queue.
    # This strategy can be useful when the acquired images are only displayed on the screen.
    # If the processor has been busy for a while and images could not be displayed automatically
    # the latest image is displayed when processing time is available again.
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Execute the software trigger, wait actively until the camera accepts the next
    # frame trigger or until the timeout occurs.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(
                FRAME_TRIGGER_READY_TIMEOUT_MS,
                pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()

    # Wait for all images.
    time.sleep(POST_TRIGGER_SLEEP_MS / 1000.0)

    # Check whether the grab result is waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("A grab result waits in the output queue.")

    # Only the last received image is waiting in the internal output queue
    # and is now retrieved.
    # The grabbing continues in the background, e.g. when using hardware trigger mode.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        print("Skipped ", grab_result.NumberOfSkippedImages, " images.")
        buffers_in_queue += 1
        grab_result.Release()

    print("Retrieved ", buffers_in_queue, " grab result from output queue.")

    # Stop the grabbing.
    camera.StopGrabbing()

    print(STRATEGY_SECTION_RULE)
    print("Grab using strategy GrabStrategy_LatestImages:")

    # The GrabStrategy_LatestImages strategy is used. The images are processed
    # in the order of their arrival, but only a number of the images received last
    # are kept in the output queue.

    # The size of the output queue can be adjusted.
    # When using this strategy the OutputQueueSize parameter can be changed during grabbing.
    camera.OutputQueueSize.Value = 2

    camera.StartGrabbing(pylon.GrabStrategy_LatestImages)

    # Execute the software trigger, wait actively until the camera accepts the next
    # frame trigger or until the timeout occurs.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(
                FRAME_TRIGGER_READY_TIMEOUT_MS,
                pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()

    # Wait for all images.
    time.sleep(POST_TRIGGER_SLEEP_MS / 1000.0)

    # Check whether the grab results are waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("Grab results wait in the output queue.")

    # Only the images received last are waiting in the internal output queue
    # and are now retrieved.
    # The grabbing continues in the background, e.g. when using hardware trigger mode.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        if grab_result.NumberOfSkippedImages:
            print("Skipped ", grab_result.NumberOfSkippedImages, " image.")
        buffers_in_queue += 1
        grab_result.Release()

    print("Retrieved ", buffers_in_queue, " grab results from output queue.")

    # When setting the output queue size to 1 this strategy is equivalent to grab
    # strategy GrabStrategy_LatestImageOnly.
    camera.OutputQueueSize.Value = 1

    # When setting the output queue size to CInstantCamera::MaxNumBuffer this strategy is
    # equivalent to GrabStrategy_OneByOne.
    camera.OutputQueueSize.Value = camera.MaxNumBuffer.Value

    # Stop the grabbing.
    camera.StopGrabbing()

    # The Upcoming Image grab strategy cannot be used together with USB camera devices.
    # For more information, see the advanced topics section of the pylon Programmer's Guide.
    if not camera.IsUsb():
        print(STRATEGY_SECTION_RULE)
        print("Grab using the GrabStrategy_UpcomingImage strategy:")

        # Reconfigure the camera to use continuous acquisition.
        pylon.AcquireContinuousConfiguration().OnOpened(camera)

        # The GrabStrategy_UpcomingImage strategy is used. A buffer for grabbing
        # is queued each time when RetrieveResult()
        # is called. The image data is grabbed into the buffer and returned.
        # This ensures that the image grabbed is the next image
        # received from the camera.
        # All images are still transported to the PC.
        camera.StartGrabbing(pylon.GrabStrategy_UpcomingImage)

        # Queues a buffer for grabbing and waits for the grab to finish.
        grab_result = camera.RetrieveResult(
            UPCOMING_RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException)
        grab_result.Release()

        # Sleep.
        time.sleep(UPCOMING_POST_RETRIEVE_SLEEP_MS / 1000.0)

        # Check no grab result is waiting, because no buffers are queued for grabbing.
        if not camera.GetGrabResultWaitObject().Wait(0):
            print("No grab result waits in the output queue.")

        # Stop the grabbing
        camera.StopGrabbing()

    camera.Close()

except BaseException as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
