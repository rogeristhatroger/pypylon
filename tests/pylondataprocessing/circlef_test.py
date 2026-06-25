"""\
This unit test checks the CircleF type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class CircleFTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """CircleF supports default, coordinate, point-based and copy construction."""
        default_circle = pylondataprocessing.CircleF()
        self.assertEqual(default_circle.Center.X, 0.0)
        self.assertEqual(default_circle.Center.Y, 0.0)
        self.assertEqual(default_circle.Radius, 0.0)
        circle_from_coordinates = pylondataprocessing.CircleF(1.2, 3.4, 5.6)
        self.assertEqual(circle_from_coordinates.Center.X, 1.2)
        self.assertEqual(circle_from_coordinates.Center.Y, 3.4)
        self.assertEqual(circle_from_coordinates.Radius, 5.6)
        circle_from_point = pylondataprocessing.CircleF(pylondataprocessing.PointF2D(1.22, 3.42), 5.62)
        self.assertEqual(circle_from_point.Center.X, 1.22)
        self.assertEqual(circle_from_point.Center.Y, 3.42)
        self.assertEqual(circle_from_point.Radius, 5.62)
        copied_circle = pylondataprocessing.CircleF(circle_from_point)
        self.assertEqual(copied_circle.Center.X, 1.22)
        self.assertEqual(copied_circle.Center.Y, 3.42)
        self.assertEqual(copied_circle.Radius, 5.62)
        # Center returns _Center with a reference to its parent added.
        # _Center holds a pointer to the C++ member SCircleF::Center.
        # CircleF must not be released while using _Center.
        self.assertEqual(copied_circle.Center.X, copied_circle._Center.X)
        copied_circle.Center.Y = 1234.5
        self.assertEqual(copied_circle.Center.Y, 1234.5)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(CircleF) renders center and radius."""
        circle = pylondataprocessing.CircleF(1.2, 3.4, 5.6)
        self.assertEqual(str(circle), "Center: (X = 1.2; Y = 3.4); Radius = 5.6")


if __name__ == "__main__":
    unittest.main()
