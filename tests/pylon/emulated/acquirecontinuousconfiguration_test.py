"""\
This unit test checks the AcquireContinuousConfiguration class
introduced by `src/pylon/AcquireContinuousConfiguration.i`.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class AcquireContinuousConfigurationTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid configuration object."""
        configuration = pylon.AcquireContinuousConfiguration()
        self.assertIsNotNone(configuration)

    # ------------------------------------------------------------------
    # ApplyConfiguration
    # ------------------------------------------------------------------

    def test_apply_configuration(self):
        """ApplyConfiguration sets AcquisitionMode to Continuous."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # camera is open here
            camera.AcquisitionMode.Value = "SingleFrame"
            pylon.AcquireContinuousConfiguration.ApplyConfiguration(camera.NodeMap)
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")

    def test_apply_configuration_on_opened(self):
        """OnOpened applies the configuration and sets AcquisitionMode to Continuous."""
        with pylon.InstantCamera() as camera:
            camera.Attach(self.get_camera_traits(), pylon.FirstFound)
            # The configuration implements OnOpened, so it is applied when opening the camera
            camera.RegisterConfiguration(pylon.AcquireContinuousConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # for the camemu this node is a floating node and it can be changed before opening the camera
            camera.AcquisitionMode.Value = "SingleFrame"
            camera.Open()
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")


if __name__ == "__main__":
    unittest.main()
