#!/usr/bin/env python3
"""\
Demonstrate camera event handlers for Exposure End notifications during
software-triggered grabs.

It is shown in this sample how to register event handlers indicating the arrival
of events sent by the camera. For demonstration purposes, several different handlers
are registered for the same event.

Basler USB3 Vision and GigE Vision cameras can send event messages. For example,
when a sensor exposure has finished, the camera can send an Exposure End event to
the computer. The event can be received by the computer before the image data of
the finished exposure has been transferred completely. This sample demonstrates
how to be notified when camera event message data is received.

The event messages are automatically retrieved and processed by the InstantCamera
classes. The information carried by event messages is exposed as parameter nodes
in the camera node map and can be accessed like standard camera parameters. These
nodes are updated when a camera event is received. You can register camera event
handler objects that are triggered when event data has been received.

These mechanisms are demonstrated for the Exposure End and the Event Overrun events.
The Exposure End event carries the following information:
  ExposureEndEventFrameID: Number of the image that has been exposed.
  ExposureEndEventTimestamp: Time when the event was generated.
The Event Overrun event is sent by the camera as a warning that events are being
dropped. The notification contains no specific information about how many or which
events have been dropped. Events may be dropped if events are generated at a high
frequency and if there isn't enough bandwidth available to send the events.

Note: Camera event support depends on the camera model. Particularly the Basler 
Camera Emulation and many entry-level USB cameras (e.g. ace 2 Basic) do not 
provide writable EventSelector/EventNotification nodes.
See https://docs.baslerweb.com/event-notification for a per-model list of
available events.
"""
import sys
from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 5
TRIGGER_READY_TIMEOUT_MS = 1000
RETRIEVE_TIMEOUT_MS = 5000

EXPOSURE_END_EVENT_ID = 100
EVENT_OVERRUN_EVENT_ID = 200


class SampleCameraEventHandler(pylon.CameraEventHandler):
    """Print Exposure End and Event Overrun details when a camera event arrives."""

    # Only very short processing tasks should be performed by this method.
    # Otherwise, the event notification will block the processing of images.
    def OnCameraEvent(self, camera, user_provided_id, parameter):
        print()

        if user_provided_id == EXPOSURE_END_EVENT_ID:
            if camera.EventExposureEndFrameID.IsReadable():
                print(
                    "Exposure End event. FrameID:",
                    camera.EventExposureEndFrameID.Value,
                    "Timestamp:",
                    camera.EventExposureEndTimestamp.Value,
                )
            else:
                print(
                    "Exposure End event. FrameID:",
                    camera.ExposureEndEventFrameID.Value,
                    "Timestamp:",
                    camera.ExposureEndEventTimestamp.Value,
                )
        elif user_provided_id == EVENT_OVERRUN_EVENT_ID:
            if camera.EventOverrunEventFrameID.IsReadable():
                print(
                    "Event Overrun event. FrameID:",
                    camera.EventOverrunEventFrameID.Value,
                    "Timestamp:",
                    camera.EventOverrunEventTimestamp.Value,
                )
            else:
                print("Event Overrun event received.")


class GenericNodePrinter(pylon.CameraEventHandler):
    """Print the name of the node for which the camera event callback fired."""

    def OnCameraEvent(self, camera, user_provided_id, parameter):
        try:
            print("Camera event callback for node:", parameter.GetInfoOrDefault(pylon.ParameterInfo_Name, "<unknown>"))
        except Exception:
            print("Camera event callback fired.")


class SampleImageEventHandler(pylon.ImageEventHandler):
    """Print a notification when an image has been grabbed."""

    def OnImageGrabbed(self, camera, grab_result):
        print("SampleImageEventHandler.OnImageGrabbed called.")
        print()


exit_code = 0
try:
    # Create the camera without a device so that GrabCameraEvents (which must be
    # set before Open) can be configured before the device is attached and opened.
    with pylon.InstantCamera() as camera:

        handler1 = SampleCameraEventHandler()
        handler2 = GenericNodePrinter()

        # Register the standard configuration event handler for enabling software
        # triggering. The software trigger configuration handler replaces the
        # default configuration as all currently registered configuration handlers
        # are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(
            pylon.SoftwareTriggerConfiguration(),
            pylon.RegistrationMode_ReplaceAll,
            pylon.Cleanup_Delete,
        )

        camera.RegisterImageEventHandler(
            SampleImageEventHandler(),
            pylon.RegistrationMode_Append,
            pylon.Cleanup_Delete,
        )

        # Camera event processing must be activated first, the default is off.
        # This must be set before Open().
        camera.GrabCameraEvents.Value = True

        # Attach the first found device and open.
        camera.Attach(pylon.FirstFound)

        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        camera.Open()

        # Check if the device supports events.
        if not camera.EventSelector.IsWritable() or not camera.EventNotification.IsWritable():
            print("The device doesn't support events.")
            sys.exit(0)

        # Cameras based on SFNC 2.0 or later, e.g., USB cameras
        if camera.NodeMap.Contains("EventExposureEndData"):
            # Register an event handler for the Exposure End event. For each event
            # type, there is a "data" node representing the event. The actual data
            # that is carried by the event is held by child nodes of the data node.
            # In the case of the Exposure End event, the child nodes are
            # EventExposureEndFrameID and EventExposureEndTimestamp.
            camera.RegisterCameraEventHandler(
                handler1,
                "EventExposureEndData",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_None,
            )
            # The handler is registered for both the EventExposureEndFrameID and the
            # EventExposureEndTimestamp node. These nodes represent the data carried
            # by the Exposure End event. For each Exposure End event received, the
            # handler will be called twice: once for the frame ID, and once for the
            # time stamp.
            camera.RegisterCameraEventHandler(
                handler2,
                "EventExposureEndFrameID",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
            )
            camera.RegisterCameraEventHandler(
                handler2,
                "EventExposureEndTimestamp",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
            )
        else:
            camera.RegisterCameraEventHandler(
                handler1,
                "ExposureEndEventData",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_None,
            )

            # Register the same handler for a second event. The user-provided ID
            # can be used to distinguish between the events.
            camera.RegisterCameraEventHandler(
                handler1,
                "EventOverrunEventData",
                EVENT_OVERRUN_EVENT_ID,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
            )

            camera.RegisterCameraEventHandler(
                handler2,
                "ExposureEndEventFrameID",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
            )
            camera.RegisterCameraEventHandler(
                handler2,
                "ExposureEndEventTimestamp",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
            )

        # Enable sending of Exposure End events.
        if not camera.EventSelector.TrySetValue("ExposureEnd"):
            print("Could not enable Exposure End events in this environment.")
            sys.exit(0)

        if not camera.EventNotification.TrySetValue("On"):
            # scout-f, scout-g, and aviator GigE cameras use a different value.
            camera.EventNotification.SetValue("GenICamEvent")

        # Enable event notification for the EventOverrun event, if available.
        if camera.EventSelector.TrySetValue("EventOverrun"):
            if not camera.EventNotification.TrySetValue("On"):
                camera.EventNotification.SetValue("GenICamEvent")

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            if camera.WaitForFrameTriggerReady(
                TRIGGER_READY_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ):
                camera.ExecuteSoftwareTrigger()

            # Retrieve grab results and notify the camera event and image event handlers.
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                pass

        # Disable sending Exposure End and Event Overrun events.
        for event_name in ("ExposureEnd", "EventOverrun"):
            if camera.EventSelector.TrySetValue(event_name):
                camera.EventNotification.TrySetValue("Off")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
