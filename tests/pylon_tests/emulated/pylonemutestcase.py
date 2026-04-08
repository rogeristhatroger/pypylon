"""\
Base test case class for pypylon unit tests that use the Basler camera emulator.
"""
import os

NUM_CAMERAS = 3
os.environ["PYLON_CAMEMU"] = "%d" % NUM_CAMERAS

from pypylon import pylon
import unittest


def get_class_and_filter():
    device_class = pylon.BaslerCamEmuDeviceClass
    device_info = pylon.DeviceInfo()
    device_info.DeviceClass = device_class
    return device_class, [device_info]


class PylonEmuTestCase(unittest.TestCase):
    num_devices = NUM_CAMERAS
    device_class, device_filter = get_class_and_filter()

    def get_camera_traits(self):
        return {"DeviceClass": pylon.BaslerCamEmuDeviceClass}

    def create_first(self):
        tl_factory = pylon.TlFactory.GetInstance()
        return pylon.InstantCamera(tl_factory.CreateFirstDevice(self.device_filter[0]))
