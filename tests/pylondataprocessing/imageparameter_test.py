"""Tests for `src/pylondataprocessing/ImageParameter.i`."""

from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylon
from pypylon import pylondataprocessing
import unittest


class ImageParameterTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Availability / construction
    # ------------------------------------------------------------------

    def test_image_parameter_symbol_when_available(self):
        """ImageParameter is exposed (when supported) and derives from pylon.Parameter."""
        if not hasattr(pylondataprocessing, "ImageParameter"):
            self.skipTest("ImageParameter is not available in this DataProcessing SDK version")

        image_parameter = pylondataprocessing.ImageParameter()
        self.assertIsInstance(image_parameter, pylondataprocessing.ImageParameter)
        self.assertTrue(isinstance(image_parameter, pylon.Parameter))


if __name__ == "__main__":
    unittest.main()

