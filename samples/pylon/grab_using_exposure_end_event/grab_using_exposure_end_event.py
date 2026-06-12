#!/usr/bin/env python3
"""\
Demonstrate Exposure End events and their timing relative to received image buffers.

This sample shows how to use the Exposure End event to speed up image acquisition.
For example, when a sensor exposure is finished, the camera can send an Exposure End
event to the computer. The computer can receive the event before the image data of
the finished exposure has been transferred completely. This avoids unnecessary delays,
e.g., when an image object moves before the related image data transfer is complete.

A camera event handler logs Exposure End events and an image event handler logs
grabbed buffers. The combined log shows the arrival order and inter-event timing.

Note: For ace 2 camera models, EventExposureEndFrameID and BlockID don't contain
matching values. The BlockID equivalent is the chunk value represented by
ChunkSelector FrameID. See the grab_chunk_image sample for more information.

Note: Camera event support depends on the camera model. Particularly the
Basler Camera Emulation does not provide writable EventSelector/
EventNotification nodes. See https://docs.baslerweb.com/event-notification
for a per-model list of available events.
"""
import sys
import time
from dataclasses import dataclass
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 20
RETRIEVE_TIMEOUT_MS = 5000

# Enumeration used for distinguishing different events.
EXPOSURE_END_EVENT_ID = 100


# Used for logging received events without outputting the information on the screen
# because outputting will change the timing.
@dataclass
class LogItem:
    """Single timestamped entry in the event log."""
    event_name: str
    frame_number: int
    timestamp: float


class SharedEventState:
    """Track expected frame numbers and log events with high-resolution timestamps."""
    def __init__(self, start_frame, is_16_bit_gige):
        self.next_expected_image = start_frame
        self.next_expected_exposure = start_frame
        self.next_frame_for_move = start_frame
        self.is_16_bit_gige = is_16_bit_gige
        self.log = []

    def _increment(self, frame_number):
        frame_number += 1
        # Zero is not a valid frame number for GigE cameras.
        if self.is_16_bit_gige and frame_number == 0:
            frame_number += 1
        return frame_number

    def log_event(self, event_name, frame_number):
        self.log.append(LogItem(event_name, int(frame_number), time.perf_counter()))

    # Check whether the imaged item or the sensor head can be moved.
    def move_if_ready(self, frame_number):
        if frame_number == self.next_frame_for_move:
            # The imaged item or the sensor head can be moved now...
            # The camera may not be ready yet for a trigger at this point because
            # the sensor is still being read out.
            # See the documentation of CInstantCamera::WaitForFrameTriggerReady()
            # for more information.
            self.log_event("Move", frame_number)
            self.next_frame_for_move = self._increment(frame_number)

    def on_exposure_end(self, frame_number):
        # An Exposure End event has been received.
        self.log_event("ExposureEndEvent", frame_number)
        self.move_if_ready(frame_number)
        # Check for missing Exposure End events.
        if frame_number != self.next_expected_exposure:
            print(
                "Warning: expected exposure-end frame",
                self.next_expected_exposure,
                "but got",
                frame_number
            )
        self.next_expected_exposure = self._increment(frame_number)

    # This method is called when an image has been grabbed.
    def on_image_received(self, frame_number):
        # An image has been received.
        self.log_event("ImageReceived", frame_number)
        # Check whether the imaged item or the sensor head can be moved.
        # This will be the case if the Exposure End has been lost or if the
        # Exposure End is received later than the image.
        self.move_if_ready(frame_number)
        # Check for missing images.
        if frame_number != self.next_expected_image:
            print(
                "Warning: expected image frame",
                self.next_expected_image,
                "but got",
                frame_number
            )
        self.next_expected_image = self._increment(frame_number)

    # Helper function for printing a log.
    def print_log(self):
        if not self.log:
            print("No events were logged.")
            return

        print()
        print("Warning. The time values printed may not be correct on older computer hardware.")
        print()
        # Print the event information header.
        print("Time [ms]    Event                 Frame Number")
        print("------------ --------------------- -----------")
        previous = None
        for item in self.log:
            delta_ms = 0.0 if previous is None else (item.timestamp - previous) * 1000.0
            # Print the event information.
            print(f"{delta_ms:12.4f} {item.event_name:<21} {item.frame_number}")
            previous = item.timestamp


