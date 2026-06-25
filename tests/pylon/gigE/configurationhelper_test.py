"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/ConfigurationHelper.i for GigE cameras.
"""
from pylongigetestcase import PylonTestCase
from pypylon import pylon
import unittest


class ConfigurationHelperTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Create camera
    # ------------------------------------------------------------------

    def test_create_camera(self):
        """InstantCamera can be created using get_camera_traits and FirstFound."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertIsNotNone(camera)
            self.assertTrue(camera.IsGigE())

    # ------------------------------------------------------------------
    # DisableAllTriggers
    # ------------------------------------------------------------------

    def test_disablealltriggers(self):
        """DisableAllTriggers sets TriggerMode to Off for every TriggerSelector entry."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            trigger_selector = camera.TriggerSelector
            trigger_mode = camera.TriggerMode
            if trigger_selector.IsWritable() and trigger_mode.IsWritable():

                # Save the original trigger selector and all trigger modes.
                original_selector = trigger_selector.Value
                original_modes = {}
                for entry in trigger_selector.GetSettableValues():
                    trigger_selector.Value = entry
                    original_modes[entry] = trigger_mode.Value
                    trigger_mode.TrySetValue("On")

                try:
                    pylon.ConfigurationHelper.DisableAllTriggers(camera.NodeMap)

                    for entry in trigger_selector.GetSettableValues():
                        trigger_selector.Value = entry
                        self.assertEqual(
                            "Off",
                            trigger_mode.Value,
                            f"TriggerMode should be 'Off' for TriggerSelector '{entry}' after DisableAllTriggers",
                        )
                finally:
                    # Restore the original trigger modes and selector.
                    for entry, mode in original_modes.items():
                        trigger_selector.Value = entry
                        trigger_mode.Value = mode
                    trigger_selector.Value = original_selector
            else:
                # Calling without required nodes should remain safe.
                try:
                    pylon.ConfigurationHelper.DisableAllTriggers(camera.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableAllTriggers raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # DisableCompression
    # ------------------------------------------------------------------

    def test_disablecompression(self):
        """DisableCompression sets ImageCompressionMode to Off when supported."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            compression_mode = camera.ImageCompressionMode
            if compression_mode.IsWritable():
                original = compression_mode.Value
                compression_mode.TrySetValue("BaslerCompressionBeyond")
                pylon.ConfigurationHelper.DisableCompression(camera.NodeMap)
                self.assertEqual("Off", compression_mode.Value)
                compression_mode.Value = original
            else:
                # Calling without the required node should be safe.
                try:
                    pylon.ConfigurationHelper.DisableCompression(camera.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableCompression raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # DisableGenDC
    # ------------------------------------------------------------------

    def test_disablegendc(self):
        """DisableGenDC sets GenDCStreamingMode to Off when supported."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            gendc = camera.GenDCStreamingMode
            if gendc.IsWritable():
                original = gendc.Value
                gendc.GenDCStreamingMode.TrySetValue("On")
                pylon.ConfigurationHelper.DisableGenDC(camera.NodeMap)
                self.assertEqual("Off", gendc.Value)
                gendc.Value = original
            else:
                # Calling without required node should remain safe.
                try:
                    pylon.ConfigurationHelper.DisableGenDC(camera.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableGenDC raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # SelectRangeComponent
    # ------------------------------------------------------------------

    def test_selectrangecomponent(self):
        """SelectRangeComponent sets ComponentSelector to Range when supported."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            component_selector = camera.ComponentSelector
            if component_selector.CanSetValue("Range"):
                original = component_selector.Value
                pylon.ConfigurationHelper.SelectRangeComponent(camera.NodeMap)
                self.assertEqual("Range", component_selector.Value)
                component_selector.Value = original
            else:
                # Calling without the required nodes should remain safe.
                try:
                    pylon.ConfigurationHelper.SelectRangeComponent(camera.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"SelectRangeComponent raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # ProbePacketSize
    # ------------------------------------------------------------------

    def test_probepacketsize(self):
        """ProbePacketSize executes without raising even when unsupported."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            original = camera.GevSCPSPacketSize.Value
            try:
                pylon.ConfigurationHelper.ProbePacketSize(camera.NodeMap)
            except pylon.GenericException as exc:
                self.fail(f"ProbePacketSize raised unexpectedly: {exc}")
            finally:
                camera.GevSCPSPacketSize.Value = original


if __name__ == "__main__":
    unittest.main()
