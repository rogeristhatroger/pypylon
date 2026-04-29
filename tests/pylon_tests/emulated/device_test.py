"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/Device.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class DeviceTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # PylonDevice creation
    # ------------------------------------------------------------------

    def test_create_pylon_device_returns_pylon_device(self):
        """TlFactory.CreateFirstDevice returns a PylonDevice instance."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice(self.device_filter[0])
        self.assertIsInstance(device, pylon.PylonDevice)
        tl_factory.DestroyDevice(device)

    # ------------------------------------------------------------------
    # DeviceInfo property
    # ------------------------------------------------------------------

    def test_device_info_is_not_none(self):
        """DeviceInfo property returns a non-None CDeviceInfo object."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice(self.device_filter[0])
        try:
            info = device.DeviceInfo
            self.assertIsNotNone(info)
        finally:
            tl_factory.DestroyDevice(device)

    def test_device_info_is_device_info_type(self):
        """DeviceInfo property returns a DeviceInfo instance."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice(self.device_filter[0])
        try:
            info = device.DeviceInfo
            self.assertIsInstance(info, pylon.DeviceInfo)
        finally:
            tl_factory.DestroyDevice(device)

    def test_device_info_device_class_is_emulator(self):
        """DeviceInfo.DeviceClass matches the emulator device class."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice(self.device_filter[0])
        try:
            info = device.DeviceInfo
            self.assertEqual(info.DeviceClass, pylon.BaslerCamEmuDeviceClass)
        finally:
            tl_factory.DestroyDevice(device)

if __name__ == "__main__":
    unittest.main()