class SampleCameraEventHandler(pylon.CameraEventHandler):
    """Forward Exposure End camera events to SharedEventState."""
    def __init__(self, state):
        super().__init__()
        self.state = state

    # This method is called when a camera event has been received.
    def OnCameraEvent(self, camera, user_provided_id, node):
        if user_provided_id != EXPOSURE_END_EVENT_ID:
            return

        if camera.EventExposureEndFrameID.IsReadable():
            frame_number = int(camera.EventExposureEndFrameID.Value)
        else:
            frame_number = int(camera.ExposureEndEventFrameID.Value)

        self.state.on_exposure_end(frame_number)


class SampleImageEventHandler(pylon.ImageEventHandler):
    """Forward grabbed image events to SharedEventState."""
    def __init__(self, state):
        super().__init__()
        self.state = state

    # This method is called when an image has been grabbed.
    def OnImageGrabbed(self, camera, grab_result):
        if grab_result.GrabSucceeded():
            self.state.on_image_received(int(grab_result.BlockID))


exit_code = 0
try:
    # Create the camera without a device so that GrabCameraEvents (which must be
    # set before Open) can be configured before the device is attached and opened.
    with pylon.InstantCamera() as camera:

        # Camera event processing must be enabled first. The default is off.
        # This must be set before Open().
        camera.GrabCameraEvents.Value = True

        # Now attach the first found device.
        camera.Attach(pylon.FirstFound)

        # Camera models behave differently regarding IDs and counters. Set initial values.
        is_gige = camera.DeviceInfo.DeviceClass == pylon.BaslerGigEDeviceClass
        is_16_bit_gige = False
        if is_gige and camera.GevGVSPExtendedIDMode.IsReadable():
            # If the GevGVSPExtendedIDMode is "Off", then the camera is using 16-bit mode.
            is_16_bit_gige = camera.GevGVSPExtendedIDMode.Value == "Off"
        
        # Zero is not a valid frame number for GigE cameras.
        state = SharedEventState(0 if not is_gige else 1, is_16_bit_gige)

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # Register the event handler.
        camera.RegisterImageEventHandler(
            SampleImageEventHandler(state),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete
        )

        # Open the camera to configure parameters.
        camera.Open()

        # Check whether the device supports events.
        if not camera.EventSelector.IsWritable() or not camera.EventNotification.IsWritable():
            print("The device doesn't support events.")
            sys.exit(0)

        if camera.NodeMap.Contains("ExposureEndEventData"):
            camera.RegisterCameraEventHandler(
                SampleCameraEventHandler(state),
                "ExposureEndEventData",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_Delete
            )
        else:
            camera.RegisterCameraEventHandler(
                SampleCameraEventHandler(state),
                "EventExposureEndData",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_Delete
            )

        # Enable the sending of Exposure End events.
        # Select the event to be received.
        if not camera.EventSelector.TrySetValue("ExposureEnd"):
            print("Could not enable Exposure End events in this environment.")
            sys.exit(0)

        # Start grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        # The camera device is operated in a default configuration that sets up
        # free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Retrieve grab results and notify the camera event and image event handlers.
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                pass

        # Disable the sending of Exposure End events.
        for event_name in ("ExposureEnd", "FrameStartOvertrigger", "EventOverrun"):
            if camera.EventSelector.TrySetValue(event_name):
                camera.EventNotification.TrySetValue("Off")

        # Print the recorded log showing the timing of events and images.
        state.print_log()

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
