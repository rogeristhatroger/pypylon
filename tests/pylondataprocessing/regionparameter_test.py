"""Tests for `src/pylondataprocessing/RegionParameter.i`."""

from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylon
from pypylon import pylondataprocessing
import unittest


class RegionParameterTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Availability / construction
    # ------------------------------------------------------------------

    def test_region_parameter_symbol_when_available(self):
        """RegionParameter is exposed (when supported) and derives from pylon.Parameter."""
        if not hasattr(pylondataprocessing, "RegionParameter"):
            self.skipTest("RegionParameter is not available in this DataProcessing SDK version")

        region_parameter = pylondataprocessing.RegionParameter()
        self.assertIsInstance(region_parameter, pylondataprocessing.RegionParameter)
        self.assertTrue(isinstance(region_parameter, pylon.Parameter))


if __name__ == "__main__":
    unittest.main()

