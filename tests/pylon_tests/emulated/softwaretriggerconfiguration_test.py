"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/SoftwareTriggerConfiguration.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class SoftwareTriggerConfigurationTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid configuration object."""
        configuration = pylon.SoftwareTriggerConfiguration()
        self.assertIsNotNone(configuration)

    # ------------------------------------------------------------------
    # ApplyConfiguration
    # ------------------------------------------------------------------

    def test_apply_configuration(self):
        """ApplyConfiguration enables software triggering and sets AcquisitionMode to Continuous."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # camera is open here
            camera.AcquisitionMode.Value = "SingleFrame"
            pylon.SoftwareTriggerConfiguration.ApplyConfiguration(camera.NodeMap)
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")
            self.assertEqual(camera.TriggerSelector.Value, "FrameStart")
            self.assertEqual(camera.TriggerMode.Value, "On")
            self.assertEqual(camera.TriggerSource.Value, "Software")

    def test_apply_configuration_on_opened(self):
        """OnOpened applies the configuration and enables software triggering."""
        with pylon.InstantCamera() as camera:
            camera.Attach(self.get_camera_traits(), pylon.FirstFound)
            # The configuration implements OnOpened, so it is applied when opening the camera
            camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # for the camemu this node is a floating node and it can be changed before opening the camera
            camera.AcquisitionMode.Value = "SingleFrame"
            camera.Open()
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")
            self.assertEqual(camera.TriggerSelector.Value, "FrameStart")
            self.assertEqual(camera.TriggerMode.Value, "On")
            self.assertEqual(camera.TriggerSource.Value, "Software")

    # ------------------------------------------------------------------
    # Software trigger flow
    # ------------------------------------------------------------------

    def test_software_trigger_grab(self):
        """A grabbed frame can be triggered via ExecuteSoftwareTrigger after the configuration is applied."""
        with pylon.InstantCamera() as camera:
            camera.Attach(self.get_camera_traits(), pylon.FirstFound)
            camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
            self.assertTrue(camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException))
            camera.ExecuteSoftwareTrigger()
            with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
            camera.StopGrabbing()


if __name__ == "__main__":
    unittest.main()
