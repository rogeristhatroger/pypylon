"""\
This unit test checks camera event handling for USB cameras.

USB cameras always use SFNC 2.x event node names:
  EventExposureEndData, EventExposureEndFrameID, EventExposureEndTimestamp.

GrabCameraEvents must be enabled before Open(), so these tests construct
an empty InstantCamera, configure it, then attach and open the device.
"""
from pylonusbtestcase import PylonTestCase
from pypylon import pylon
import unittest


COUNT_OF_IMAGES_TO_GRAB = 5
TRIGGER_READY_TIMEOUT_MS = 1000
RETRIEVE_TIMEOUT_MS = 5000

EXPOSURE_END_EVENT_ID = 100


class ExposureEndEventRecorder(pylon.CameraEventHandler):
    """Record Exposure End events for later assertion."""

    def __init__(self):
        super().__init__()
        self.event_count = 0
        self.frame_ids = []
        self.timestamps = []

    def OnCameraEvent(self, camera, user_provided_id, parameter):
        if user_provided_id == EXPOSURE_END_EVENT_ID:
            if camera.EventExposureEndFrameID.IsReadable():
                self.event_count += 1
                self.frame_ids.append(camera.EventExposureEndFrameID.Value)
                self.timestamps.append(camera.EventExposureEndTimestamp.Value)


class GrabCameraEventsTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Exposure End event
    # ------------------------------------------------------------------

    def test_exposure_end_event_received_for_every_frame(self):
        """One Exposure End event with a readable frame ID is received per grabbed image."""
        recorder = ExposureEndEventRecorder()

        # GrabCameraEvents must be set before Open(), so construct the camera
        # without a device first, then attach and open.
        with pylon.InstantCamera() as camera:
            camera.GrabCameraEvents.Value = True

            camera.RegisterConfiguration(
                pylon.SoftwareTriggerConfiguration(),
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_Delete,
            )

            # USB cameras use SFNC 2.x: register for the parent data node.
            camera.RegisterCameraEventHandler(
                recorder,
                "EventExposureEndData",
                EXPOSURE_END_EVENT_ID,
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_None,
            )

            camera.Attach(self.get_camera_traits(), pylon.FirstFound)
            camera.Open()

            if not camera.EventSelector.IsWritable():
                self.skipTest("Camera does not support event notification.")
            if not camera.EventSelector.TrySetValue("ExposureEnd"):
                self.skipTest("Camera does not support ExposureEnd events.")

            camera.EventNotification.Value = "On"

            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)
            while camera.IsGrabbing():
                camera.WaitForFrameTriggerReady(
                    TRIGGER_READY_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                )
                camera.ExecuteSoftwareTrigger()

                with camera.RetrieveResult(
                    RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())

            camera.EventSelector.Value = "ExposureEnd"
            camera.EventNotification.Value = "Off"

        self.assertEqual(COUNT_OF_IMAGES_TO_GRAB, recorder.event_count)
        self.assertEqual(COUNT_OF_IMAGES_TO_GRAB, len(recorder.frame_ids))

        # Frame IDs and timestamps must be strictly increasing across grabs.
        for index in range(1, len(recorder.frame_ids)):
            self.assertGreater(
                recorder.frame_ids[index],
                recorder.frame_ids[index - 1],
                f"Frame ID at index {index} is not greater than the previous one.",
            )
            self.assertGreater(
                recorder.timestamps[index],
                recorder.timestamps[index - 1],
                f"Timestamp at index {index} is not greater than the previous one.",
            )


if __name__ == "__main__":
    unittest.main()

