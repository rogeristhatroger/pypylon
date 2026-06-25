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

if __name__ == "__main__":
    unittest.main()

