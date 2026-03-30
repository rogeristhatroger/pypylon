from pypylon import pylon
from pylonusbtestcase import PylonTestCase
import unittest


class ConfigurationHelperTestSuite(PylonTestCase):
    def test_create_camera(self):
        cam = self.create_first()
        self.assertIsNotNone(cam)

    def test_disablealltriggers(self):
        """ Test the configuration helper method 'DisableAllTriggers' """
        cam = self.create_first()
        try:
            cam.Open()
            try:
                # if the nodes aren't available an exception is raised
                triggerselector = cam.TriggerSelector
                triggermode = cam.TriggerMode

                # save the trigger selector and the trigger modes
                original = triggerselector.Value
                original_modes = []
                for ts in triggerselector.GetSettableValues():
                    triggerselector.Value = ts
                    original_modes.append(triggermode.Value)

                try:
                    pylon.ConfigurationHelper.DisableAllTriggers(cam.NodeMap)

                    # test that the trigger modes are shut off
                    for ts in triggerselector.GetSettableValues():
                        triggerselector.Value = ts
                        self.assertEqual(
                            "Off",
                            triggermode.Value,
                            f"TriggerMode should be 'Off' for TriggerSelector '{ts}' after DisableAllTriggers",
                        )

                finally:
                    # restore the original values for trigger mode and trigger selector
                    for ts in triggerselector.GetSettableValues():
                        triggerselector.Value = ts
                        tm = original_modes.pop(0)
                        triggermode.Value = tm

                    triggerselector.Value = original

            except pylon.GenericException:
                # Calling without required nodes should remain safe.
                try:
                    pylon.ConfigurationHelper.DisableAllTriggers(cam.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableAllTriggers raised unexpectedly: {exc}")

        finally:
            cam.Close()

    def test_disablecompression(self):
        """Test the configuration 'DisableCompression' """
        cam = self.create_first()
        try:
            cam.Open()
            try:
                cm = cam.ImageCompressionMode
                original = cm.Value
                try:
                    pylon.ConfigurationHelper.DisableCompression(cam.NodeMap)
                    self.assertEqual("Off", cm.Value)
                finally:
                    cm.Value = original
            except:
                try: # Calling without the required node should be safe
                    pylon.ConfigurationHelper.DisableCompression(cam.NodeMap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableCompression raised unexpectedly: {exc}")
        finally:
            cam.Close()

    def test_disablegendc(self):
        cam = self.create_first()
        try:
            cam.Open()
            cameranodemap = cam.GetNodeMap()

            try:
                gendc = cam.GenDCStreamingMode
                original = gendc.Value

                try:
                    pylon.ConfigurationHelper.DisableGenDC(cameranodemap)
                    self.assertEqual("Off", gendc.Value)

                finally:
                    gendc.Value = original
            except:
                # Calling without required node should remain safe.
                try:
                    pylon.ConfigurationHelper.DisableGenDC(cameranodemap)
                except pylon.GenericException as exc:
                    self.fail(f"DisableGenDC raised unexpectedly: {exc}")
        finally:
            cam.Close()

    def test_selectrangecomponent(self):
        cam = self.create_first()
        try:
            cam.Open()
            cameranodemap = cam.GetNodeMap()
            try:
                cs = cam.ComponentSelector
                original = cs.Value

                try:
                    pylon.ConfigurationHelper.SelectRangeComponent(cameranodemap)
                    self.assertEqual("Range", cs.Value)
                finally:
                    cs.Value = original

            except:
                # Calling without the required nodes should remain safe.
                try:
                    pylon.ConfigurationHelper.SelectRangeComponent(cameranodemap)
                except pylon.GenericException as exc:
                    self.fail(f"SelectRangeComponent raised unexpectedly: {exc}")
        finally:
            cam.Close()

    def test_probepacketsize(self):
        cam = self.create_first()
        try:
            cam.Open()
            cameranodemap = cam.GetNodeMap()
            try:
                # ProbePacketSize executes a command to probe the optimal packet size.
                # It is safe to call even if the camera does not support it.
                pylon.ConfigurationHelper.ProbePacketSize(cameranodemap)
            except pylon.GenericException as exc:
                self.fail(f"ProbePacketSize raised unexpectedly: {exc}")
        finally:
            cam.Close()


if __name__ == '__main__':
    unittest.main()
