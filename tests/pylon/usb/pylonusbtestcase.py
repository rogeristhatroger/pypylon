import unittest
from pypylon import pylon


class PylonTestCase(unittest.TestCase):
    def get_camera_traits(self):
        return {pylon.DeviceClassKey: pylon.BaslerUsbDeviceClass}
