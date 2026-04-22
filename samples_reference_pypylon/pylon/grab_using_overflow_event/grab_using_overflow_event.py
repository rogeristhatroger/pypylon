#!/usr/bin/env python3
"""\
Grab images using software-triggered AsyncGatedTriggerMultiframe mode
and synchronize each grab result with Overflow events from the frame
grabber.

This sample combines software triggering with evaluation of Overflow
events on a Basler CXP frame grabber. Images are acquired
asynchronously by InstantCamera, and each grab result is matched with
the corresponding EventOverflowFrameId / EventOverflowIsEndOfSequence
tag so the application knows precisely when a gated multiframe sequence
has finished.

A ConfigurationEventHandler is used to set up camera and frame grabber
parameters when the camera is opened.

This sample requires a CXP line scan camera connected through a Basler
CXP-12 frame grabber.
"""
import sys
import time
import threading
from pypylon import pylon
from pypylon import genicam

COUNT_OF_IMAGES_TO_GRAB = 20
RETRIEVE_TIMEOUT_MS = 5000
ROI_WIDTH = 8192
ROI_HEIGHT = 8192


class ImageTag:
    """Holds information about a frame for event synchronization."""

    def __init__(self, frame_id=0, is_sequence_end=False):
        self.frame_id = frame_id
        self.is_sequence_end = is_sequence_end


tag_list = []
tag_list_lock = threading.Lock()
is_terminated = False


def on_overflow_event(node_value):
    """GenICam callback invoked when an Overflow event arrives.

    Extracts the frame ID and isEndOfSequence flag from the event's
    child nodes and appends an ImageTag to the global tag list.
    """
    if is_terminated:
        return

    print("Event handler active")

    tag = ImageTag()
    try:
        tag.frame_id = node_value.Node.NodeMap.EventOverflowFrameId.Value
    except genicam.GenericException as e:
        print(f"[EventOverflowFrameId Error]: {e}")
    tag.is_sequence_end = node_value.Node.NodeMap.EventOverflowIsEndOfSequence.Value

    print(f"FRAME ID (Overflow Event): {tag.frame_id}")

    with tag_list_lock:
        tag_list.append(tag)


class CameraSetupConfiguration(pylon.ConfigurationEventHandler):
    """Configure camera and frame grabber parameters when the camera opens."""

    def OnOpened(self, camera):
        transport_layer_nodemap = camera.TLNodeMap

        # Set a test pattern on the camera.
        camera.TestPattern.Value = "Testimage3"
        print(f"Test pattern set to: {camera.TestPattern.Value}")

        # Disable automatic ROI control on the frame grabber.
        transport_layer_nodemap.AutomaticROIControl.Value = False

        # Set desired ROI dimensions.
        transport_layer_nodemap.Width.Value = ROI_WIDTH
        transport_layer_nodemap.Height.Value = ROI_HEIGHT
        print(f"ROI set to {ROI_WIDTH}x{ROI_HEIGHT}")

        # Set the image trigger mode.
        transport_layer_nodemap.ImageTriggerMode.Value = "AsyncGatedTriggerMultiframe"
        print("Trigger mode set to AsyncGatedTriggerMultiframe")

        # Set the trigger input source to software.
        transport_layer_nodemap.ImageTriggerInputSource.Value = "SoftwareTrigger"
        print("Trigger input source set to SoftwareTrigger")

        # Configure software trigger initial state (LowActive).
        transport_layer_nodemap.SetSoftwareTrigger.Value = "LowActive"
        print("Software trigger set to LowActive")


def configure_overflow_event(transport_layer_nodemap):
    """Enable Overflow event notification on the frame grabber."""
    print("Enabling Overflow event notification...")

    transport_layer_nodemap.EventSelector.Value = "Overflow"
    transport_layer_nodemap.EventNotification.Value = "On"
    transport_layer_nodemap.OverflowEventSelect.TrySetValue("All")


def find_cxp_camera():
    """Locate the first CXP camera device in the system.

    Returns the DeviceInfo of a camera connected through a Basler CXP-12
    frame grabber, or None if no such device is present.
    """
    info = pylon.DeviceInfo()
    info.DeviceClass = pylon.BaslerGenTlCxpDeviceClass
    device_filter = [info]
    device_list = pylon.TlFactory.GetInstance().EnumerateDevices(device_filter)
    if len(device_list) > 0:
        return device_list[0]
    else:
        return None


def grab_images(camera):
    """Continuously grab images and match each with its Overflow event tag."""
    while camera.IsGrabbing():
        print("Grabbing frame...")
        with camera.RetrieveResult(
            RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
        ) as grab_result:
            print("Frame retrieved.")

            if grab_result.GrabSucceeded():
                buffer_id = grab_result.ImageNumber
                print(f"Image Index: {buffer_id}")

                current_tag = ImageTag(frame_id=buffer_id)
                with tag_list_lock:
                    while tag_list and (buffer_id - 1) > tag_list[0].frame_id:
                        tag_list.pop(0)
                    if tag_list:
                        current_tag = tag_list.pop(0)

                print(
                    f"SizeX: {grab_result.Width}, "
                    f"SizeY: {grab_result.Height}, "
                    f"Payload: {grab_result.PayloadSize}"
                )

                img = grab_result.Array
                print(f"First pixel gray value: {img.flat[0]}")
                print()

                pylon.DisplayImage(int(buffer_id), grab_result)
            else:
                print(
                    "Grab Error:",
                    f"{grab_result.ErrorCode:#x}",
                    grab_result.ErrorDescription,
                )


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

    # Register the configuration before Open() so that OnOpened fires
    # and applies the setup. Open() on an already-open camera is a no-op,
    # so we construct without a device first.
    with pylon.InstantCamera() as camera:
        camera.RegisterConfiguration(
            CameraSetupConfiguration(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )
        camera.Attach(cxp_device_info, pylon.Unambiguous)
        camera.Open()

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        transport_layer_nodemap = camera.TLNodeMap

        configure_overflow_event(transport_layer_nodemap)

        event_overflow_node = transport_layer_nodemap.GetNode("EventOverflowData")
        event_callback_handle = genicam.Register(
            event_overflow_node, on_overflow_event, genicam.cbPostOutsideLock
        )

        camera.StartGrabbing(COUNT_OF_IMAGES_TO_GRAB)

        worker = threading.Thread(target=grab_images, args=(camera,))
        worker.start()

        # Simulate the gate signal with varying high-phase durations.
        software_trigger = transport_layer_nodemap.SetSoftwareTrigger
        time.sleep(0.1)
        for j in range(10):
            software_trigger.Value = "HighActive"
            time.sleep(j * 0.002)
            software_trigger.Value = "LowActive"
            time.sleep(0.1)
            print(f"Trigger #{j} sent.")

        worker.join()

        is_terminated = True
        genicam.Deregister(event_callback_handle)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
