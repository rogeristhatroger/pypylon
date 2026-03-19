from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class LoadAndSaveTestSuite(PylonEmuTestCase):
    def test_camemu_value(self):
        deviceclass = pylon.BaslerCamEmuDeviceClass
        self.assertEqual( deviceclass , "BaslerCamEmu" )

    def test_ipcam_value(self):
        deviceclass = pylon.BaslerIpCamDeviceClass
        self.assertEqual( deviceclass , "BaslerIPCam" )
    def test_cameralink_value(self):
        deviceclass = pylon.BaslerCameraLinkDeviceClass
        self.assertEqual( deviceclass , "BaslerCameraLink" )

    def test_gentlgev_value(self):
        deviceclass = pylon.BaslerGenTlGevDeviceClass
        self.assertEqual( deviceclass , "BaslerGTC/Basler/GEV" )

    def test_gentlu3b_value(self):
        deviceclass = pylon.BaslerGenTlU3vDeviceClass
        self.assertEqual( deviceclass , "BaslerGTC/Basler/U3V" )

    def test_gentlcxpv_value(self):
        deviceclass = pylon.BaslerGenTlCxpDeviceClass
        self.assertEqual( deviceclass , "BaslerGTC/Basler/CXP" )

    def test_gentlblaze_value(self):
        deviceclass = pylon.BaslerGenTlBlazeDeviceClass
        self.assertEqual( deviceclass , "BaslerGTC/Basler/GenTL_Producer_for_Basler_blaze_101_cameras" )

    def test_gentlsta_value(self):
        deviceclass = pylon.BaslerGenTlStaDeviceClass
        self.assertEqual( deviceclass , "BaslerGTC/Basler/basler_xw" )

    def test_usb_value(self):
        deviceclass = pylon.BaslerUsbDeviceClass
        self.assertEqual( deviceclass , "BaslerUsb" )
    def test_camemu_not_writable(self):
        original = pylon.BaslerCamEmuDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerCamEmuDeviceClass", "writable")
        self.assertEqual(pylon.BaslerCamEmuDeviceClass, original)

    def test_ipcam_not_writable(self):
        original = pylon.BaslerIpCamDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerIpCamDeviceClass", "writable")
        self.assertEqual(pylon.BaslerIpCamDeviceClass, original)

    def test_cameralink_not_writable(self):
        original = pylon.BaslerCameraLinkDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerCameraLinkDeviceClass", "writable")
        self.assertEqual(pylon.BaslerCameraLinkDeviceClass, original)

    def test_gentlgev_not_writable(self):
        original = pylon.BaslerGenTlGevDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerGenTlGevDeviceClass", "writable")
        self.assertEqual(pylon.BaslerGenTlGevDeviceClass, original)

    def test_gentlu3v_not_writable(self):
        original = pylon.BaslerGenTlU3vDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerGenTlU3vDeviceClass", "writable")
        self.assertEqual(pylon.BaslerGenTlU3vDeviceClass, original)

    def test_gentlcxp_not_writable(self):
        original = pylon.BaslerGenTlCxpDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerGenTlCxpDeviceClass", "writable")
        self.assertEqual(pylon.BaslerGenTlCxpDeviceClass, original)

    def test_gentlblaze_not_writable(self):
        original = pylon.BaslerGenTlBlazeDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerGenTlBlazeDeviceClass", "writable")
        self.assertEqual(pylon.BaslerGenTlBlazeDeviceClass, original)

    def test_gentlsta_not_writable(self):
        original = pylon.BaslerGenTlStaDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerGenTlStaDeviceClass", "writable")
        self.assertEqual(pylon.BaslerGenTlStaDeviceClass, original)

    def test_usb_not_writable(self):
        original = pylon.BaslerUsbDeviceClass
        with self.assertRaises((AttributeError, TypeError)):
            setattr(pylon, "BaslerUsbDeviceClass", "writable")
        self.assertEqual(pylon.BaslerUsbDeviceClass, original)

'''
    const char* const BaslerIpCamDeviceClass = "BaslerIPCam"; ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
    const char* const BaslerCameraLinkDeviceClass = "BaslerCameraLink"; ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
    const char* const BaslerGenTlDeviceClassPrefix = "BaslerGTC";    ///< The actual device class string is made up of this prefix + '/' + [TL Vendor] + '/' + [TL Model].
    const char* const BaslerGenTlGevDeviceClass = "BaslerGTC/Basler/GEV";
    const char* const BaslerGenTlU3vDeviceClass = "BaslerGTC/Basler/U3V";
    const char* const BaslerGenTlCxpDeviceClass = "BaslerGTC/Basler/CXP"; ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
    const char* const BaslerGenTlBlazeDeviceClass = "BaslerGTC/Basler/GenTL_Producer_for_Basler_blaze_101_cameras"; ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
    const char* const BaslerGenTlStaDeviceClass = "BaslerGTC/Basler/basler_xw"; ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
    const char* const BaslerUsbDeviceClass = "BaslerUsb";            ///< This device class can be used to create the corresponding Transport Layer object or when creating Devices with the Transport Layer Factory.
'''
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

