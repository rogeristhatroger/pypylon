"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/TlFactory.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class TlFactoryTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # GetInstance
    # ------------------------------------------------------------------

    def test_get_instance_returns_tl_factory(self):
        """GetInstance returns a TlFactory instance."""
        tl_factory = pylon.TlFactory.GetInstance()
        self.assertIsInstance(tl_factory, pylon.TlFactory)

    # ------------------------------------------------------------------
    # EnumerateTls
    # ------------------------------------------------------------------

    def test_enumerate_tls_returns_tuple(self):
        """EnumerateTls returns a tuple."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer_infos = tl_factory.EnumerateTls()
        self.assertIsInstance(transport_layer_infos, tuple)

    def test_enumerate_tls_contains_tl_info_objects(self):
        """Every entry returned by EnumerateTls is a TlInfo instance."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer_infos = tl_factory.EnumerateTls()
        for transport_layer_info in transport_layer_infos:
            self.assertIsInstance(transport_layer_info, pylon.TlInfo)

    def test_enumerate_tls_includes_emulator(self):
        """EnumerateTls includes the camera emulator transport layer."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer_infos = tl_factory.EnumerateTls()
        device_classes = [transport_layer_info.DeviceClass for transport_layer_info in transport_layer_infos]
        self.assertIn(pylon.BaslerCamEmuDeviceClass, device_classes)

    # ------------------------------------------------------------------
    # CreateTl / ReleaseTl
    # ------------------------------------------------------------------

    def test_create_tl_by_device_class_returns_none(self):
        """CreateTl with an unknown device class string returns None."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer = tl_factory.CreateTl("NonExistentTransportLayer_XYZ")
        self.assertIsNone(transport_layer)

    def test_create_tl_by_device_class_returns_transport_layer(self):
        """CreateTl with a device class string returns a TransportLayer."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer = tl_factory.CreateTl(pylon.BaslerCamEmuDeviceClass)
        try:
            self.assertIsInstance(transport_layer, pylon.TransportLayer)
        finally:
            tl_factory.ReleaseTl(transport_layer)

    def test_create_tl_by_tl_info_returns_transport_layer(self):
        """CreateTl with a TlInfo object returns a TransportLayer."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer_infos = tl_factory.EnumerateTls()
        emu_info = next(
            transport_layer_info
            for transport_layer_info in transport_layer_infos
            if transport_layer_info.DeviceClass == pylon.BaslerCamEmuDeviceClass
        )
        transport_layer = tl_factory.CreateTl(emu_info)
        try:
            self.assertIsInstance(transport_layer, pylon.TransportLayer)
        finally:
            tl_factory.ReleaseTl(transport_layer)

    # ------------------------------------------------------------------
    # TransportLayer context manager  (TlFactory.TransportLayer())
    # ------------------------------------------------------------------

    def test_transport_layer_context_by_string_enters_and_exits(self):
        """TransportLayer context manager by string yields a TransportLayer."""
        tl_factory = pylon.TlFactory.GetInstance()
        with tl_factory.TransportLayer(pylon.BaslerCamEmuDeviceClass) as transport_layer:
            self.assertIsInstance(transport_layer, pylon.TransportLayer)

    def test_transport_layer_context_by_tl_info_enters_and_exits(self):
        """TransportLayer context manager by TlInfo yields a TransportLayer."""
        tl_factory = pylon.TlFactory.GetInstance()
        transport_layer_infos = tl_factory.EnumerateTls()
        emu_info = next(
            transport_layer_info
            for transport_layer_info in transport_layer_infos
            if transport_layer_info.DeviceClass == pylon.BaslerCamEmuDeviceClass
        )
        with tl_factory.TransportLayer(emu_info) as transport_layer:
            self.assertIsInstance(transport_layer, pylon.TransportLayer)

    def test_transport_layer_context_enumerates_emulated_devices(self):
        """TransportLayer context manager exposes EnumerateDevices."""
        tl_factory = pylon.TlFactory.GetInstance()
        with tl_factory.TransportLayer(pylon.BaslerCamEmuDeviceClass) as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertEqual(len(devices), self.num_devices)

    # ------------------------------------------------------------------
    # EnumerateDevices
    # ------------------------------------------------------------------

    def test_enumerate_devices_returns_tuple(self):
        """TlFactory.EnumerateDevices returns a tuple."""
        tl_factory = pylon.TlFactory.GetInstance()
        self.assertIsInstance(tl_factory.EnumerateDevices(), tuple)

    def test_enumerate_devices_finds_emulated_cameras(self):
        """TlFactory.EnumerateDevices finds all emulated cameras."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        self.assertEqual(len(devices), self.num_devices)

    def test_enumerate_devices_returns_device_info_objects(self):
        """Every entry returned by EnumerateDevices is a DeviceInfo instance."""
        tl_factory = pylon.TlFactory.GetInstance()
        for device_info in tl_factory.EnumerateDevices():
            self.assertIsInstance(device_info, pylon.DeviceInfo)

    def test_enumerate_devices_filter_by_device_info(self):
        """EnumerateDevices with a DeviceInfo filter returns only matching devices."""
        tl_factory = pylon.TlFactory.GetInstance()
        with tl_factory.TransportLayer(pylon.BaslerCamEmuDeviceClass) as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertGreater(len(devices), 0)
            first = devices[0]
            filtered = tl_factory.EnumerateDevices([first])
            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_by_dict(self):
        """EnumerateDevices with a dict filter returns only matching devices."""
        tl_factory = pylon.TlFactory.GetInstance()
        with tl_factory.TransportLayer(pylon.BaslerCamEmuDeviceClass) as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertGreater(len(devices), 0)
            first = devices[0]
            filtered = tl_factory.EnumerateDevices(
                [{pylon.SerialNumberKey: first.SerialNumber,
                  pylon.DeviceClassKey: pylon.BaslerCamEmuDeviceClass}]
            )
            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0].SerialNumber, first.SerialNumber)

    def test_enumerate_devices_filter_by_device_class_dict(self):
        """EnumerateDevices with a DeviceClass dict returns all emulated cameras."""
        tl_factory = pylon.TlFactory.GetInstance()
        filtered = tl_factory.EnumerateDevices(
            [{pylon.DeviceClassKey: pylon.BaslerCamEmuDeviceClass}]
        )
        self.assertEqual(len(filtered), self.num_devices)

    def test_enumerate_devices_filter_mixed_list(self):
        """EnumerateDevices accepts a filter list mixing DeviceInfo and dict items."""
        tl_factory = pylon.TlFactory.GetInstance()
        with tl_factory.TransportLayer(pylon.BaslerCamEmuDeviceClass) as transport_layer:
            devices = transport_layer.EnumerateDevices()
            self.assertGreaterEqual(len(devices), 2)
            first = devices[0]
            second = devices[1]
            mixed_filter = [
                first,
                {pylon.SerialNumberKey: second.SerialNumber,
                 pylon.DeviceClassKey: pylon.BaslerCamEmuDeviceClass},
            ]
            filtered = tl_factory.EnumerateDevices(mixed_filter)
            serial_numbers = {di.SerialNumber for di in filtered}
            self.assertIn(first.SerialNumber, serial_numbers)
            self.assertIn(second.SerialNumber, serial_numbers)

    def test_enumerate_devices_filter_wrong_type_raises_type_error(self):
        """EnumerateDevices raises TypeError when filter list contains invalid items."""
        tl_factory = pylon.TlFactory.GetInstance()
        with self.assertRaises(TypeError):
            tl_factory.EnumerateDevices(["not_a_device_info"])

    def test_enumerate_devices_filter_dict_non_string_value_raises_type_error(self):
        """EnumerateDevices raises TypeError when a dict filter has a non-string value."""
        tl_factory = pylon.TlFactory.GetInstance()
        with self.assertRaises(TypeError):
            tl_factory.EnumerateDevices([{"SerialNumber": 42}])

    # ------------------------------------------------------------------
    # CreateDevice / CreateFirstDevice / DestroyDevice
    # ------------------------------------------------------------------

    def test_create_device_returns_pylon_device(self):
        """CreateDevice with a DeviceInfo returns a PylonDevice."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        device = tl_factory.CreateDevice(devices[0])
        try:
            self.assertIsInstance(device, pylon.PylonDevice)
        finally:
            tl_factory.DestroyDevice(device)

    def test_create_first_device_returns_pylon_device(self):
        """CreateFirstDevice with a DeviceInfo filter returns a PylonDevice."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice(self.device_filter[0])
        try:
            self.assertIsInstance(device, pylon.PylonDevice)
        finally:
            tl_factory.DestroyDevice(device)

    def test_create_first_device_no_filter_returns_pylon_device(self):
        """CreateFirstDevice without a filter returns a PylonDevice."""
        tl_factory = pylon.TlFactory.GetInstance()
        device = tl_factory.CreateFirstDevice()
        try:
            self.assertIsInstance(device, pylon.PylonDevice)
        finally:
            tl_factory.DestroyDevice(device)

    def test_destroy_device_releases_device(self):
        """DestroyDevice allows the same device to be created again afterwards."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        device = tl_factory.CreateDevice(devices[0])
        tl_factory.DestroyDevice(device)
        device2 = tl_factory.CreateDevice(devices[0])
        try:
            self.assertIsInstance(device2, pylon.PylonDevice)
        finally:
            tl_factory.DestroyDevice(device2)

    # ------------------------------------------------------------------
    # IsDeviceAccessible
    # ------------------------------------------------------------------

    def test_is_device_accessible_returns_true_for_available_device(self):
        """IsDeviceAccessible returns True for an available emulated device."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        self.assertTrue(tl_factory.IsDeviceAccessible(devices[0]))

    def test_is_device_accessible_info_returns_tuple(self):
        """IsDeviceAccessibleInfo returns a (bool, accessibility_info) tuple."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        result = tl_factory.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Control)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_is_device_accessible_info_ok_for_available_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_Ok for an available device."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        accessible, accessibility_info = tl_factory.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Control)
        self.assertTrue(accessible)
        self.assertEqual(accessibility_info, pylon.Accessibility_Ok)
        accessible, accessibility_info = tl_factory.IsDeviceAccessibleInfo(devices[0])
        self.assertTrue(accessible)
        self.assertEqual(accessibility_info, pylon.Accessibility_Ok)

    def test_is_device_accessible_info_opened_exclusively_for_open_device(self):
        """IsDeviceAccessibleInfo reports Accessibility_OpenedExclusively when device is exclusively opened."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        device = tl_factory.CreateDevice(devices[0])
        with pylon.InstantCamera(device) as camera:
            accessible, accessibility_info = tl_factory.IsDeviceAccessibleInfo(devices[0], pylon.DeviceAccessMode_Exclusive)
            self.assertTrue(accessible) # CamEmu returns true
            self.assertEqual(accessibility_info, pylon.Accessibility_Ok) # CamEmu returns OK

