"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/ActionTriggerConfiguration.i.
"""

from pylongigetestcase import PylonTestCase
from pypylon import pylon
import unittest


class ActionTriggerConfigurationTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _require_action_commands(self, camera):
        """Skip the calling test if the camera does not support Action Commands."""
        if (not camera.ActionGroupKey.IsReadable()) or (not camera.ActionGroupMask.IsReadable()):
            self.skipTest("Camera does not support Action Commands - skipping test.")

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction_with_device_and_group_key(self):
        """Construction with device key and group key produces a valid configuration."""
        configuration = pylon.ActionTriggerConfiguration(1, 2)
        self.assertIsNotNone(configuration)

    def test_construction_with_group_mask(self):
        """Construction with device key, group key and group mask produces a valid configuration."""
        configuration = pylon.ActionTriggerConfiguration(1, 2, 3)
        self.assertIsNotNone(configuration)

    def test_copy_construction(self):
        """Copy construction produces a configuration equal to the original."""
        original = pylon.ActionTriggerConfiguration(1, 2, 3)
        copy = pylon.ActionTriggerConfiguration(original)
        self.assertIsNotNone(copy)

    # ------------------------------------------------------------------
    # AllGroupMask
    # ------------------------------------------------------------------

    def test_all_group_mask_constant(self):
        """AllGroupMask is accessible and equals 0xffffffff."""
        self.assertEqual(pylon.AllGroupMask, 0xffffffff)

    # ------------------------------------------------------------------
    # ApplyConfiguration
    # ------------------------------------------------------------------

    def test_apply_configuration(self):
        """ApplyConfiguration sets ActionDeviceKey and ActionGroupKey on the node map."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self._require_action_commands(camera)
            camera.AcquisitionMode.TrySetValue("SingleFrame")
            pylon.ActionTriggerConfiguration.ApplyConfiguration(camera.NodeMap, 1, 2)
            self.assertEqual(camera.ActionDeviceKey.GetValueOrDefault(1), 1)  #defined write-only by SFNC
            self.assertEqual(camera.ActionGroupKey.Value, 2)
            self.assertEqual(camera.ActionGroupMask.Value, pylon.AllGroupMask)
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")

    def test_apply_configuration_on_opened(self):
        """OnOpened applies the configuration, setting ActionDeviceKey, ActionGroupKey and AcquisitionMode to Continuous."""
        with pylon.InstantCamera() as camera:
            camera.Attach(self.get_camera_traits(), pylon.FirstFound)

            # Open without ActionTriggerConfiguration first to check feature support.
            camera.Open()
            self._require_action_commands(camera)
            camera.Close()

            # The configuration implements OnOpened, so it is applied when opening the camera.
            camera.RegisterConfiguration(
                pylon.ActionTriggerConfiguration(1, 2),
                pylon.RegistrationMode_ReplaceAll,
                pylon.Cleanup_Delete,
            )
            camera.Open()
            self.assertEqual(camera.ActionDeviceKey.GetValueOrDefault(1), 1) #defined write-only by SFNC
            self.assertEqual(camera.ActionGroupKey.Value, 2)
            self.assertEqual(camera.ActionGroupMask.Value, pylon.AllGroupMask)
            self.assertEqual(camera.AcquisitionMode.Value, "Continuous")


if __name__ == "__main__":
    unittest.main()
