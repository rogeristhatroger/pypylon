"""\
This unit test checks the QueueMode enum bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class QueueModeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    def test_presence(self):
        """All public QueueMode constants expose their documented values."""
        self.assertEqual(pylondataprocessing.QueueMode_Unlimited, 0)
        self.assertEqual(pylondataprocessing.QueueMode_DropOldest, 1)
        self.assertEqual(pylondataprocessing.QueueMode_DropNewest, 2)
        self.assertEqual(pylondataprocessing.QueueMode_Blocking, 3)


if __name__ == "__main__":
    unittest.main()
