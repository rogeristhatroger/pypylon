"""\
This unit test checks the LineF2D type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class LineF2DTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """LineF2D supports default, coordinate, point-based and copy construction."""
        default_line = pylondataprocessing.LineF2D()
        self.assertEqual(default_line.PointA.X, 0.0)
        self.assertEqual(default_line.PointA.Y, 0.0)
        self.assertEqual(default_line.PointB.X, 0.0)
        self.assertEqual(default_line.PointB.Y, 0.0)
        line_from_coordinates = pylondataprocessing.LineF2D(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(line_from_coordinates.PointA.X, 1.2)
        self.assertEqual(line_from_coordinates.PointA.Y, 3.4)
        self.assertEqual(line_from_coordinates.PointB.X, 5.6)
        self.assertEqual(line_from_coordinates.PointB.Y, 7.8)
        line_from_points = pylondataprocessing.LineF2D(
            pylondataprocessing.PointF2D(1.22, 3.42), pylondataprocessing.PointF2D(5.62, 7.82))
        self.assertEqual(line_from_points.PointA.X, 1.22)
        self.assertEqual(line_from_points.PointA.Y, 3.42)
        self.assertEqual(line_from_points.PointB.X, 5.62)
        self.assertEqual(line_from_points.PointB.Y, 7.82)
        copied_line = pylondataprocessing.LineF2D(line_from_points)
        self.assertEqual(copied_line.PointA.X, 1.22)
        self.assertEqual(copied_line.PointA.Y, 3.42)
        self.assertEqual(copied_line.PointB.X, 5.62)
        self.assertEqual(copied_line.PointB.Y, 7.82)
        # PointA returns _PointA with a reference to its parent added.
        # _PointA holds a pointer to the C++ member SLineF2D::PointA.
        # LineF2D must not be released while using _PointA.
        self.assertEqual(copied_line.PointA.X, copied_line._PointA.X)
        self.assertEqual(copied_line.PointB.X, copied_line._PointB.X)
        copied_line.PointB.Y = 1234.5
        self.assertEqual(copied_line.PointB.Y, 1234.5)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(LineF2D) renders both end points."""
        line = pylondataprocessing.LineF2D(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(str(line), "PointA: (X = 1.2; Y = 3.4); PointB: (X = 5.6; Y = 7.8)")


if __name__ == "__main__":
    unittest.main()
