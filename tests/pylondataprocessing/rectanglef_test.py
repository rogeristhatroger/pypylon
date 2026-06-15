"""\
This unit test checks the RectangleF type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class RectangleFTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """RectangleF supports default, coordinate, point-based, partial and copy construction."""
        default_rectangle = pylondataprocessing.RectangleF()
        self.assertEqual(default_rectangle.Center.X, 0.0)
        self.assertEqual(default_rectangle.Center.Y, 0.0)
        self.assertEqual(default_rectangle.Width, 0.0)
        self.assertEqual(default_rectangle.Height, 0.0)
        self.assertEqual(default_rectangle.Rotation, 0.0)
        rectangle_from_coordinates = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(rectangle_from_coordinates.Center.X, 1.2)
        self.assertEqual(rectangle_from_coordinates.Center.Y, 3.4)
        self.assertEqual(rectangle_from_coordinates.Width, 5.6)
        self.assertEqual(rectangle_from_coordinates.Height, 7.8)
        self.assertEqual(rectangle_from_coordinates.Rotation, 9.0)
        rectangle_from_point = pylondataprocessing.RectangleF(
            pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82, 9.02)
        self.assertEqual(rectangle_from_point.Center.X, 1.22)
        self.assertEqual(rectangle_from_point.Center.Y, 3.42)
        self.assertEqual(rectangle_from_point.Width, 5.62)
        self.assertEqual(rectangle_from_point.Height, 7.82)
        self.assertEqual(rectangle_from_point.Rotation, 9.02)
        rectangle_without_rotation = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(rectangle_without_rotation.Center.X, 1.2)
        self.assertEqual(rectangle_without_rotation.Center.Y, 3.4)
        self.assertEqual(rectangle_without_rotation.Width, 5.6)
        self.assertEqual(rectangle_without_rotation.Height, 7.8)
        self.assertEqual(rectangle_without_rotation.Rotation, 0.0)
        rectangle_from_point_without_rotation = pylondataprocessing.RectangleF(
            pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82)
        self.assertEqual(rectangle_from_point_without_rotation.Center.X, 1.22)
        self.assertEqual(rectangle_from_point_without_rotation.Center.Y, 3.42)
        self.assertEqual(rectangle_from_point_without_rotation.Width, 5.62)
        self.assertEqual(rectangle_from_point_without_rotation.Height, 7.82)
        self.assertEqual(rectangle_from_point_without_rotation.Rotation, 0.0)
        copied_rectangle = pylondataprocessing.RectangleF(
            rectangle_from_point_without_rotation)
        self.assertEqual(copied_rectangle.Center.X, 1.22)
        self.assertEqual(copied_rectangle.Center.Y, 3.42)
        self.assertEqual(copied_rectangle.Width, 5.62)
        self.assertEqual(copied_rectangle.Height, 7.82)
        self.assertEqual(copied_rectangle.Rotation, 0.0)
        # Center returns _Center with a reference to its parent added.
        # _Center holds a pointer to the C++ member SRectangleF::Center.
        # RectangleF must not be released while using _Center.
        self.assertEqual(copied_rectangle.Center.X, copied_rectangle._Center.X)
        copied_rectangle.Center.Y = 1234.5
        self.assertEqual(copied_rectangle.Center.Y, 1234.5)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(RectangleF) renders center, size and rotation."""
        rectangle = pylondataprocessing.RectangleF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(
            str(rectangle),
            "Center: (X = 1.2; Y = 3.4); Width = 5.6; Height = 7.8; Rotation = 9.0 rad")


if __name__ == "__main__":
    unittest.main()
