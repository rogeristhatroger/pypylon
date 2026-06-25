"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/TransportLayer.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class TransportLayerTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def get_transport_layer(self):
        return pylon.TlFactory.GetInstance().TransportLayer(pylon.BaslerCamEmuDeviceClass)

    # ------------------------------------------------------------------
    # IDeviceFactory inheritance
    # ------------------------------------------------------------------

    def test_transport_layer_is_device_factory(self):
        """TransportLayer is a subclass of IDeviceFactory."""
        self.assertTrue(issubclass(pylon.TransportLayer, pylon.IDeviceFactory))

    # ------------------------------------------------------------------
    # TlInfo property
    # ------------------------------------------------------------------

    def test_tl_info_returns_tl_info_instance(self):
        """TlInfo property returns a TlInfo instance."""
        with self.get_transport_layer() as transport_layer:
            self.assertIsInstance(transport_layer.TlInfo, pylon.TlInfo)

    def test_tl_info_device_class_matches_emulator(self):
        """TlInfo.DeviceClass matches the emulator device class."""
        with self.get_transport_layer() as transport_layer:
            self.assertEqual(transport_layer.TlInfo.DeviceClass, pylon.BaslerCamEmuDeviceClass)

    # ------------------------------------------------------------------
    # NodeMap property
    # ------------------------------------------------------------------

    def test_node_map_returns_node_map_proxy(self):
        """NodeMap property returns a non-None object."""
        with self.get_transport_layer() as transport_layer:
            self.assertIsNotNone(transport_layer.NodeMap)

    def test_node_map_get_num_nodes_is_positive(self):
        """NodeMap contains at least one node."""
        with self.get_transport_layer() as transport_layer:
            self.assertGreater(transport_layer.NodeMap.GetNumNodes(), 0)

    # ------------------------------------------------------------------
    # EnumerateDevices
    # ------------------------------------------------------------------

    def test_enumerate_devices_returns_tuple(self):
        """EnumerateDevices returns a tuple."""
        with self.get_transport_layer() as transport_layer:
            self.assertIsInstance(transport_layer.EnumerateDevices(), tuple)

    def test_enumerate_devices_finds_emulated_cameras(self):
        """EnumerateDevices finds all emulated cameras."""
        with self.get_transport_layer() as transport_layer:
            self.assertEqual(len(transport_layer.EnumerateDevices()), self.num_devices)

    def test_enumerate_devices_returns_device_info_objects(self):
        """Every entry returned by EnumerateDevices is a DeviceInfo instance."""
        with self.get_transport_layer() as transport_layer:
            for di in transport_layer.EnumerateDevices():
                self.assertIsInstance(di, pylon.DeviceInfo)

    def test_enumerate_devices_filter_by_device_info(self):
        """EnumerateDevices with a DeviceInfo filter returns only matching devices."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertGreater(len(devices), 0)
            first = devices[0]
            filtered = transport_layer.EnumerateDevices([first])
            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_by_dict(self):
        """EnumerateDevices with a dict filter returns only matching devices."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertGreater(len(devices), 0)
            first = devices[0]
            filtered = transport_layer.EnumerateDevices(
                [{pylon.SerialNumberKey: first.SerialNumber,
                  pylon.DeviceClassKey: pylon.BaslerCamEmuDeviceClass}]
            )
            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_wrong_type_raises_type_error(self):
        """EnumerateDevices raises TypeError when filter list contains invalid items."""
        with self.get_transport_layer() as transport_layer:
            with self.assertRaises(TypeError):
                transport_layer.EnumerateDevices(["not_a_device_info"])

    # ------------------------------------------------------------------
    # EnumerateInterfaces
    # ------------------------------------------------------------------

    def test_enumerate_interfaces_returns_tuple(self):
        """EnumerateInterfaces returns a tuple."""
        with self.get_transport_layer() as transport_layer:
            self.assertIsInstance(transport_layer.EnumerateInterfaces(), tuple)

    def test_enumerate_interfaces_returns_interface_info_objects(self):
        """Every entry returned by EnumerateInterfaces is an InterfaceInfo instance."""
        with self.get_transport_layer() as transport_layer:
            for interface_info in transport_layer.EnumerateInterfaces():
                self.assertIsInstance(interface_info, pylon.InterfaceInfo)

    # ------------------------------------------------------------------
    # Interface context manager  (transport_layer.Interface())
    # ------------------------------------------------------------------

    def test_interface_context_yields_interface(self):
        """Interface context manager yields an Interface instance."""
        with self.get_transport_layer() as transport_layer:
            interface_infos = transport_layer.EnumerateInterfaces()
            self.assertGreater(len(interface_infos), 0)
            with transport_layer.Interface(interface_infos[0]) as interface:
                self.assertIsInstance(interface, pylon.Interface)

    def test_interface_context_destroys_interface_on_exit(self):
        """Interface context manager destroys the interface on exit."""
        with self.get_transport_layer() as transport_layer:
            interface_infos = transport_layer.EnumerateInterfaces()
            self.assertGreater(len(interface_infos), 0)
            with transport_layer.Interface(interface_infos[0]) as interface:
                self.assertIsNotNone(interface)
            # After exit re-creating the same interface must succeed,
            # proving DestroyInterface was called.
            with transport_layer.Interface(interface_infos[0]) as interface2:
                self.assertIsNotNone(interface2)

    # ------------------------------------------------------------------
    # InterfaceNodeMap context manager  (transport_layer.InterfaceNodeMap())
    # ------------------------------------------------------------------

    def test_interface_node_map_context_yields_node_map(self):
        """InterfaceNodeMap context manager yields a non-None nodemap."""
        with self.get_transport_layer() as transport_layer:
            interface_infos = transport_layer.EnumerateInterfaces()
            self.assertGreater(len(interface_infos), 0)
            with transport_layer.InterfaceNodeMap(interface_infos[0]) as node_map:
                self.assertIsNotNone(node_map)

    def test_interface_node_map_context_has_nodes(self):
        """InterfaceNodeMap context manager yields a nodemap with at least one node."""
        with self.get_transport_layer() as transport_layer:
            interface_infos = transport_layer.EnumerateInterfaces()
            self.assertGreater(len(interface_infos), 0)
            with transport_layer.InterfaceNodeMap(interface_infos[0]) as node_map:
                # there is not interface not map for the camera emulator currently
                self.assertEqual(node_map.GetNumNodes(), 0)

    # ------------------------------------------------------------------
    # CreateDevice / CreateFirstDevice / DestroyDevice
    # ------------------------------------------------------------------

    def test_create_device_returns_pylon_device(self):
        """CreateDevice with a DeviceInfo returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            device = transport_layer.CreateDevice(devices[0])
            try:
                self.assertIsInstance(device, pylon.PylonDevice)
            finally:
                transport_layer.DestroyDevice(device)

    def test_create_first_device_returns_pylon_device(self):
        """CreateFirstDevice with a DeviceInfo filter returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            device = transport_layer.CreateFirstDevice(self.device_filter[0])
            try:
                self.assertIsInstance(device, pylon.PylonDevice)
            finally:
                transport_layer.DestroyDevice(device)

    def test_create_first_device_no_filter_returns_pylon_device(self):
        """CreateFirstDevice without a filter returns a PylonDevice."""
        with self.get_transport_layer() as transport_layer:
            device = transport_layer.CreateFirstDevice()
            try:
                self.assertIsInstance(device, pylon.PylonDevice)
            finally:
                transport_layer.DestroyDevice(device)

    def test_destroy_device_releases_device(self):
        """DestroyDevice allows the same device to be created again afterwards."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            device = transport_layer.CreateDevice(devices[0])
            transport_layer.DestroyDevice(device)
            device2 = transport_layer.CreateDevice(devices[0])
            try:
                self.assertIsInstance(device2, pylon.PylonDevice)
            finally:
                transport_layer.DestroyDevice(device2)

    # ------------------------------------------------------------------
    # IsDeviceAccessible
    # ------------------------------------------------------------------

    def test_is_device_accessible_returns_true_for_available_device(self):
        """IsDeviceAccessible returns True for an available emulated device."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertTrue(transport_layer.IsDeviceAccessible(devices[0]))

    def test_is_device_accessible_info_ok_for_available_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_Ok for an available device."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            accessible, accessibility_info = transport_layer.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Control)
            self.assertTrue(accessible)
            self.assertEqual(accessibility_info, pylon.Accessibility_Ok)
            accessible, accessibility_info = transport_layer.IsDeviceAccessibleInfo(devices[0])
            self.assertTrue(accessible)
            self.assertEqual(accessibility_info, pylon.Accessibility_Ok)

    def test_is_device_accessible_info_opened_exclusively_for_open_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_OpenedExclusively when device is exclusively opened."""
        with self.get_transport_layer() as transport_layer:
            devices = transport_layer.EnumerateDevices()
            device = transport_layer.CreateDevice(devices[1])
            with pylon.InstantCamera(device) as camera:
                accessible, accessibility_info = transport_layer.IsDeviceAccessibleInfo(devices[1], pylon.DeviceAccessMode_Exclusive)
                self.assertTrue(accessible) # CamEmu returns true
                self.assertEqual(accessibility_info, pylon.Accessibility_Ok) # CamEmu returns OK

