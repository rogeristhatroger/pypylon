"""\
This unit test checks the container types returned by the pylon.TlFactory
enumeration methods (EnumerateTls, EnumerateInterfaces, EnumerateDevices).
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class ContainerTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # TlInfo container
    # ------------------------------------------------------------------

    def test_enumerate_tls_returns_tuple_of_tl_infos(self):
        """EnumerateTls returns a non-empty tuple of TlInfo objects."""
        tl_infos = pylon.TlFactory.GetInstance().EnumerateTls()
        self.assertIsInstance(tl_infos, tuple)
        self.assertGreater(len(tl_infos), 0)
        self.assertIsInstance(tl_infos[0], pylon.TlInfo)

    # ------------------------------------------------------------------
    # InterfaceInfo container
    # ------------------------------------------------------------------

    def test_enumerate_interfaces_returns_tuple_of_interface_infos(self):
        """EnumerateInterfaces returns a tuple of InterfaceInfo objects for each available TL."""
        tl_factory = pylon.TlFactory.GetInstance()
        for tl_info in tl_factory.EnumerateTls():
            try:
                current_tl = tl_factory.CreateTl(tl_info)
            except Exception:
                continue
            if current_tl is None:
                continue
            try:
                interface_infos = current_tl.EnumerateInterfaces()
                self.assertIsInstance(interface_infos, tuple)
                self.assertGreater(len(interface_infos), 0)
                self.assertIsInstance(interface_infos[0], pylon.InterfaceInfo)
            finally:
                tl_factory.ReleaseTl(current_tl)

    # ------------------------------------------------------------------
    # DeviceInfo container
    # ------------------------------------------------------------------

    def test_enumerate_devices_returns_tuple(self):
        """EnumerateDevices returns a tuple, with DeviceInfo elements when devices are present."""
        device_infos = pylon.TlFactory.GetInstance().EnumerateDevices()
        self.assertIsInstance(device_infos, tuple)
        if len(device_infos) > 0:
            self.assertIsInstance(device_infos[0], pylon.DeviceInfo)


if __name__ == "__main__":
    unittest.main()
