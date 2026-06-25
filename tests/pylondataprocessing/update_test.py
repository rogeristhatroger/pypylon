"""\
This unit test checks the Update type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest


class UpdateTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction / comparison
    # ------------------------------------------------------------------

    def test_init(self):
        """Default-constructed updates are invalid and compare as equal."""
        first_update = pylondataprocessing.Update()
        second_update = pylondataprocessing.Update()
        copied_update = pylondataprocessing.Update(second_update)
        self.assertFalse(first_update.IsValid())
        self.assertEqual(first_update.GetNumPrecedingUpdates(), 0)
        self.assertFalse(first_update.HasBeenTriggeredBy(second_update))
        # Invalid updates compare equal; valid updates are only available from a running recipe.
        self.assertTrue(first_update == second_update)
        self.assertFalse(first_update != second_update)
        self.assertFalse(first_update < second_update)
        with self.assertRaises(genicam.RuntimeException) as context:
            first_update.GetPrecedingUpdate(0)
        self.assertTrue(
            str(context.exception).startswith("This update is invalid. Cannot get preceding updates."))


if __name__ == "__main__":
    unittest.main()
