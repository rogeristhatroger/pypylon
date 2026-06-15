"""\
This unit test checks the PointF2D type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class PointF2DTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """PointF2D supports default, coordinate and copy construction."""
        default_point = pylondataprocessing.PointF2D()
        self.assertEqual(default_point.X, 0.0)
        self.assertEqual(default_point.Y, 0.0)
        point_from_coordinates = pylondataprocessing.PointF2D(1.2, 3.4)
        self.assertEqual(point_from_coordinates.X, 1.2)
        self.assertEqual(point_from_coordinates.Y, 3.4)
        copied_point = pylondataprocessing.PointF2D(point_from_coordinates)
        self.assertEqual(copied_point.X, 1.2)
        self.assertEqual(copied_point.Y, 3.4)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(PointF2D) renders the coordinates."""
        point = pylondataprocessing.PointF2D(1.2, 3.4)
        self.assertEqual(str(point), "X = 1.2; Y = 3.4")


if __name__ == "__main__":
    unittest.main()
