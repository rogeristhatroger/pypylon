"""\
This unit test checks the VariantContainerType enum bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class VariantContainerTypeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    def test_variant_container_type_constants(self):
        """All public VariantContainerType constants expose their documented values."""
        self.assertEqual(pylondataprocessing.VariantContainerType_None, 0)
        self.assertEqual(pylondataprocessing.VariantContainerType_Array, 1)
        self.assertEqual(pylondataprocessing.VariantContainerType_Unsupported, 2)


if __name__ == "__main__":
    unittest.main()


