"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/DeviceFactory.i.
"""

from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class DeviceFactoryTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # IDeviceFactory subclass checks
    # ------------------------------------------------------------------

    def test_tl_factory_is_device_factory(self):
        """TlFactory is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.TlFactory, pylon.IDeviceFactory))

    def test_transport_layer_is_device_factory(self):
        """TransportLayer is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.TransportLayer, pylon.IDeviceFactory))

    def test_interface_is_device_factory(self):
        """Interface is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.Interface, pylon.IDeviceFactory))

    # ------------------------------------------------------------------
    # EDeviceAccessMode enum values
    # ------------------------------------------------------------------

    def test_device_access_mode_enum_values(self):
        """EDeviceAccessMode enum values match the expected C++ integer values."""
        self.assertEqual(pylon.DeviceAccessMode_Control, 0x1)
        self.assertEqual(pylon.DeviceAccessMode_Stream, 0x3)
        self.assertEqual(pylon.DeviceAccessMode_Event, 0x4)
        self.assertEqual(pylon.DeviceAccessMode_Exclusive, 0x5)

    # ------------------------------------------------------------------
    # EDeviceAccessiblityInfo enum values
    # ------------------------------------------------------------------

    def test_device_accessibility_info_enum_values(self):
        """EDeviceAccessiblityInfo enum values match the expected C++ integer values."""
        self.assertEqual(pylon.Accessibility_Unknown, 0)
        self.assertEqual(pylon.Accessibility_Ok, 1)
        self.assertEqual(pylon.Accessibility_Opened, 2)
        self.assertEqual(pylon.Accessibility_OpenedExclusively, 3)
        self.assertEqual(pylon.Accessibility_NotReachable, 4)


if __name__ == "__main__":
    unittest.main()
