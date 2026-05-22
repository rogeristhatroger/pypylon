from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class InstantCameraArrayTestSuite(PylonEmuTestCase):
    def test_constructor_empty(self):
        cameraArray = pylon.InstantCameraArray()
        self.assertEqual(0, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())
        # Test if no Camera is connected
        for cam in cameraArray:
            self.fail()

    def test_initialize(self):
        cameraArray = pylon.InstantCameraArray()
        self.assertEqual(0, cameraArray.GetSize())
        cameraArray.Initialize(self.num_devices)
        self.assertEqual(self.num_devices, cameraArray.GetSize())
        v = 0
        for cam in cameraArray:
            v += 1
        self.assertEqual(self.num_devices, v)

    def test_connect_cameras(self):
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        self.assertEqual(len(devices), self.num_devices)
        cameraArray = pylon.InstantCameraArray(self.num_devices)
        for i, cam in enumerate(cameraArray):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.Open()

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.StartGrabbing()

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertTrue(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.RetrieveResult(300)

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertTrue(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.StopGrabbing()

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.Close()

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.DestroyDevice()

        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

    def test_detach_cameras(self):

        cameraArray = pylon.InstantCameraArray(self.num_devices)
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        self.assertEqual(len(devices), self.num_devices)
        for i, cam in enumerate(cameraArray):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))

        cameraArray.Open()
        cameraArray.StartGrabbing()
        cameraArray.DetachDevice()
        self.assertEqual(self.num_devices, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

    def test_grab_multiple_cameras(self):
        twoCamsUsed = False
        # Number of images to be grabbed.
        countOfImagesToGrab = 10
        # Limits the amount of cameras used for grabbing.
        maxCamerasToUse = 2
        # Get the transport layer factory.
        tlFactory = pylon.TlFactory.GetInstance()
        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices(self.device_filter)
        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
        l = cameras.GetSize()
        self.assertEqual(2, l)  # Are 2 Cameras initialized
        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(tlFactory.CreateDevice(devices[i]))
        cameras.Open()
        for i, cam in enumerate(cameras):
            cam.Width.Value = 1024
            cam.Height.Value = 1040
            cam.PixelFormat.Value = "Mono8"
            cam.ExposureTimeAbs.Value = 10000.0
        # Starts grabbing for all cameras
        cameras.StartGrabbing()
        # Grab c_countOfImagesToGrab from the cameras.
        for i in range(countOfImagesToGrab):
            if not cameras.IsGrabbing():
                break
            grabResult = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            cameraContextValue = grabResult.GetCameraContext()
            if (cameraContextValue == 1):
                twoCamsUsed = True
            # Now, the image data can be processed.
            self.assertEqual(True, grabResult.GrabSucceeded())
            img = grabResult.GetArray()
            first_line = img[0]
            prev = int(first_line[0])
            for pxl in first_line[1:]:
                self.assertEqual(int(pxl), (prev + 1) % 256)
                prev = int(pxl)
        self.assertTrue(twoCamsUsed)  # Are 2 Cameras actually used

if __name__ == "__main__":
    unittest.main()
