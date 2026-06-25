"""\
This unit test checks the SmartInstantCameraResult type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class SmartInstantCameraResultTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """A default SmartInstantCameraResult exposes an invalid update, grab result and a dict container."""
        result = pylondataprocessing.SmartInstantCameraResult()
        update = result.Update
        grab_result = result.GrabResult
        container = result.Container
        # GetContainer() is currently also available but not considered part of the official API.
        self.assertFalse(update.IsValid())
        self.assertFalse(grab_result.IsValid())
        self.assertIsInstance(container, dict)
        result.Release()


if __name__ == "__main__":
    unittest.main()
