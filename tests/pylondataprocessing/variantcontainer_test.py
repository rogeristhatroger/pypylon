"""\
This unit test verifies that the legacy VariantContainer symbol is no longer exposed.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class VariantContainerTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # API removal
    # ------------------------------------------------------------------

    def test_variant_container_symbol_is_removed(self):
        """VariantContainer is not part of the public Python API anymore."""
        self.assertFalse(hasattr(pylondataprocessing, "VariantContainer"))


if __name__ == "__main__":
    unittest.main()
