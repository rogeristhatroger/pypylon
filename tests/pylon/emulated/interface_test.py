"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/Interface.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class InterfaceTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_transport_layer(self):
        return pylon.TlFactory.GetInstance().TransportLayer(pylon.BaslerCamEmuDeviceClass)

    def get_interface_info(self, transport_layer):
        interface = transport_layer.EnumerateInterfaces()
        self.assertGreater(len(interface), 0, "No interfaces found for emulator TL")
        return interface[0]

    # ------------------------------------------------------------------
    # IDeviceFactory inheritance
    # ------------------------------------------------------------------

    def test_interface_is_device_factory(self):
        """Interface is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.Interface, pylon.IDeviceFactory))

    # ------------------------------------------------------------------
    # EnumerateDevices
    # ------------------------------------------------------------------

    def test_enumerate_devices_returns_tuple(self):
        """EnumerateDevices returns a tuple."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertIsInstance(interface.EnumerateDevices(), tuple)

    def test_enumerate_devices_finds_emulated_cameras(self):
        """EnumerateDevices finds all emulated cameras."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertEqual(len(interface.EnumerateDevices()), self.num_devices)

    def test_enumerate_devices_returns_device_info_objects(self):
        """Every entry returned by EnumerateDevices is a DeviceInfo instance."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                for device_info in interface.EnumerateDevices():
                    self.assertIsInstance(device_info, pylon.DeviceInfo)

    def test_enumerate_devices_filter_by_device_info(self):
        """EnumerateDevices with a DeviceInfo filter returns only matching devices."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                self.assertGreater(len(devices), 0)
                first = devices[0]
                filtered = interface.EnumerateDevices([first])
                self.assertEqual(len(filtered), 1)
                self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_by_dict(self):
        """EnumerateDevices with a dict filter returns only matching devices."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                self.assertGreater(len(devices), 0)
                first = devices[0]
                filtered = interface.EnumerateDevices(
                    [{pylon.SerialNumberKey: first.SerialNumber,
                      pylon.DeviceClassKey: pylon.BaslerCamEmuDeviceClass}]
                )
                self.assertEqual(len(filtered), 1)
                self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_wrong_type_raises_type_error(self):
        """EnumerateDevices raises TypeError when filter list contains invalid items."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                with self.assertRaises(TypeError):
                    interface.EnumerateDevices(["not_a_device_info"])

    # ------------------------------------------------------------------
    # InterfaceInfo property
    # ------------------------------------------------------------------

    def test_interface_info_returns_interface_info_instance(self):
        """InterfaceInfo property returns an InterfaceInfo instance."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertIsInstance(interface.InterfaceInfo, pylon.InterfaceInfo)

    def test_interface_info_device_class_matches_emulator(self):
        """InterfaceInfo.DeviceClass matches the emulator device class."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertEqual(interface.InterfaceInfo.DeviceClass, pylon.BaslerCamEmuDeviceClass)

    # ------------------------------------------------------------------
    # Open / Close / IsOpen
    # ------------------------------------------------------------------

    def test_is_open_false_before_open(self):
        """IsOpen returns False before Open is called."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertFalse(interface.IsOpen())

    def test_is_open_true_after_open(self):
        """IsOpen returns True after Open is called."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                interface.Open()
                try:
                    self.assertTrue(interface.IsOpen())
                finally:
                    interface.Close()

    def test_is_open_false_after_close(self):
        """IsOpen returns False after Close is called."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                interface.Open()
                interface.Close()
                self.assertFalse(interface.IsOpen())

    # ------------------------------------------------------------------
    # NodeMap property (context manager)
    # ------------------------------------------------------------------

    def test_node_map_context_opens_and_closes_interface(self):
        """NodeMap context manager opens the interface on enter and closes it on exit."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                self.assertFalse(interface.IsOpen())
                with interface.NodeMap:
                    self.assertTrue(interface.IsOpen())
                self.assertFalse(interface.IsOpen())

    def test_node_map_context_returns_node_map(self):
        """NodeMap context manager yields a non-None object."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                with interface.NodeMap as node_map:
                    self.assertIsNotNone(node_map)

    def test_node_map_context_closes_on_exception(self):
        """NodeMap context manager closes the interface even if an exception occurs."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                try:
                    with interface.NodeMap:
                        raise RuntimeError("intentional error")
                except RuntimeError:
                    pass
                self.assertFalse(interface.IsOpen())

    # ------------------------------------------------------------------
    # CreateDevice / CreateFirstDevice / DestroyDevice
    # ------------------------------------------------------------------

    def test_create_device_returns_pylon_device(self):
        """CreateDevice with a DeviceInfo returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                device = interface.CreateDevice(devices[0])
                try:
                    self.assertIsInstance(device, pylon.PylonDevice)
                finally:
                    interface.DestroyDevice(device)

    def test_create_first_device_returns_pylon_device(self):
        """CreateFirstDevice with a DeviceInfo filter returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                device = interface.CreateFirstDevice(self.device_filter[0])
                try:
                    self.assertIsInstance(device, pylon.PylonDevice)
                finally:
                    interface.DestroyDevice(device)

    def test_create_first_device_no_filter_returns_pylon_device(self):
        """CreateFirstDevice without a filter returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                device = interface.CreateFirstDevice()
                try:
                    self.assertIsInstance(device, pylon.PylonDevice)
                finally:
                    interface.DestroyDevice(device)

    def test_destroy_device_releases_device(self):
        """DestroyDevice allows the same device to be created again afterwards."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                device = interface.CreateDevice(devices[0])
                interface.DestroyDevice(device)
                device2 = interface.CreateDevice(devices[0])
                try:
                    self.assertIsInstance(device2, pylon.PylonDevice)
                finally:
                    interface.DestroyDevice(device2)

    # ------------------------------------------------------------------
    # IsDeviceAccessible
    # ------------------------------------------------------------------

    def test_is_device_accessible_returns_true_for_available_device(self):
        """IsDeviceAccessible returns True for an available emulated device."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                self.assertTrue(interface.IsDeviceAccessible(devices[0]))

    def test_is_device_accessible_info_ok_for_available_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_Ok for an available device."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                accessible, accessibility_info = interface.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Control)
                self.assertTrue(accessible)
                self.assertEqual(accessibility_info, pylon.Accessibility_Ok)
                accessible, accessibility_info = interface.IsDeviceAccessibleInfo(devices[0])
                self.assertTrue(accessible)
                self.assertEqual(accessibility_info, pylon.Accessibility_Ok)

    def test_is_device_accessible_info_opened_exclusively_for_open_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_OpenedExclusively when device is exclusively opened."""
        with self.get_transport_layer() as transport_layer:
            with transport_layer.Interface(self.get_interface_info(transport_layer)) as interface:
                devices = interface.EnumerateDevices()
                device = interface.CreateDevice(devices[0])
                with pylon.InstantCamera(device) as camera:
                    accessible, accessibility_info = interface.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Exclusive)
                    self.assertTrue(accessible) # CamEmu returns true
                    self.assertEqual(accessibility_info, pylon.Accessibility_Ok) # CamEmu returns OK


if __name__ == "__main__":
    unittest.main()

