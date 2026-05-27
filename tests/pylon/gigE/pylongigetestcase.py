"""\
Base test case class for pypylon unit tests that use a Basler GigE camera.
"""
from pypylon import pylon
import unittest


def get_class_and_filter():
    device_class = pylon.BaslerGigEDeviceClass
    device_info = pylon.DeviceInfo()
    device_info.DeviceClass = device_class
    return device_class, [device_info]


class PylonTestCase(unittest.TestCase):
    device_class, device_filter = get_class_and_filter()

    def get_camera_traits(self):
        return {"DeviceClass": pylon.BaslerGigEDeviceClass}

    def create_first(self):
        tl_factory = pylon.TlFactory.GetInstance()
        return pylon.InstantCamera(tl_factory.CreateFirstDevice(self.device_filter[0]))
