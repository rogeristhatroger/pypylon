from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import numpy
import unittest


class InstantCameraTestSuite(PylonEmuTestCase):
    def test_open_device(self):
        cam = pylon.InstantCamera()
        self.assertFalse(cam.IsOpen())
        cam = self.create_first()
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()
        self.assertFalse(cam.IsOpen())

    def test_attach(self):
        cam = pylon.InstantCamera()
        self.assertFalse(cam.IsPylonDeviceAttached())
        dev = pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        cam.Attach(dev)
        cam.Open()
        self.assertTrue(cam.IsPylonDeviceAttached())
        cam.DetachDevice()
        self.assertFalse(cam.IsPylonDeviceAttached())

    def test_destroy_device(self):
        cam = self.create_first()
        cam.Open()
        cam.DestroyDevice()
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_grab_one(self):
        cam = self.create_first()
        cam.Open()
        self.assertTrue(cam.GrabOne(1000))
        result = cam.GrabOne(1000)
        actual = list(result.Array[0:20, 0])
        expected = [actual[0] + i for i in range(20)]
        self.assertEqual(actual, expected)
        cam.Close()

    def test_grabbing(self):
        cam = self.create_first()
        cam.Open()
        self.assertFalse(cam.IsGrabbing())
        cam.StartGrabbing()
        self.assertTrue(cam.IsGrabbing())
        i = 0
        while (i < 10):
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                self.assertEqual(1024, grabResult.Width)
                self.assertEqual(1040, grabResult.Height)
                img = grabResult.Array
            grabResult.Release()
            self.assertTrue(cam.IsGrabbing())
            i = i + 1
        cam.StopGrabbing()
        self.assertFalse(cam.IsGrabbing())
        cam.Close()

    # ------------------------------------------------------------------
    # InstantCamera(bool firstFound) tests
    # ------------------------------------------------------------------

    def test_constructor_bool_true_attaches_device(self):
        """InstantCamera(FirstFound) uses CreateFirstDevice() and attaches a device."""
        cam = pylon.InstantCamera(pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_constructor_bool_true_can_open(self):
        """InstantCamera(FirstFound) – the attached device can be opened."""
        cam = pylon.InstantCamera(pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_constructor_bool_true_can_grab(self):
        """InstantCamera(FirstFound) – grabbing works after construction."""
        cam = pylon.InstantCamera(pylon.FirstFound)
        cam.Open()
        result = cam.GrabOne(1000)
        self.assertTrue(result.GrabSucceeded())
        cam.Close()

    # ------------------------------------------------------------------
    # InstantCamera(DeviceInfo, bool firstFound) tests
    # ------------------------------------------------------------------

    def test_constructor_device_info_first_found_attaches_device(self):
        """InstantCamera(DeviceInfo, FirstFound) uses CreateFirstDevice with a filter."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera(di, pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_constructor_device_info_first_found_can_open(self):
        """InstantCamera(DeviceInfo, FirstFound) – the attached device can be opened."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera(di, pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_constructor_device_info_first_found_matches_class(self):
        """InstantCamera(DeviceInfo, FirstFound) – attached device matches the requested class."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera(di, pylon.FirstFound)
        self.assertEqual(cam.GetDeviceInfo().GetDeviceClass(), self.device_class)

    def test_constructor_device_info_exact_attaches_device(self):
        """InstantCamera(DeviceInfo, Unambiguous) uses CreateDevice for an exact match."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(di, pylon.Unambiguous)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_constructor_device_info_exact_can_open(self):
        """InstantCamera(DeviceInfo, Unambiguous) – the attached device can be opened."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(di, pylon.Unambiguous)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_constructor_device_info_exact_matches_serial(self):
        """InstantCamera(DeviceInfo, Unambiguous) – attached device has the requested serial number."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(di, pylon.Unambiguous)
        self.assertEqual(
            cam.GetDeviceInfo().GetSerialNumber(),
            di.GetSerialNumber(),
        )

    def test_constructor_device_info_exact_can_grab(self):
        """InstantCamera(DeviceInfo, Unambiguous) – grabbing works after construction."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(di, pylon.Unambiguous)
        cam.Open()
        result = cam.GrabOne(1000)
        self.assertTrue(result.GrabSucceeded())
        cam.Close()

    # ------------------------------------------------------------------
    # InstantCamera(dict, bool firstFound) tests
    # ------------------------------------------------------------------

    def test_constructor_dict_first_found_attaches_device(self):
        """InstantCamera(dict, FirstFound) converts dict to DeviceInfo and uses CreateFirstDevice."""
        cam = pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_constructor_dict_first_found_can_open(self):
        """InstantCamera(dict, FirstFound) – the attached device can be opened."""
        cam = pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_constructor_dict_first_found_matches_class(self):
        """InstantCamera(dict, FirstFound) – attached device matches the requested class."""
        cam = pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound)
        self.assertEqual(cam.GetDeviceInfo().GetDeviceClass(), self.device_class)

    def test_constructor_dict_first_found_can_grab(self):
        """InstantCamera(dict, FirstFound) – grabbing works after construction."""
        cam = pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound)
        cam.Open()
        result = cam.GrabOne(1000)
        self.assertTrue(result.GrabSucceeded())
        cam.Close()

    def test_constructor_dict_exact_attaches_device(self):
        """InstantCamera(dict, Unambiguous) converts dict to DeviceInfo and uses CreateDevice."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        )
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_constructor_dict_exact_can_open(self):
        """InstantCamera(dict, Unambiguous) – the attached device can be opened."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        )
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_constructor_dict_exact_matches_serial(self):
        """InstantCamera(dict, Unambiguous) – attached device has the requested serial number."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        serial = di.GetSerialNumber()
        cam = pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": serial},
            pylon.Unambiguous,
        )
        self.assertEqual(cam.GetDeviceInfo().GetSerialNumber(), serial)

    def test_constructor_dict_exact_can_grab(self):
        """InstantCamera(dict, Unambiguous) – grabbing works after construction."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        )
        cam.Open()
        result = cam.GrabOne(1000)
        self.assertTrue(result.GrabSucceeded())
        cam.Close()

    def test_has_hardware_interface(self):
        cam = self.create_first()
        cam.Open()
        self.assertFalse(cam.IsUsb())
        self.assertFalse(cam.IsCameraLink())
        self.assertFalse(cam.IsGigE())

        cam.Close()

        #######################################################
        # Can't test Eventhandlers with Emulated Cameras      #
        #######################################################

    # ------------------------------------------------------------------
    # Attach(bool firstFound) tests
    # ------------------------------------------------------------------

    def test_attach_bool_true_attaches_device(self):
        """Attach(FirstFound) uses CreateFirstDevice() and attaches a device."""
        cam = pylon.InstantCamera()
        cam.Attach(pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_attach_bool_true_can_open(self):
        """Attach(FirstFound) – the attached device can be opened."""
        cam = pylon.InstantCamera()
        cam.Attach(pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_attach_bool_true_can_grab(self):
        """Attach(FirstFound) – grabbing works after attaching."""
        cam = pylon.InstantCamera()
        cam.Attach(pylon.FirstFound)
        cam.Open()
        result = cam.GrabOne(1000)
        self.assertTrue(result.GrabSucceeded())
        cam.Close()

    # ------------------------------------------------------------------
    # Attach(DeviceInfo, bool firstFound) tests
    # ------------------------------------------------------------------

    def test_attach_device_info_first_found_attaches_device(self):
        """Attach(DeviceInfo, FirstFound) uses CreateFirstDevice with a filter."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_attach_device_info_first_found_can_open(self):
        """Attach(DeviceInfo, FirstFound) – the attached device can be opened."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_attach_device_info_first_found_matches_class(self):
        """Attach(DeviceInfo, FirstFound) – attached device matches the requested class."""
        di = pylon.DeviceInfo()
        di.SetDeviceClass(self.device_class)
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.FirstFound)
        self.assertEqual(cam.GetDeviceInfo().GetDeviceClass(), self.device_class)

    def test_attach_device_info_exact_attaches_device(self):
        """Attach(DeviceInfo, Unambiguous) uses CreateDevice for an exact match."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.Unambiguous)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_attach_device_info_exact_can_open(self):
        """Attach(DeviceInfo, Unambiguous) – the attached device can be opened."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.Unambiguous)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_attach_device_info_exact_matches_serial(self):
        """Attach(DeviceInfo, Unambiguous) – attached device has the requested serial number."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera()
        cam.Attach(di, pylon.Unambiguous)
        self.assertEqual(
            cam.GetDeviceInfo().GetSerialNumber(),
            di.GetSerialNumber(),
        )

    # ------------------------------------------------------------------
    # Attach(dict, bool firstFound) tests
    # ------------------------------------------------------------------

    def test_attach_dict_first_found_attaches_device(self):
        """Attach(dict, FirstFound) converts dict to DeviceInfo and uses CreateFirstDevice."""
        cam = pylon.InstantCamera()
        cam.Attach({"DeviceClass": self.device_class}, pylon.FirstFound)
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_attach_dict_first_found_can_open(self):
        """Attach(dict, FirstFound) – the attached device can be opened."""
        cam = pylon.InstantCamera()
        cam.Attach({"DeviceClass": self.device_class}, pylon.FirstFound)
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_attach_dict_first_found_matches_class(self):
        """Attach(dict, FirstFound) – attached device matches the requested class."""
        cam = pylon.InstantCamera()
        cam.Attach({"DeviceClass": self.device_class}, pylon.FirstFound)
        self.assertEqual(cam.GetDeviceInfo().GetDeviceClass(), self.device_class)

    def test_attach_dict_exact_attaches_device(self):
        """Attach(dict, Unambiguous) converts dict to DeviceInfo and uses CreateDevice."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera()
        cam.Attach(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        )
        self.assertTrue(cam.IsPylonDeviceAttached())

    def test_attach_dict_exact_can_open(self):
        """Attach(dict, Unambiguous) – the attached device can be opened."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        cam = pylon.InstantCamera()
        cam.Attach(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        )
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()

    def test_attach_dict_exact_matches_serial(self):
        """Attach(dict, Unambiguous) – attached device has the requested serial number."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        serial = di.GetSerialNumber()
        cam = pylon.InstantCamera()
        cam.Attach(
            {"DeviceClass": self.device_class, "SerialNumber": serial},
            pylon.Unambiguous,
        )
        self.assertEqual(cam.GetDeviceInfo().GetSerialNumber(), serial)

    # ------------------------------------------------------------------
    # with-statement (__enter__ / __exit__) tests
    # ------------------------------------------------------------------

    def test_with_no_device_does_not_open(self):
        """with InstantCamera() – no device attached, __enter__ does not open."""
        with pylon.InstantCamera() as cam:
            self.assertFalse(cam.IsPylonDeviceAttached())
            self.assertFalse(cam.IsOpen())

    def test_with_no_device_exit_does_not_raise(self):
        """with InstantCamera() – __exit__ on an unattached camera does not raise."""
        with pylon.InstantCamera():
            pass  # should not raise

    def test_with_bool_true_opens_and_destroys(self):
        """with InstantCamera(FirstFound) – device is open inside block and destroyed on exit."""
        with pylon.InstantCamera(pylon.FirstFound) as cam:
            self.assertTrue(cam.IsOpen())
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_with_bool_true_can_grab(self):
        """with InstantCamera(FirstFound) – grabbing works inside the with block."""
        with pylon.InstantCamera(pylon.FirstFound) as cam:
            result = cam.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_with_device_info_first_found_opens_and_destroys(self):
        """with InstantCamera(DeviceInfo, FirstFound) – device is open inside block and destroyed on exit."""
        di = pylon.DeviceInfo()
        di.DeviceClass = self.device_class
        with pylon.InstantCamera(di, pylon.FirstFound) as cam:
            self.assertTrue(cam.IsOpen())
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_with_device_info_exact_opens_and_destroys(self):
        """with InstantCamera(DeviceInfo, Unambiguous) – device is open inside block and destroyed on exit."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        with pylon.InstantCamera(devices[0], pylon.Unambiguous) as cam:
            self.assertTrue(cam.IsOpen())
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_with_device_info_exact_can_grab(self):
        """with InstantCamera(DeviceInfo, Unambiguous) – grabbing works inside the with block."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        with pylon.InstantCamera(devices[0], pylon.Unambiguous) as cam:
            result = cam.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_with_dict_first_found_opens_and_destroys(self):
        """with InstantCamera(dict, FirstFound) – device is open inside block and destroyed on exit."""
        with pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound) as cam:
            self.assertTrue(cam.IsOpen())
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_with_dict_exact_opens_and_destroys(self):
        """with InstantCamera(dict, Unambiguous) – device is open inside block and destroyed on exit."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        with pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        ) as cam:
            self.assertTrue(cam.IsOpen())
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_with_dict_exact_can_grab(self):
        """with InstantCamera(dict, Unambiguous) – grabbing works inside the with block."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        di = devices[0]
        with pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": di.GetSerialNumber()},
            pylon.Unambiguous,
        ) as cam:
            result = cam.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_with_exception_still_destroys_device(self):
        """with InstantCamera(FirstFound) – __exit__ destroys device even when an exception is raised."""
        cam_ref = None
        try:
            with pylon.InstantCamera(pylon.FirstFound) as cam:
                cam_ref = cam
                raise RuntimeError("test error")
        except RuntimeError:
            pass
        self.assertIsNotNone(cam_ref)
        self.assertFalse(cam_ref.IsPylonDeviceAttached())
        self.assertFalse(cam_ref.IsOpen())


if __name__ == "__main__":
    unittest.main()
