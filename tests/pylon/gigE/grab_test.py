"""\
This unit test checks basic image grabbing for GigE cameras.
"""
from pylongigetestcase import PylonTestCase
from pypylon import pylon
import unittest


COUNT_OF_IMAGES_TO_GRAB = 5
RETRIEVE_TIMEOUT_MS = 5000


class GrabTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # GrabOne
    # ------------------------------------------------------------------

    def test_grabone(self):
        """GrabOne returns an image with the camera's maximum width and height."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # Just try both parameters to be sure that at least one of them is supported by the camera.
            if not camera.ExposureTime.TrySetToMinimum():
                camera.ExposureTimeAbs.SetToMinimum()
            camera.Width.SetToMaximum()
            camera.Height.SetToMaximum()
            with camera.GrabOne(RETRIEVE_TIMEOUT_MS) as grab_result:
                self.assertEqual(camera.Width.Value, grab_result.Width)
                self.assertEqual(camera.Height.Value, grab_result.Height)

    # ------------------------------------------------------------------
    # Continuous grab
    # ------------------------------------------------------------------

    def test_grab(self):
        """StartGrabbingMax delivers the requested number of images at full resolution."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.SetToMaximum()
            camera.Height.SetToMaximum()
            # Just try both parameters to be sure that at least one of them is supported by the camera.
            if not camera.ExposureTime.TrySetToMinimum():
                camera.ExposureTimeAbs.SetToMinimum()

            image_count = 0
            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)
            while camera.IsGrabbing():
                with camera.RetrieveResult(
                    RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    if grab_result.GrabSucceeded():
                        image_count += 1
                        self.assertEqual(camera.Width.Value, grab_result.Width)
                        self.assertEqual(camera.Height.Value, grab_result.Height)

            self.assertEqual(COUNT_OF_IMAGES_TO_GRAB, image_count)


if __name__ == "__main__":
    unittest.main()
