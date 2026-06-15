"""\
This unit test checks the RecipeFileFormat enum bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest


class RecipeFileFormatTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    def test_presence(self):
        """RecipeFileFormat constants expose their documented values (data processing 3.1+)."""
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(3, 1, 0):
            self.assertEqual(pylondataprocessing.RecipeFileFormat_JsonDefault, 1)
            self.assertEqual(pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData, 2)


if __name__ == "__main__":
    unittest.main()
