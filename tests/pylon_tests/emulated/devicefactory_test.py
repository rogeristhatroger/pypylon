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


if __name__ == "__main__":
    unittest.main()
