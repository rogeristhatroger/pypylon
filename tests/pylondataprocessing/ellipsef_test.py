"""\
This unit test checks the EllipseF type bindings of pylondataprocessing.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class EllipseFTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_init(self):
        """EllipseF supports default, coordinate, point-based, partial and copy construction."""
        default_ellipse = pylondataprocessing.EllipseF()
        self.assertEqual(default_ellipse.Center.X, 0.0)
        self.assertEqual(default_ellipse.Center.Y, 0.0)
        self.assertEqual(default_ellipse.Radius1, 0.0)
        self.assertEqual(default_ellipse.Radius2, 0.0)
        self.assertEqual(default_ellipse.Rotation, 0.0)
        ellipse_from_coordinates = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(ellipse_from_coordinates.Center.X, 1.2)
        self.assertEqual(ellipse_from_coordinates.Center.Y, 3.4)
        self.assertEqual(ellipse_from_coordinates.Radius1, 5.6)
        self.assertEqual(ellipse_from_coordinates.Radius2, 7.8)
        self.assertEqual(ellipse_from_coordinates.Rotation, 9.0)
        ellipse_from_point = pylondataprocessing.EllipseF(
            pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82, 9.02)
        self.assertEqual(ellipse_from_point.Center.X, 1.22)
        self.assertEqual(ellipse_from_point.Center.Y, 3.42)
        self.assertEqual(ellipse_from_point.Radius1, 5.62)
        self.assertEqual(ellipse_from_point.Radius2, 7.82)
        self.assertEqual(ellipse_from_point.Rotation, 9.02)
        ellipse_without_rotation = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8)
        self.assertEqual(ellipse_without_rotation.Center.X, 1.2)
        self.assertEqual(ellipse_without_rotation.Center.Y, 3.4)
        self.assertEqual(ellipse_without_rotation.Radius1, 5.6)
        self.assertEqual(ellipse_without_rotation.Radius2, 7.8)
        self.assertEqual(ellipse_without_rotation.Rotation, 0.0)
        ellipse_from_point_without_rotation = pylondataprocessing.EllipseF(
            pylondataprocessing.PointF2D(1.22, 3.42), 5.62, 7.82)
        self.assertEqual(ellipse_from_point_without_rotation.Center.X, 1.22)
        self.assertEqual(ellipse_from_point_without_rotation.Center.Y, 3.42)
        self.assertEqual(ellipse_from_point_without_rotation.Radius1, 5.62)
        self.assertEqual(ellipse_from_point_without_rotation.Radius2, 7.82)
        self.assertEqual(ellipse_from_point_without_rotation.Rotation, 0.0)
        copied_ellipse = pylondataprocessing.EllipseF(
            ellipse_from_point_without_rotation)
        self.assertEqual(copied_ellipse.Center.X, 1.22)
        self.assertEqual(copied_ellipse.Center.Y, 3.42)
        self.assertEqual(copied_ellipse.Radius1, 5.62)
        self.assertEqual(copied_ellipse.Radius2, 7.82)
        self.assertEqual(copied_ellipse.Rotation, 0.0)
        # Center returns _Center with a reference to its parent added.
        # _Center holds a pointer to the C++ member SEllipseF::Center.
        # EllipseF must not be released while using _Center.
        self.assertEqual(copied_ellipse.Center.X, copied_ellipse._Center.X)
        copied_ellipse.Center.Y = 1234.5
        self.assertEqual(copied_ellipse.Center.Y, 1234.5)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(EllipseF) renders center, radii and rotation."""
        ellipse = pylondataprocessing.EllipseF(1.2, 3.4, 5.6, 7.8, 9.0)
        self.assertEqual(
            str(ellipse),
            "Center: (X = 1.2; Y = 3.4); Radius1 = 5.6; Radius2 = 7.8; Rotation = 9.0 rad")


if __name__ == "__main__":
    unittest.main()
