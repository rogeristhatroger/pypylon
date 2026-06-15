"""\
This unit test checks the RegionEntryRLE32 type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class RegionEntryTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init_RegionEntryRLE32(self):
        """RegionEntryRLE32 supports default and value construction."""
        default_entry = pylondataprocessing.RegionEntryRLE32()
        self.assertEqual(default_entry.StartX, 0.0)
        self.assertEqual(default_entry.EndX, 0.0)
        self.assertEqual(default_entry.Y, 0.0)
        entry_from_values = pylondataprocessing.RegionEntryRLE32(10, 30, 40)
        self.assertEqual(entry_from_values.StartX, 10)
        self.assertEqual(entry_from_values.EndX, 30)
        self.assertEqual(entry_from_values.Y, 40)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(RegionEntryRLE32) renders start, end and row."""
        entry = pylondataprocessing.RegionEntryRLE32(10, 30, 40)
        self.assertEqual(str(entry), "StartX = 10; EndX = 30; Y = 40")


if __name__ == "__main__":
    unittest.main()
