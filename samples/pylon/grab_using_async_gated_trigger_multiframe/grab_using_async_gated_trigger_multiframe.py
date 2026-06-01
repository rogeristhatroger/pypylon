#!/usr/bin/env python3
"""\
Grab line scan images using asynchronous gated trigger multiframe mode
with a software-simulated gate signal.

This sample demonstrates how to use AsyncGatedTriggerMultiframe in line
scan applications where a gate signal marks start and end of an object
(e.g. a light barrier on a conveyor belt). The frame grabber appends
acquired lines into buffers of a fixed ROI height. When the gate goes
low, the remaining lines form a shorter final buffer. The Overflow
event's isEndOfSequence flag indicates the last buffer in each sequence.

Because no external trigger hardware is needed here, the gate is
simulated via the frame grabber's SoftwareTrigger node. For the
hardware-triggered variant see grab_using_async_gated_trigger_multiframe_hardware.

This sample requires a CXP line scan camera connected through a Basler
CXP-12 frame grabber.
"""
import sys
import time
import threading
from pypylon import pylon
from pypylon import genicam

COUNT_OF_IMAGES_TO_GRAB = 100
RETRIEVE_TIMEOUT_MS = 5000
ROI_WIDTH = 8192
ROI_HEIGHT = 20


class ImageTags:
    """Thread-safe list that pairs frame IDs with end-of-sequence flags.

    The Overflow event callback inserts entries; the grab thread consumes
    them to determine whether a grabbed buffer is the last in a sequence.
    """

    def __init__(self):
        self._tags = []  # list of (frame_id, is_sequence_end)
        self._lock = threading.Lock()

    def insert(self, frame_id, is_sequence_end=False):
        with self._lock:
            self._tags.append((frame_id, is_sequence_end))

    def synchronize(self, current_frame_id):
        """Pop entries until the tag matches *current_frame_id*.

        If the tag list runs empty (events lost), assume the frame is
        not an end-of-sequence.
        """
        with self._lock:
            is_sequence_end = False
            while True:
                if self._tags:
                    frame_id, is_sequence_end = self._tags.pop(0)
                else:
                    frame_id = current_frame_id
                    is_sequence_end = False
                if frame_id >= current_frame_id - 1:
                    break
            return is_sequence_end


image_tags = ImageTags()
is_terminated = False


def on_overflow_event(node_value):
    """GenICam callback invoked when an Overflow event arrives.

    Extracts the frame ID and isEndOfSequence flag from the event
    category child nodes and records them in *image_tags*.
    """
    if is_terminated:
        print("Inactive event handling!")
        return

    print("Event handler active")
    frame_id = 0
    is_sequence_end = False

    frame_id = node_value.Node.NodeMap.EventOverflowFrameId.Value
    is_sequence_end = node_value.Node.NodeMap.EventOverflowIsEndOfSequence.Value

    print(f"Frame ID: {frame_id}")
    image_tags.insert(frame_id, is_sequence_end)


def grab_thread(camera):
    """Retrieve images in a background thread and track sequences."""
    cumulated_height = 0

    while camera.IsGrabbing():
        with camera.RetrieveResult(
            RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
        ) as grab_result:
            if grab_result.GrabSucceeded():
                buffer_id = grab_result.ImageNumber
                is_sequence_end = image_tags.synchronize(buffer_id)

                # Some camera models use a GenICam Generic Data Container (GenDC) format.
                # For single grabbed images, a data component is emulated automatically.
                # pylon provides a data component wrapper to handle both cases uniformly.
                with grab_result.GetFirstImageDataComponent() as image_data_component:
                    current_height = image_data_component.Height
                    if is_sequence_end:
                        print(f"THE SEQUENCE END TAG IS HERE: {buffer_id}")
                        print(f"--Complete height was: {cumulated_height}")
                        cumulated_height = 0
                    else:
                        cumulated_height += current_height

                    print(f"Actual Frame Height:  {current_height}")
                    print(f"Image Index: {buffer_id}")

                    img = image_data_component.Array
                    print(f"Gray value of first pixel: {img.flat[0]}")
                    print()
            else:
                print(
                    "Error:",
                    f"{grab_result.ErrorCode:#x}",
                    grab_result.ErrorDescription,
                )


def find_cxp_camera():
    """Locate the first CXP camera device in the system.

    Returns the DeviceInfo of a camera connected through a Basler CXP-12
    frame grabber, or None if no such device is present.
    """
    device_list = pylon.TlFactory.GetInstance().EnumerateDevices(
        [{pylon.DeviceClassKey : pylon.BaslerGenTlCxpDeviceClass}]
    )
    if len(device_list) > 0:
        return device_list[0]
    else:
        return None


exit_code = 0
try:
    # Verify the required hardware is connected before doing anything else.
    cxp_device_info = find_cxp_camera()
    if cxp_device_info is None:
        print(
            "No CXP camera found. This sample requires a CXP line scan "
            "camera connected through a Basler CXP-12 frame grabber."
        )
        sys.exit(1)

    # GrabCameraEvents must be set before Open() and is not writable once
    # the camera is open, so we construct without a device first.
    with pylon.InstantCamera() as camera:
        camera.GrabCameraEvents.Value = True
        camera.Attach(cxp_device_info, pylon.Unambiguous)
        camera.Open()

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        transport_layer_nodemap = camera.TLNodeMap

        # Set a test pattern on the camera.
        camera.TestPattern.Value = "Testimage3"
        print("Setting the Test Pattern")

        # Disable automatic ROI control on the frame grabber.
        transport_layer_nodemap.AutomaticROIControl.Value = False

        # --- Configure Overflow event ---
        print("Enable Event...")
        transport_layer_nodemap.EventSelector.Value = "Overflow"
        transport_layer_nodemap.EventNotification.Value = "On"
        transport_layer_nodemap.OverflowEventSelect.TrySetValue("All")

        # Register a GenICam callback on the EventOverflowData node.
        event_overflow_node = transport_layer_nodemap.EventOverflowData
        event_callback_handle = genicam.Register(
            event_overflow_node, on_overflow_event, genicam.cbPostOutsideLock
        )

        # --- Set frame grabber ROI ---
        transport_layer_nodemap.Height.Value = ROI_HEIGHT
        transport_layer_nodemap.Width.Value = ROI_WIDTH
        print("Setting FG ROI")

        # --- Set trigger mode ---
        transport_layer_nodemap.ImageTriggerMode.Value = "AsyncGatedTriggerMultiframe"
        print("Setting Image Trigger Mode")

        # Use software trigger as the gate signal source.
        transport_layer_nodemap.ImageTriggerInputSource.Value = "SoftwareTrigger"

        software_trigger = transport_layer_nodemap.SetSoftwareTrigger
        software_trigger.Value = "LowActive"

        print("Software Trigger...")

        # --- Grab ---
        camera.StartGrabbing(COUNT_OF_IMAGES_TO_GRAB)
        time.sleep(1.0)

        worker = threading.Thread(target=grab_thread, args=(camera,))
        worker.start()

        # Simulate the gate signal with varying high-phase durations.
        time.sleep(0.1)
        for j in range(10):
            software_trigger.Value = "HighActive"
            time.sleep(j * 0.002)
            software_trigger.Value = "LowActive"
            time.sleep(0.1)
            print(j)

        worker.join()

        is_terminated = True
        genicam.Deregister(event_callback_handle)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
