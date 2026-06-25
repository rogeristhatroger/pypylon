"""\
This unit test checks the RegionType enum bindings and helper functions of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest


class RegionTypeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    def test_presence(self):
        """RegionType constants expose their documented values."""
        self.assertEqual(pylondataprocessing.RegionType_Undefined, -1)
        self.assertEqual(pylondataprocessing.RegionType_RLE32, 6291457)

    # ------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------

    def test_is_valid(self):
        """IsValidRegionType reports valid region types and rejects undefined ones."""
        self.assertTrue(pylondataprocessing.IsValidRegionType(pylondataprocessing.RegionType_RLE32))
        self.assertFalse(pylondataprocessing.IsValidRegionType(pylondataprocessing.RegionType_Undefined))

    def test_bit_per_region_element(self):
        """BitPerRegionElement returns the bit size and raises for undefined region types."""
        self.assertEqual(
            pylondataprocessing.BitPerRegionElement(pylondataprocessing.RegionType_RLE32), 3 * 32)
        with self.assertRaises(genicam.InvalidArgumentException) as context:
            pylondataprocessing.BitPerRegionElement(pylondataprocessing.RegionType_Undefined)
        self.assertTrue(str(context.exception).startswith("Invalid region type passed."))

    def test_compute_region_size(self):
        """ComputeRegionSize returns the buffer size and raises for undefined region types."""
        self.assertEqual(
            pylondataprocessing.ComputeRegionSize(pylondataprocessing.RegionType_RLE32, 10), 3 * 4 * 10)
        with self.assertRaises(genicam.InvalidArgumentException) as context:
            pylondataprocessing.ComputeRegionSize(pylondataprocessing.RegionType_Undefined, 10)
        self.assertTrue(str(context.exception).startswith("Invalid region type passed."))


if __name__ == "__main__":
    unittest.main()
