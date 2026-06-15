"""\
This unit test checks BaslerCompressionBeyond lossless decompression for USB cameras.
"""
from pylonusbtestcase import PylonTestCase
from pypylon import pylon
import unittest

from numpy.testing import assert_array_equal


class DecompressionTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _setup_compression(self, camera):
        """Configure camera for lossless BaslerCompressionBeyond and return a reference array.

        Grabs one uncompressed image as the reference, then switches the camera
        into lossless compression mode.  Skips the calling test if the camera
        does not support BaslerCompressionBeyond.
        """
        camera.ExposureTime.SetToMinimum()
        camera.PixelFormat.TrySetValue("Mono8")
        camera.TestPattern.TrySetValue("Testimage1")

        camera.ImageCompressionMode.TrySetValue("Off")
        with camera.GrabOne(10000) as reference_image:
            reference_array = reference_image.Array.copy()

        if not camera.ImageCompressionMode.TrySetValue("BaslerCompressionBeyond"):
            self.skipTest("Camera does not support BaslerCompressionBeyond.")

        camera.ImageCompressionRateOption.TrySetValue("Lossless")
        camera.BslImageCompressionRatio.TrySetValue(100.0)

        return reference_array

    # ------------------------------------------------------------------
    # Grab compressed (raw buffer)
    # ------------------------------------------------------------------

    def test_grab_compressed(self):
        """Decompressing via raw payload buffer matches the uncompressed reference."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            reference_array = self._setup_compression(camera)

            decompressor = pylon.ImageDecompressor()
            descriptor = camera.BslImageCompressionBCBDescriptor.GetAll()
            decompressor.SetCompressionDescriptor(descriptor)

            with camera.GrabOne(10000) as compressed_image:
                payload = compressed_image.GetBuffer()
                decompressed_image = decompressor.DecompressImage(payload)
                decompressed_array = decompressed_image.Array

            assert_array_equal(reference_array, decompressed_array)

    # ------------------------------------------------------------------
    # Decompress image (GrabResultPtr)
    # ------------------------------------------------------------------

    def test_decompress_image(self):
        """Decompressing via GrabResultPtr directly matches the uncompressed reference."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            reference_array = self._setup_compression(camera)

            decompressor = pylon.ImageDecompressor()
            descriptor = camera.BslImageCompressionBCBDescriptor.GetAll()
            decompressor.SetCompressionDescriptor(descriptor)

            with camera.GrabOne(10000) as compressed_image:
                decompressed_image = decompressor.DecompressImage(compressed_image)
                decompressed_array = decompressed_image.Array

            assert_array_equal(reference_array, decompressed_array)


if __name__ == "__main__":
    unittest.main()
